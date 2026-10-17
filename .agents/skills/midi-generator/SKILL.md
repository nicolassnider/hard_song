---
name: midi-generator
description: >-
  Procedimiento técnico para modificar, compilar y auditar pistas MIDI multitrack
  del proyecto utilizando generate_midi_tracks.py y el script de verificación.
---

# MIDI Generator & Quality Gate Runbook

Este skill define el procedimiento estricto para manipular las secuencias MIDI del proyecto musical sin romper la compatibilidad con Steinberg Cubase ni violar las reglas de tempo, compás y tesitura vocal.

---

## 1. Especificaciones Invariables del Archivo MIDI

- **Formato:** Standard MIDI File Format 1 (Multi-track con pista de tempo/conductor separada).
- **Resolución temporal:** 480 ticks por negra (`ticks_per_quarter = 480`).
- **Compás:** 4/4 (1920 ticks por compás completo).
- **Tempo estricto:** **80 BPM** (750,000 microsegundos por negra, `mpqn = 750000`).
- **Canal de Batería:** Canal 10 (índice 9 en Python / 0x09).
- **Pistas estándar (Orden obligatorio):**
  1. `00_Tempo_and_Markers` (Metadatos, tempo 80 BPM, marcadores de sección).
  2. `01_Drums` (Batería GM: Bombo 36, Caja 38, Charles 42/46, Toms 41/43/45/47, Platos 49/51).
  3. `02_Bass` (Línea de bajo en Sol menor).
  4. `03_Rhythm_Guide_Chords` (Armonía completa con voicings clásicos).
  5. `04_Rhythm_LesPaul_L` (Marcador/carril para guitarra rítmica izquierda).
  6. `05_Rhythm_Hamer_R` (Marcador/carril para guitarra rítmica derecha).
  7. `06_Lead_Guitar_Center` (Carril de guitarra líder / solo).
  8. `07_Lead_Vocal_Guide` (Melodía guía vocal restringida estrictamente a **D2 [38] - D#4 [63]**).

---

## 2. Flujo de Trabajo para el Agente

Cuando se requiera modificar compases, arreglos o patrones:

1. **Editar [tones.py](file:///c:/repos/hard_song/tones.py) (o [generate_midi_tracks.py](file:///c:/repos/hard_song/generate_midi_tracks.py) si se modifica el motor):**
   - Los tonos (`NOTES`), acordes (`CHORDS`), mapeo de batería (`DRUMS`), secciones (`SECTIONS`) y patrones musicales están desacoplados en [tones.py](file:///c:/repos/hard_song/tones.py).
   - Asegurar que cualquier nota agregada a la pista vocal `07_Lead_Vocal_Guide` se mantenga dentro del rango MIDI 38 a 63.
   - Respetar los compases y marcadores de sección (Intro: compás 3-6, Estrofa: 7-14, Pre-Chorus: 15-18, Estribillo: 19-26, Remate: 27-28).
2. **Compilar el archivo MIDI:**
   Ejecutar en la terminal:
   ```powershell
   python generate_midi_tracks.py
   ```
3. **Ejecutar el Control de Calidad Obligatorio:**
   Antes de confirmar al usuario que los cambios están listos, correr el script de verificación:
   ```powershell
   python .agents/skills/midi-generator/scripts/verify_midi.py
   ```
4. **Verificar salida:**
   - Si el script devuelve `=> APROBADO: Cumple con todas las directrices de producción.`, el cambio es válido.
   - Si falla, revisar inmediatamente el reporte de notas o tempo y corregir el código.
