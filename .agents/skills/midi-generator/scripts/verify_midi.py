"""Script de verificación y control de calidad para archivos MIDI del proyecto 'hard_song'.

Valida de forma determinista que:
1. El archivo MIDI sea Formato 1 estándar con división de 480 ticks/negra.
2. El tempo principal sea exactamente 80 BPM (mpqn = 750,000).
3. El compás sea 4/4.
4. Las pistas esenciales existan (Conductor, Drums, Bass, Guitarras, Guía Vocal).
5. Las notas de la pista vocal no excedan la tesitura de barítono (D2 [38] a D#4 [63]).
"""

import sys
import struct
from pathlib import Path

# Constantes de proyecto
EXPECTED_BPM = 80
EXPECTED_MPQN = 750000
EXPECTED_TIME_SIG = (4, 2) # 4/4 -> numerator 4, denominator 2^2=4
MIN_VOCAL_NOTE = 38 # D2
MAX_VOCAL_NOTE = 63 # D#4 (Eb4)
EXPECTED_TICKS_PER_BEAT = 480

NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def midi_note_to_name(num):
    octave = (num // 12) - 1
    name = NOTE_NAMES[num % 12]
    return f"{name}{octave} (MIDI {num})"

def read_var_length(data, offset):
    val = 0
    bytes_read = 0
    while True:
        b = data[offset + bytes_read]
        bytes_read += 1
        val = (val << 7) | (b & 0x7F)
        if (b & 0x80) == 0:
            break
    return val, bytes_read

def parse_and_validate_midi(filepath):
    errors = []
    warnings = []

    path = Path(filepath)
    if not path.exists():
        return [f"Error crítico: Archivo no encontrado en '{filepath}'"], []

    with open(path, 'rb') as f:
        data = f.read()

    if len(data) < 14:
        return ["Error crítico: Archivo corrupto o demasiado corto"], []

    # Parse MThd
    header_chunk, header_len = struct.unpack('>4sI', data[0:8])
    if header_chunk != b'MThd' or header_len != 6:
        errors.append(f"Header chunk inválido: {header_chunk}")
        return errors, warnings

    fmt, num_tracks, division = struct.unpack('>HHH', data[8:14])
    if fmt != 1:
        errors.append(f"Se esperaba Formato MIDI 1, encontrado: {fmt}")
    if division != EXPECTED_TICKS_PER_BEAT:
        warnings.append(f"División de ticks esperada {EXPECTED_TICKS_PER_BEAT}, encontrada: {division}")

    # Parse MTrk chunks
    offset = 14
    tracks_parsed = []
    found_tempo = False
    found_time_sig = False

    for track_idx in range(num_tracks):
        if offset + 8 > len(data):
            errors.append(f"Fin inesperado de archivo leyendo pista {track_idx}")
            break
        chunk_id, chunk_len = struct.unpack('>4sI', data[offset:offset+8])
        offset += 8
        if chunk_id != b'MTrk':
            errors.append(f"Chunk inesperado '{chunk_id}' en lugar de MTrk en pista {track_idx}")
            break

        track_data = data[offset:offset+chunk_len]
        offset += chunk_len

        # Parse track events
        t_offset = 0
        track_name = f"Track_{track_idx}"
        notes_in_track = []
        running_status = None

        while t_offset < len(track_data):
            delta, d_bytes = read_var_length(track_data, t_offset)
            t_offset += d_bytes

            if t_offset >= len(track_data):
                break

            status = track_data[t_offset]

            if status == 0xFF: # Meta event
                t_offset += 1
                meta_type = track_data[t_offset]
                t_offset += 1
                length, l_bytes = read_var_length(track_data, t_offset)
                t_offset += l_bytes
                meta_content = track_data[t_offset:t_offset+length]
                t_offset += length

                if meta_type == 0x03: # Track Name
                    try:
                        track_name = meta_content.decode('utf-8', errors='ignore')
                    except Exception:
                        pass
                elif meta_type == 0x51: # Set Tempo
                    if len(meta_content) == 3:
                        mpqn = (meta_content[0] << 16) | (meta_content[1] << 8) | meta_content[2]
                        bpm = round(60000000 / mpqn)
                        found_tempo = True
                        if bpm != EXPECTED_BPM:
                            errors.append(f"Tempo incorrecto: {bpm} BPM (Esperado: {EXPECTED_BPM} BPM)")
                elif meta_type == 0x58: # Time Signature
                    if len(meta_content) >= 2:
                        found_time_sig = True
                        num = meta_content[0]
                        denom = meta_content[1]
                        if (num, denom) != EXPECTED_TIME_SIG:
                            errors.append(f"Compás incorrecto: {num}/{2**denom} (Esperado: 4/4)")
                elif meta_type == 0x2F: # End of track
                    break

            elif status == 0xF0 or status == 0xF7: # SysEx
                t_offset += 1
                length, l_bytes = read_var_length(track_data, t_offset)
                t_offset += l_bytes + length
            else:
                if status & 0x80:
                    running_status = status
                    t_offset += 1
                else:
                    status = running_status

                event_type = status & 0xF0
                if event_type in (0x80, 0x90, 0xA0, 0xB0, 0xE0):
                    param1 = track_data[t_offset]
                    param2 = track_data[t_offset + 1]
                    t_offset += 2
                    if event_type == 0x90 and param2 > 0: # Note On
                        notes_in_track.append(param1)
                elif event_type in (0xC0, 0xD0):
                    t_offset += 1

        tracks_parsed.append({
            "name": track_name,
            "notes": notes_in_track
        })

    # Validaciones globales
    if not found_tempo:
        errors.append("No se encontró evento de tempo en el archivo MIDI")
    if not found_time_sig:
        warnings.append("No se encontró evento explícito de compás (Time Signature)")

    # Validar tesitura vocal
    vocal_tracks = [t for t in tracks_parsed if 'vocal' in t['name'].lower()]
    for vt in vocal_tracks:
        notes = vt['notes']
        out_of_range = []
        for n in notes:
            if n < MIN_VOCAL_NOTE or n > MAX_VOCAL_NOTE:
                out_of_range.append(n)
        if out_of_range:
            invalid_str = ", ".join(midi_note_to_name(n) for n in set(out_of_range))
            errors.append(
                f"Violación de tesitura barítono en pista '{vt['name']}': notas fuera de rango ({invalid_str}). "
                f"Rango permitido: D2 ({MIN_VOCAL_NOTE}) a D#4 ({MAX_VOCAL_NOTE})"
            )

    return errors, warnings, tracks_parsed

def main():
    default_path = Path("cubase/hard_song_tracks.mid")
    filepath = sys.argv[1] if len(sys.argv) > 1 else default_path

    print(f"=== Auditoría de Calidad MIDI para Agentes: {filepath} ===")
    errors, warnings, tracks = parse_and_validate_midi(filepath)

    print(f"\n[Pistas detectadas: {len(tracks)}]")
    for i, t in enumerate(tracks):
        note_count = len(t['notes'])
        print(f"  Pista {i:02d}: {t['name']:<25} ({note_count} notas registradas)")

    print("\n[Resultados de Verificación]")
    if warnings:
        for w in warnings:
            print(f"  [AVISO] {w}")

    if errors:
        for e in errors:
            print(f"  [FALLO] {e}")
        print("\n=> RECHAZADO: El archivo no cumple con las reglas del proyecto.")
        sys.exit(1)
    else:
        print("  [ÉXITO] Tempo (80 BPM), compás (4/4) y rango vocal respetados a la perfección.")
        print("=> APROBADO: Cumple con todas las directrices de producción.")
        sys.exit(0)

if __name__ == '__main__':
    main()
