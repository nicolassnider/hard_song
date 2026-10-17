"""Motor genérico de compilación de archivos Standard MIDI File (Formato 1).

Obtiene los tonos, acordes, secciones y eventos desde un módulo de configuración
externo (por defecto `tones.py`).
"""

import importlib
import struct
import sys
import tones as default_tones


def var_length(val):
    result = bytearray()
    result.append(val & 0x7F)
    val >>= 7
    while val > 0:
        result.insert(0, 0x80 | (val & 0x7F))
        val >>= 7
    return bytes(result)


class MidiTrack:
    def __init__(self, name=""):
        self.name = name
        self.events = []  # list of (abs_tick, bytes)
        if name:
            name_bytes = name.encode('utf-8')
            # Meta event 0x03 (Track Name): delta 0, FF 03 len text
            self.events.append((0, b'\xFF\x03' + var_length(len(name_bytes)) + name_bytes))

    def add_meta(self, abs_tick, meta_type, data_bytes):
        self.events.append((abs_tick, b'\xFF' + bytes([meta_type]) + var_length(len(data_bytes)) + data_bytes))

    def add_marker(self, abs_tick, text):
        tb = text.encode('utf-8')
        self.add_meta(abs_tick, 0x06, tb)

    def add_note(self, channel, note, velocity, start_tick, duration_ticks):
        # Note On
        status_on = 0x90 | (channel & 0x0F)
        self.events.append((start_tick, bytes([status_on, note & 0x7F, velocity & 0x7F])))
        # Note Off
        status_off = 0x80 | (channel & 0x0F)
        self.events.append((start_tick + duration_ticks, bytes([status_off, note & 0x7F, 0])))

    def build(self):
        # Sort events by absolute tick (stable sort preserves order)
        self.events.sort(key=lambda e: e[0])
        track_data = bytearray()
        prev_tick = 0
        for abs_tick, event_bytes in self.events:
            delta = abs_tick - prev_tick
            track_data.extend(var_length(delta))
            track_data.extend(event_bytes)
            prev_tick = abs_tick
        # End of track meta event: FF 2F 00
        track_data.extend(var_length(0))
        track_data.extend(b'\xFF\x2F\x00')

        # MTrk header + 4-byte length + track_data
        header = b'MTrk' + struct.pack('>I', len(track_data))
        return header + track_data


def build_project_midi(filename=None, song_module=default_tones):
    ticks_per_quarter = getattr(song_module, 'TICKS_PER_QUARTER', 480)
    bpm = getattr(song_module, 'BPM', 80)
    time_sig = getattr(song_module, 'TIME_SIGNATURE', (4, 2, 24, 8))
    output_path = filename or getattr(song_module, 'OUTPUT_FILENAME', 'c:/repos/hard_song/cubase/hard_song_tracks.mid')

    beats_per_bar = time_sig[0]
    bar_ticks = ticks_per_quarter * beats_per_bar

    # 1. Pista Conductora: Tempo, Compás y Marcadores de Sección
    t_conductor = MidiTrack("00_Tempo_and_Markers")
    mpqn = round(60_000_000 / bpm)
    t_conductor.add_meta(0, 0x51, struct.pack('>I', mpqn)[1:])  # 3 bytes
    t_conductor.add_meta(0, 0x58, bytes(time_sig))

    section_starts = {}
    current_tick = 0
    for sec_id, marker_text, num_bars in song_module.SECTIONS:
        section_starts[sec_id] = current_tick
        t_conductor.add_marker(current_tick, marker_text)
        current_tick += num_bars * bar_ticks

    tracks = [t_conductor]

    # 2. Construcción genérica de pistas a partir del módulo de tonos
    tracks_def = song_module.get_tracks_definition(section_starts, ticks_per_quarter, bar_ticks)
    for t_def in tracks_def:
        midi_track = MidiTrack(t_def["name"])
        channel = t_def["channel"]
        for note, velocity, start_tick, duration_ticks in t_def["events"]:
            midi_track.add_note(channel, note, velocity, start_tick, duration_ticks)
        tracks.append(midi_track)

    num_tracks = len(tracks)

    # Header chunk: MThd, length=6, format=1, num_tracks, division
    header = b'MThd' + struct.pack('>IHHH', 6, 1, num_tracks, ticks_per_quarter)

    with open(output_path, 'wb') as f:
        f.write(header)
        for t in tracks:
            f.write(t.build())

    print(f"Archivo MIDI generado exitosamente: {output_path} ({num_tracks} pistas)")


if __name__ == '__main__':
    module = default_tones
    if len(sys.argv) > 1:
        module = importlib.import_module(sys.argv[1].replace('.py', ''))
    build_project_midi(song_module=module)
