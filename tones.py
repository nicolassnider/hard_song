"""Definición de tonos, acordes, mapeo de batería y patrones musicales para 'Sigo de Pie'.

Este módulo separa los datos musicales del motor de generación MIDI para que
`generate_midi_tracks.py` funcione de forma completamente genérica.
"""

# Configuración general del proyecto
BPM = 80
TICKS_PER_QUARTER = 480
TIME_SIGNATURE = (4, 2, 24, 8)  # 4/4 (numerador 4, denominador 2^2=4)
OUTPUT_FILENAME = 'c:/repos/hard_song/cubase/hard_song_tracks.mid'

# Diccionario de notas MIDI (Tonos base)
NOTES = {
    'F1': 29,
    'G1': 31,
    'A1': 33,
    'Bb1': 34,
    'C2': 36,
    'D2': 38,
    'E2': 40,
    'F2': 41,
    'A2': 45,
    'C3': 48,
    'D3': 50,
    'E3': 52,
    'F3': 53,
    'F#3': 54,
    'G3': 55,
    'A3': 57,
    'Bb3': 58,
    'B3': 59,
    'C4': 60,
    'D4': 62,
    'Eb4': 63,
    'E4': 64,
    'F4': 65,
    'G4': 67,
}

# Mapeo General MIDI para Batería (Canal 10 / índice 9)
DRUMS = {
    'kick': 36,       # Bass Drum 1
    'sidestick': 37,  # Side Stick
    'snare': 38,      # Acoustic Snare
    'floor_tom_l': 41,# Low Floor Tom
    'hh_closed': 42,  # Closed Hi-Hat
    'floor_tom_h': 43,# High Floor Tom
    'low_tom': 45,    # Low Tom
    'hh_open': 46,    # Open Hi-Hat
    'mid_tom': 47,    # Low-Mid Tom
    'crash': 49,      # Crash Cymbal 1
    'high_tom': 50,   # High Tom
    'ride': 51,       # Ride Cymbal 1
}

# Diccionario de acordes y voicings
CHORDS = {
    # Power chords (2 notas para el riff)
    'G5_riff': [NOTES['G3'], NOTES['D4']],
    'Bb5_riff': [NOTES['Bb3'], NOTES['F4']],
    'C5_riff': [NOTES['C4'], NOTES['G4']],
    # Power chords completos (3 notas)
    'F5': [NOTES['F2'], NOTES['C3'], NOTES['F3']],
    'A5': [NOTES['A2'], NOTES['E3'], NOTES['A3']],
    'C5': [NOTES['C3'], NOTES['G3'], NOTES['C4']],
    'D5': [NOTES['D3'], NOTES['A3'], NOTES['D4']],
    'E5': [NOTES['E3'], NOTES['B3'], NOTES['E4']],
    'G5': [NOTES['G3'], NOTES['D4'], NOTES['G4']],
    # Acordes abiertos / tríadas para la estrofa
    'G': [NOTES['G3'], NOTES['B3'], NOTES['D4']],
    'D': [NOTES['D3'], NOTES['F#3'], NOTES['A3'], NOTES['D4']],
    'Em': [NOTES['E3'], NOTES['G3'], NOTES['B3'], NOTES['E4']],
    'C': [NOTES['C3'], NOTES['E3'], NOTES['G3'], NOTES['C4']],
}

# Estructura de secciones de la canción: (id_seccion, texto_marcador, cantidad_compases)
SECTIONS = [
    ('count_in', "Count-in (2 Compases)", 2),
    ('intro', "Intro - Riff Principal (G Pentatonica)", 4),
    ('verse', "Estrofa 1 (G - D - Em - C)", 8),
    ('prechorus', "Pre-Chorus (A5 - C5 - D5)", 4),
    ('chorus', "Estribillo (G5 - D5 - C5)", 8),
    ('outro', "Remate (F5 - C5 - G5)", 2),
]


def get_drum_events(section_starts, ticks_per_quarter, bar_ticks):
    """Genera la lista de eventos (nota, velocidad, inicio_tick, duracion_ticks) para 01_Drums."""
    events = []
    q = ticks_per_quarter
    e_dur = q // 2
    s_dur = q // 4

    # Count-in (2 compases)
    base = section_starts['count_in']
    for b in range(2):
        for beat in range(4):
            tick = base + b * bar_ticks + beat * q
            vel = 110 if beat == 0 else 90
            events.append((DRUMS['sidestick'], vel, tick, e_dur))

    # Intro (4 compases)
    base = section_starts['intro']
    for b in range(4):
        bar_base = base + b * bar_ticks
        if b == 0:
            events.append((DRUMS['crash'], 115, bar_base, q))
        events.append((DRUMS['kick'], 110, bar_base, q))
        events.append((DRUMS['kick'], 105, bar_base + 2 * q, e_dur))
        events.append((DRUMS['kick'], 95, bar_base + int(2.5 * q), e_dur))
        events.append((DRUMS['snare'], 115, bar_base + q, q))
        events.append((DRUMS['snare'], 115, bar_base + 3 * q, q))
        for e in range(8):
            events.append((DRUMS['ride'], 90, bar_base + e * e_dur, e_dur))

    # Verse (8 compases)
    base = section_starts['verse']
    for b in range(8):
        bar_base = base + b * bar_ticks
        events.append((DRUMS['kick'], 100, bar_base, q))
        events.append((DRUMS['kick'], 95, bar_base + 2 * q, q))
        events.append((DRUMS['snare'], 105, bar_base + q, q))
        events.append((DRUMS['snare'], 105, bar_base + 3 * q, q))
        for e in range(8):
            vel = 85 if e % 2 == 0 else 70
            events.append((DRUMS['hh_closed'], vel, bar_base + e * e_dur, e_dur))

    # Pre-Chorus (4 compases)
    base = section_starts['prechorus']
    for b in range(4):
        bar_base = base + b * bar_ticks
        if b < 2:
            for e in range(8):
                t_pos = bar_base + e * e_dur
                vel_kick = 110 if e % 2 == 0 else 95
                events.append((DRUMS['kick'], vel_kick, t_pos, e_dur))
                tom_note = DRUMS['floor_tom_h'] if e % 2 == 0 else DRUMS['low_tom']
                events.append((tom_note, 90 + b * 10, t_pos, e_dur))
                if e in (2, 6):
                    events.append((DRUMS['snare'], 105, t_pos, e_dur))
        else:
            for s in range(16):
                t_pos = bar_base + s * s_dur
                cresc_vel = min(127, 75 + (b - 2) * 24 + s * 2)
                if s % 2 == 0:
                    events.append((DRUMS['kick'], cresc_vel, t_pos, s_dur))
                if b == 2:
                    t_note = DRUMS['floor_tom_l'] if s % 2 == 0 else DRUMS['low_tom']
                else:
                    if s < 8:
                        t_note = DRUMS['low_tom'] if s % 2 == 0 else DRUMS['mid_tom']
                    else:
                        t_note = DRUMS['high_tom'] if s % 2 == 0 else DRUMS['snare']
                events.append((t_note, cresc_vel, t_pos, s_dur))

    # Chorus (8 compases)
    base = section_starts['chorus']
    for b in range(8):
        bar_base = base + b * bar_ticks
        if b % 4 == 0:
            events.append((DRUMS['crash'], 120, bar_base, q))
        events.append((DRUMS['kick'], 115, bar_base, q))
        events.append((DRUMS['kick'], 110, bar_base + int(1.5 * q), e_dur))
        events.append((DRUMS['kick'], 110, bar_base + 2 * q, q))
        events.append((DRUMS['snare'], 120, bar_base + q, q))
        events.append((DRUMS['snare'], 120, bar_base + 3 * q, q))
        for e in range(8):
            events.append((DRUMS['hh_open'], 95, bar_base + e * e_dur, e_dur))

    # Outro / Remate (2 compases)
    base = section_starts['outro']
    for offset_q in (0, 2):
        tick = base + offset_q * q
        events.append((DRUMS['crash'], 120, tick, q))
        events.append((DRUMS['kick'], 120, tick, q))
        events.append((DRUMS['snare'], 120, tick, q))

    hit_tick = base + bar_ticks
    events.append((DRUMS['crash'], 127, hit_tick, q))
    events.append((DRUMS['kick'], 127, hit_tick, q))
    events.append((DRUMS['snare'], 127, hit_tick, q))

    return events


def get_bass_events(section_starts, ticks_per_quarter, bar_ticks):
    """Genera la lista de eventos (nota, velocidad, inicio_tick, duracion_ticks) para 02_Bass."""
    events = []
    q = ticks_per_quarter
    e_dur = q // 2

    # Intro
    base = section_starts['intro']
    for b in range(4):
        bar_base = base + b * bar_ticks
        events.append((NOTES['G1'], 110, bar_base, q))
        events.append((NOTES['G1'], 100, bar_base + q, q))
        events.append((NOTES['Bb1'], 105, bar_base + 2 * q, e_dur))
        events.append((NOTES['C2'], 105, bar_base + int(2.5 * q), e_dur))
        events.append((NOTES['G1'], 110, bar_base + 3 * q, q))

    # Verse (G - D - Em - C x 2)
    base = section_starts['verse']
    verse_roots = [NOTES['G1'], NOTES['D2'], NOTES['E2'], NOTES['C2']] * 2
    for b, root in enumerate(verse_roots):
        bar_base = base + b * bar_ticks
        for e in range(8):
            vel = 95 if e % 2 == 0 else 80
            events.append((root, vel, bar_base + e * e_dur, e_dur))

    # Pre-Chorus (A - C - D - D)
    base = section_starts['prechorus']
    pc_roots = [NOTES['A1'], NOTES['C2'], NOTES['D2'], NOTES['D2']]
    for b, root in enumerate(pc_roots):
        bar_base = base + b * bar_ticks
        if b < 2:
            events.append((root, 100, bar_base, bar_ticks))
        else:
            for e in range(8):
                events.append((root, 85 + e * 4, bar_base + e * e_dur, e_dur))

    # Chorus (G - D - C - C x 2)
    base = section_starts['chorus']
    chorus_roots = [NOTES['G1'], NOTES['D2'], NOTES['C2'], NOTES['C2']] * 2
    for b, root in enumerate(chorus_roots):
        bar_base = base + b * bar_ticks
        events.append((root, 115, bar_base, q))
        events.append((root, 110, bar_base + q, q))
        events.append((root, 110, bar_base + 2 * q, e_dur))
        events.append((root, 110, bar_base + int(2.5 * q), e_dur))
        events.append((root, 110, bar_base + 3 * q, q))

    # Outro (F - C - G)
    base = section_starts['outro']
    events.append((NOTES['F1'], 120, base, 2 * q))
    events.append((NOTES['C2'], 120, base + 2 * q, 2 * q))
    events.append((NOTES['G1'], 127, base + bar_ticks, q))

    return events


def get_rhythm_guide_events(section_starts, ticks_per_quarter, bar_ticks):
    """Genera los eventos de acordes para 03_Rhythm_Guide_Chords."""
    events = []
    q = ticks_per_quarter
    e_dur = q // 2

    def add_chord(chord_name, start, dur, vel=100):
        for n in CHORDS[chord_name]:
            events.append((n, vel, start, dur))

    # Intro
    base = section_starts['intro']
    for b in range(4):
        bar_base = base + b * bar_ticks
        add_chord('G5_riff', bar_base, q)
        add_chord('G5_riff', bar_base + q, q)
        add_chord('Bb5_riff', bar_base + 2 * q, e_dur)
        add_chord('C5_riff', bar_base + int(2.5 * q), e_dur)
        add_chord('G5_riff', bar_base + 3 * q, q)

    # Verse
    base = section_starts['verse']
    verse_prog = ['G', 'D', 'Em', 'C'] * 2
    for b, ch_name in enumerate(verse_prog):
        bar_base = base + b * bar_ticks
        for beat in range(4):
            add_chord(ch_name, bar_base + beat * q, q, 85)

    # Pre-Chorus
    base = section_starts['prechorus']
    add_chord('A5', base, bar_ticks, 95)
    add_chord('C5', base + bar_ticks, bar_ticks, 100)
    for e in range(8):
        add_chord('D5', base + 2 * bar_ticks + e * e_dur, e_dur, 85 + e * 5)
    for e in range(8):
        add_chord('D5', base + 3 * bar_ticks + e * e_dur, e_dur, 105 + e * 2)

    # Chorus
    base = section_starts['chorus']
    chorus_prog = ['G5', 'D5', 'C5', 'C5'] * 2
    for b, ch_name in enumerate(chorus_prog):
        bar_base = base + b * bar_ticks
        add_chord(ch_name, bar_base, q, 115)
        add_chord(ch_name, bar_base + q, q, 110)
        add_chord(ch_name, bar_base + 2 * q, e_dur, 110)
        add_chord(ch_name, bar_base + int(2.5 * q), e_dur, 110)
        add_chord(ch_name, bar_base + 3 * q, q, 110)

    # Outro
    base = section_starts['outro']
    add_chord('F5', base, 2 * q, 120)
    add_chord('C5', base + 2 * q, 2 * q, 120)
    add_chord('G5', base + bar_ticks, q, 127)

    return events


def get_tracks_definition(section_starts, ticks_per_quarter, bar_ticks):
    """Devuelve la definición completa de las pistas de instrumentos y sus eventos."""
    s_dur = ticks_per_quarter // 4
    return [
        {
            "name": "01_Drums",
            "channel": 9,
            "events": get_drum_events(section_starts, ticks_per_quarter, bar_ticks),
        },
        {
            "name": "02_Bass",
            "channel": 1,
            "events": get_bass_events(section_starts, ticks_per_quarter, bar_ticks),
        },
        {
            "name": "03_Rhythm_Guide_Chords",
            "channel": 2,
            "events": get_rhythm_guide_events(section_starts, ticks_per_quarter, bar_ticks),
        },
        {
            "name": "04_Rhythm_LesPaul_L",
            "channel": 3,
            "events": [(NOTES['G3'], 1, section_starts['intro'], s_dur)],
        },
        {
            "name": "05_Rhythm_Hamer_R",
            "channel": 4,
            "events": [(NOTES['G3'], 1, section_starts['intro'], s_dur)],
        },
        {
            "name": "06_Lead_Guitar_Center",
            "channel": 5,
            "events": [(NOTES['G4'], 1, section_starts['intro'], s_dur)],
        },
        {
            "name": "07_Lead_Vocal_Guide",
            "channel": 6,
            "events": [(NOTES['D4'], 1, section_starts['verse'], s_dur)],
        },
    ]
