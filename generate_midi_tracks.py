import struct

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
        self.events = [] # list of (abs_tick, bytes)
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

def build_project_midi(filename):
    ticks_per_quarter = 480
    bar_ticks = ticks_per_quarter * 4 # 1920 ticks per 4/4 bar

    # 1. Track Conductor / Tempo / Markers
    t_conductor = MidiTrack("00_Tempo_and_Markers")
    # Set Tempo: 80 BPM -> microseconds per quarter = 60,000,000 / 80 = 750,000 (0x0B71B0)
    mpqn = 750000
    t_conductor.add_meta(0, 0x51, struct.pack('>I', mpqn)[1:]) # 3 bytes
    # Time Signature: 4/4 (4, 2 -> 2^2=4, 24 MIDI clocks, 8 32nd notes per 24 clocks)
    t_conductor.add_meta(0, 0x58, bytes([4, 2, 24, 8]))

    # Song markers
    # Pre-roll: 2 bars (Bars 1-2: 0 to 2 * bar_ticks)
    t_conductor.add_marker(0, "Count-in (2 Compases)")
    intro_start = 2 * bar_ticks
    t_conductor.add_marker(intro_start, "Intro - Riff Principal (G Pentatonica)")
    verse_start = intro_start + 4 * bar_ticks # 4 bars of intro
    t_conductor.add_marker(verse_start, "Estrofa 1 (G - D - Em - C)")
    prechorus_start = verse_start + 8 * bar_ticks # 8 bars of verse
    t_conductor.add_marker(prechorus_start, "Pre-Chorus (A5 - C5 - D5)")
    chorus_start = prechorus_start + 4 * bar_ticks # 4 bars of pre-chorus
    t_conductor.add_marker(chorus_start, "Estribillo (G5 - D5 - C5)")
    outro_start = chorus_start + 8 * bar_ticks # 8 bars of chorus
    t_conductor.add_marker(outro_start, "Remate (F5 - C5 - G5)")
    song_end = outro_start + 2 * bar_ticks

    # 2. Track Drums (Channel 9 / 10 in 1-based indexing)
    t_drums = MidiTrack("01_Drums")
    # General MIDI drums:
    # 36: Bass Drum 1
    # 38: Acoustic Snare
    # 42: Closed Hi-Hat
    # 46: Open Hi-Hat
    # 49: Crash Cymbal 1
    # 51: Ride Cymbal 1
    # 37: Side Stick

    drum_ch = 9 # channel 10

    # Count-in (Bars 1 and 2)
    for b in range(2):
        for beat in range(4):
            tick = b * bar_ticks + beat * ticks_per_quarter
            # Accent first beat
            vel = 110 if beat == 0 else 90
            t_drums.add_note(drum_ch, 37, vel, tick, ticks_per_quarter // 2)

    # Intro (Bars 3-6: 4 bars)
    for b in range(4):
        bar_base = intro_start + b * bar_ticks
        # Crash on bar 1 beat 1
        if b == 0:
            t_drums.add_note(drum_ch, 49, 115, bar_base, ticks_per_quarter)
        # Kick on beat 1, beat 3 and 'and' of 3
        t_drums.add_note(drum_ch, 36, 110, bar_base, ticks_per_quarter)
        t_drums.add_note(drum_ch, 36, 105, bar_base + 2 * ticks_per_quarter, ticks_per_quarter // 2)
        t_drums.add_note(drum_ch, 36, 95, bar_base + int(2.5 * ticks_per_quarter), ticks_per_quarter // 2)
        # Snare on 2 and 4
        t_drums.add_note(drum_ch, 38, 115, bar_base + ticks_per_quarter, ticks_per_quarter)
        t_drums.add_note(drum_ch, 38, 115, bar_base + 3 * ticks_per_quarter, ticks_per_quarter)
        # 8th notes on Ride / Hi-hat
        for e in range(8):
            t_drums.add_note(drum_ch, 51, 90, bar_base + e * (ticks_per_quarter // 2), ticks_per_quarter // 2)

    # Verse (Bars 7-14: 8 bars)
    for b in range(8):
        bar_base = verse_start + b * bar_ticks
        # Kick on 1 and 3
        t_drums.add_note(drum_ch, 36, 100, bar_base, ticks_per_quarter)
        t_drums.add_note(drum_ch, 36, 95, bar_base + 2 * ticks_per_quarter, ticks_per_quarter)
        # Snare on 2 and 4
        t_drums.add_note(drum_ch, 38, 105, bar_base + ticks_per_quarter, ticks_per_quarter)
        t_drums.add_note(drum_ch, 38, 105, bar_base + 3 * ticks_per_quarter, ticks_per_quarter)
        # Closed Hi-Hat 8th notes
        for e in range(8):
            vel = 85 if e % 2 == 0 else 70
            t_drums.add_note(drum_ch, 42, vel, bar_base + e * (ticks_per_quarter // 2), ticks_per_quarter // 2)

    # Pre-Chorus (Bars 15-18: 4 bars) - Redoble ininterrumpido y toms en crescendo
    # Bar 0 (A5) & Bar 1 (C5): Patrón tribal/conducción pesada en toms y bombo en negras/corcheas
    # Bar 2 & 3 (D5): Redoble continuo en semicorcheas sobre toms y caja, subiendo tensión hacia el estribillo
    for b in range(4):
        bar_base = prechorus_start + b * bar_ticks
        if b < 2:
            # Floor Tom (41/43) y Low Tom (45) con bombo continuo
            for e in range(8):
                t_pos = bar_base + e * (ticks_per_quarter // 2)
                vel_kick = 110 if e % 2 == 0 else 95
                t_drums.add_note(drum_ch, 36, vel_kick, t_pos, ticks_per_quarter // 2) # Bombo constante
                # Floor tom marcando ritmo tribal
                tom_note = 43 if e % 2 == 0 else 45
                t_drums.add_note(drum_ch, tom_note, 90 + b * 10, t_pos, ticks_per_quarter // 2)
                # Golpe de caja acentuado en 2 y 4
                if e == 2 or e == 6:
                    t_drums.add_note(drum_ch, 38, 105, t_pos, ticks_per_quarter // 2)
        else:
            # Redoble ininterrumpido sobre D5 (Floor Tom -> Mid Tom -> Snare crescendo)
            # 16th notes fill continuo
            for s in range(16):
                t_pos = bar_base + s * (ticks_per_quarter // 4)
                cresc_vel = min(127, 75 + (b - 2) * 24 + s * 2)
                # Bombo continuo en corcheas
                if s % 2 == 0:
                    t_drums.add_note(drum_ch, 36, cresc_vel, t_pos, ticks_per_quarter // 4)
                # Rotación de toms y caja para el redoble
                if b == 2:
                    # Alternancia Floor Tom (41) y Low Tom (45)
                    t_note = 41 if s % 2 == 0 else 45
                else:
                    # Compás final hacia el chorus: Mid Tom (47), High Tom (50) y Snare (38)
                    if s < 8:
                        t_note = 45 if s % 2 == 0 else 47
                    else:
                        t_note = 50 if s % 2 == 0 else 38
                t_drums.add_note(drum_ch, t_note, cresc_vel, t_pos, ticks_per_quarter // 4)

    # Chorus (Bars 19-26: 8 bars)
    for b in range(8):
        bar_base = chorus_start + b * bar_ticks
        if b % 4 == 0:
            t_drums.add_note(drum_ch, 49, 120, bar_base, ticks_per_quarter) # Crash
        t_drums.add_note(drum_ch, 36, 115, bar_base, ticks_per_quarter)
        t_drums.add_note(drum_ch, 36, 110, bar_base + int(1.5 * ticks_per_quarter), ticks_per_quarter // 2)
        t_drums.add_note(drum_ch, 36, 110, bar_base + 2 * ticks_per_quarter, ticks_per_quarter)
        t_drums.add_note(drum_ch, 38, 120, bar_base + ticks_per_quarter, ticks_per_quarter)
        t_drums.add_note(drum_ch, 38, 120, bar_base + 3 * ticks_per_quarter, ticks_per_quarter)
        for e in range(8):
            t_drums.add_note(drum_ch, 46, 95, bar_base + e * (ticks_per_quarter // 2), ticks_per_quarter // 2) # Open HH

    # Outro / Remate (Bars 27-28)
    # Bar 27: F5 (beat 1), C5 (beat 3)
    t_drums.add_note(drum_ch, 49, 120, outro_start, ticks_per_quarter)
    t_drums.add_note(drum_ch, 36, 120, outro_start, ticks_per_quarter)
    t_drums.add_note(drum_ch, 38, 120, outro_start, ticks_per_quarter)

    t_drums.add_note(drum_ch, 49, 120, outro_start + 2 * ticks_per_quarter, ticks_per_quarter)
    t_drums.add_note(drum_ch, 36, 120, outro_start + 2 * ticks_per_quarter, ticks_per_quarter)
    t_drums.add_note(drum_ch, 38, 120, outro_start + 2 * ticks_per_quarter, ticks_per_quarter)

    # Bar 28: G5 hit on beat 1 then abrupt silence
    t_drums.add_note(drum_ch, 49, 127, outro_start + bar_ticks, ticks_per_quarter)
    t_drums.add_note(drum_ch, 36, 127, outro_start + bar_ticks, ticks_per_quarter)
    t_drums.add_note(drum_ch, 38, 127, outro_start + bar_ticks, ticks_per_quarter)

    # 3. Track Bass (Channel 1, 0-indexed)
    t_bass = MidiTrack("02_Bass")
    bass_ch = 1
    # Intro riff notes in G: G1=31, Bb1=34, C2=36, D2=38, F2=41
    # For simplicity and solid low-end foundation:
    for b in range(4):
        bar_base = intro_start + b * bar_ticks
        t_bass.add_note(bass_ch, 31, 110, bar_base, ticks_per_quarter) # G1
        t_bass.add_note(bass_ch, 31, 100, bar_base + ticks_per_quarter, ticks_per_quarter)
        t_bass.add_note(bass_ch, 34, 105, bar_base + 2 * ticks_per_quarter, ticks_per_quarter // 2) # Bb
        t_bass.add_note(bass_ch, 36, 105, bar_base + int(2.5 * ticks_per_quarter), ticks_per_quarter // 2) # C
        t_bass.add_note(bass_ch, 31, 110, bar_base + 3 * ticks_per_quarter, ticks_per_quarter) # G1

    # Verse (G - D - Em - C x 2)
    verse_chords = [31, 38, 40, 36] * 2 # G1, D2, E2, C2
    for b, root in enumerate(verse_chords):
        bar_base = verse_start + b * bar_ticks
        # 8th notes driving
        for e in range(8):
            t_bass.add_note(bass_ch, root, 95 if e % 2 == 0 else 80, bar_base + e * (ticks_per_quarter // 2), ticks_per_quarter // 2)

    # Pre-Chorus: A (33), C (36), D (38), D (38)
    pc_chords = [33, 36, 38, 38]
    for b, root in enumerate(pc_chords):
        bar_base = prechorus_start + b * bar_ticks
        if b < 2:
            t_bass.add_note(bass_ch, root, 100, bar_base, bar_ticks)
        else:
            for e in range(8):
                t_bass.add_note(bass_ch, root, 85 + e * 4, bar_base + e * (ticks_per_quarter // 2), ticks_per_quarter // 2)

    # Chorus: G (31), D (38), C (36), C (36) x 2
    chorus_chords = [31, 38, 36, 36] * 2
    for b, root in enumerate(chorus_chords):
        bar_base = chorus_start + b * bar_ticks
        t_bass.add_note(bass_ch, root, 115, bar_base, ticks_per_quarter)
        t_bass.add_note(bass_ch, root, 110, bar_base + ticks_per_quarter, ticks_per_quarter)
        t_bass.add_note(bass_ch, root, 110, bar_base + 2 * ticks_per_quarter, ticks_per_quarter // 2)
        t_bass.add_note(bass_ch, root, 110, bar_base + int(2.5 * ticks_per_quarter), ticks_per_quarter // 2)
        t_bass.add_note(bass_ch, root, 110, bar_base + 3 * ticks_per_quarter, ticks_per_quarter)

    # Outro: F (29), C (36), G (31)
    t_bass.add_note(bass_ch, 29, 120, outro_start, 2 * ticks_per_quarter)
    t_bass.add_note(bass_ch, 36, 120, outro_start + 2 * ticks_per_quarter, 2 * ticks_per_quarter)
    t_bass.add_note(bass_ch, 31, 127, outro_start + bar_ticks, ticks_per_quarter)

    # 4. Track Rhythm Guide Chords (Channel 2, 0-indexed)
    t_guide = MidiTrack("03_Rhythm_Guide_Chords")
    guide_ch = 2

    # Chords in MIDI:
    # G5: G3=55, D4=62, G4=67
    # D5: D3=50, A3=57, D4=62
    # E5: E3=52, B3=59, E4=64
    # C5: C3=48, G3=55, C4=60
    # A5: A2=45, E3=52, A3=57
    # F5: F2=41, C3=48, F3=53

    def play_chord(notes, start, dur, vel=100):
        for n in notes:
            t_guide.add_note(guide_ch, n, vel, start, dur)

    # Intro (Power Chords on Riff accents)
    for b in range(4):
        bar_base = intro_start + b * bar_ticks
        play_chord([55, 62], bar_base, ticks_per_quarter)
        play_chord([55, 62], bar_base + ticks_per_quarter, ticks_per_quarter)
        play_chord([58, 65], bar_base + 2 * ticks_per_quarter, ticks_per_quarter // 2) # Bb5
        play_chord([60, 67], bar_base + int(2.5 * ticks_per_quarter), ticks_per_quarter // 2) # C5
        play_chord([55, 62], bar_base + 3 * ticks_per_quarter, ticks_per_quarter)

    # Verse (G - D - Em - C x 2)
    chords_map = {
        'G': [55, 59, 62],
        'D': [50, 54, 57, 62],
        'Em': [52, 55, 59, 64],
        'C': [48, 52, 55, 60]
    }
    verse_prog = ['G', 'D', 'Em', 'C', 'G', 'D', 'Em', 'C']
    for b, ch_name in enumerate(verse_prog):
        bar_base = verse_start + b * bar_ticks
        c_notes = chords_map[ch_name]
        for beat in range(4):
            play_chord(c_notes, bar_base + beat * ticks_per_quarter, ticks_per_quarter, 85)

    # Pre-Chorus: A5, C5, D5, D5
    play_chord([45, 52, 57], prechorus_start, bar_ticks, 95) # A5
    play_chord([48, 55, 60], prechorus_start + bar_ticks, bar_ticks, 100) # C5
    for e in range(8):
        play_chord([50, 57, 62], prechorus_start + 2 * bar_ticks + e * (ticks_per_quarter // 2), ticks_per_quarter // 2, 85 + e * 5)
    for e in range(8):
        play_chord([50, 57, 62], prechorus_start + 3 * bar_ticks + e * (ticks_per_quarter // 2), ticks_per_quarter // 2, 105 + e * 2)

    # Chorus: G5, D5, C5, C5 x 2
    chorus_prog = [
        [55, 62, 67], # G5
        [50, 57, 62], # D5
        [48, 55, 60], # C5
        [48, 55, 60]  # C5
    ] * 2
    for b, c_notes in enumerate(chorus_prog):
        bar_base = chorus_start + b * bar_ticks
        play_chord(c_notes, bar_base, ticks_per_quarter, 115)
        play_chord(c_notes, bar_base + ticks_per_quarter, ticks_per_quarter, 110)
        play_chord(c_notes, bar_base + 2 * ticks_per_quarter, ticks_per_quarter // 2, 110)
        play_chord(c_notes, bar_base + int(2.5 * ticks_per_quarter), ticks_per_quarter // 2, 110)
        play_chord(c_notes, bar_base + 3 * ticks_per_quarter, ticks_per_quarter, 110)

    # Outro: F5, C5, G5
    play_chord([41, 48, 53], outro_start, 2 * ticks_per_quarter, 120) # F5
    play_chord([48, 55, 60], outro_start + 2 * ticks_per_quarter, 2 * ticks_per_quarter, 120) # C5
    play_chord([55, 62, 67], outro_start + bar_ticks, ticks_per_quarter, 127) # G5

    # 5. Pistas de plantilla/marcador para las Guitarras (Tracks para Cubase)
    t_lespaul = MidiTrack("04_Rhythm_LesPaul_L")
    # A single soft note at intro_start so Cubase creates the lane with length
    t_lespaul.add_note(3, 55, 1, intro_start, ticks_per_quarter // 4)

    t_hamer = MidiTrack("05_Rhythm_Hamer_R")
    t_hamer.add_note(4, 55, 1, intro_start, ticks_per_quarter // 4)

    t_lead = MidiTrack("06_Lead_Guitar_Center")
    t_lead.add_note(5, 67, 1, intro_start, ticks_per_quarter // 4)

    t_vocal = MidiTrack("07_Lead_Vocal_Guide")
    t_vocal.add_note(6, 62, 1, verse_start, ticks_per_quarter // 4) # D4 marker

    # Assemble Standard MIDI File Format 1
    tracks = [t_conductor, t_drums, t_bass, t_guide, t_lespaul, t_hamer, t_lead, t_vocal]
    num_tracks = len(tracks)

    # Header chunk: MThd, length=6, format=1, num_tracks, division
    header = b'MThd' + struct.pack('>IHHH', 6, 1, num_tracks, ticks_per_quarter)

    with open(filename, 'wb') as f:
        f.write(header)
        for t in tracks:
            f.write(t.build())

    print(f"Archivo MIDI generado exitosamente: {filename} ({num_tracks} pistas)")

if __name__ == '__main__':
    build_project_midi('c:/repos/hard_song/cubase/hard_song_tracks.mid')
