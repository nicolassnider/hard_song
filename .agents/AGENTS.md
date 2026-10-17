# Sistema de Agentes: Producción Musical "Sigo de Pie" (Hard Rock Old School)

Este documento define la **constitución técnica inquebrantable**, las restricciones del proyecto y la arquitectura operativa que todo agente de IA (principal o subagente) debe respetar en este repositorio.

---

## 1. Identidad e Invariantes Técnicos del Proyecto

Cualquier propuesta compositiva, arreglo o código generado debe cumplir sin excepciones con estos límites:

- **Estilo:** Hard Rock Old School / Rock Pesado clásico (referencias: Whitesnake, Alice in Chains, Danzig, Pappo's Blues, Riff).
- **Tonalidad Base:** Sol menor ($G$ minor / Pentatónica menor de Sol).
- **Tempo Obligatorio:** **80 BPM** ($4/4$, ritmo arrastrado y pesado de Hard Rock Balada).
- **Rango Vocal Inquebrantable:** **D2 a D#4** (Registro de Barítono / Bajo natural).
  - *Graves / Tensión:* **D2 – B2** (resonancia de pecho, estrofas oscuras).
  - *Comodidad Melódica:* **G2 – B3** (fraseo claro y cálido en versos).
  - *Clímax / Belting:* **C4 – D4** (ganchos de estribillo con grano).
  - *Cúspide Máxima:* **D#4 (Eb4)** (reservado para 1 o 2 impactos culminantes).
  - *Restricción:* **PROHIBIDO** componer melodías continuas por encima de D4 o notas que superen D#4.
- **Hardware & Instrumentación Disponible:**
  - *Guitarra Rítmica L (100% Izquierda):* Epiphone Les Paul Pro (cuerpo de caoba, humbuckers Alnico Classic Pro).
  - *Guitarra Rítmica R (100% Derecha):* Hamer Superstrat (mástil de arce, Seymour Duncan en puente, single coil mástil).
  - *Amplificación & Interfaz USB:* Line 6 Spider V 20 (Presets Brit 800 / Plexi vía Spider Remote).
  - *DAW:* Steinberg Cubase (plantilla multitrack de 8 pistas).

---

## 2. Arquitectura de Skills del Agente (División de Responsabilidades)

Para optimizar el uso de contexto y evitar alucinaciones, los procedimientos técnicos detallados se encuentran encapsulados en **Skills de Antigravity**. El agente debe consultar y aplicar el skill correspondiente según la tarea:

| Skill | Ubicación | Cuándo se Activa |
| :--- | :--- | :--- |
| **`vocal-arranger`** | [.agents/skills/vocal-arranger/SKILL.md](file:///c:/repos/hard_song/.agents/skills/vocal-arranger/SKILL.md) | Composición y corrección de letras en español, prosodia, métrica rítmica, armonización en octavas (D3) y coros raspados laterales. |
| **`tone-crafting`** | [.agents/skills/tone-crafting/SKILL.md](file:///c:/repos/hard_song/.agents/skills/tone-crafting/SKILL.md) | Modelado de amplificadores en Spider Remote (Brit 800, Screamer, cabinas), dinámica de potenciómetros (limpiar a 4-5 en estrofas) y calibración de pastillas. |
| **`cubase-workflow`** | [.agents/skills/cubase-workflow/SKILL.md](file:///c:/repos/hard_song/.agents/skills/cubase-workflow/SKILL.md) | Ruteo multitrack en Cubase, buffers ASIO, curvas de EQ para barítono (HPF en 55-65 Hz, dip en 220 Hz, realce en 3 kHz), tape delay 1/8 y mezcla. |
| **`midi-generator`** | [.agents/skills/midi-generator/SKILL.md](file:///c:/repos/hard_song/.agents/skills/midi-generator/SKILL.md) | Edición de pistas MIDI, ejecución de `generate_midi_tracks.py` y validación automatizada de secuencias. |

---

## 3. Subagentes y Roles Especializados

Cuando el usuario solicite tareas complejas o multi-etapa, el agente orquestador puede invocar subagentes especializados utilizando los siguientes roles predefinidos:

- **`@vocal-coach` (Rol: Vocal Coach & Lyricist):**
  - *Enfoque:* Perfeccionamiento de la lírica en español, rimas, acentos prosódicos y garantía de que ninguna nota exceda D#4.
- **`@guitar-tech` (Rol: Guitar Tech & Tone Engineer):**
  - *Enfoque:* Arreglos de guitarra, digitaciones en tablatura ([tabs.md](file:///c:/repos/hard_song/tabs.md)), respuesta del potenciómetro de volumen y compensación de timbres entre caoba y arce.
- **`@audio-engineer` (Rol: DAW & Mixing Specialist):**
  - *Enfoque:* Estructura de ganancia, ruteo de buses estéreo en Cubase, filtrado HPF a 35 Hz, compresión óptica y paneo 100% L / 100% R.
- **`@midi-master` (Rol: MIDI & Code Specialist):**
  - *Enfoque:* Automatización en Python con `generate_midi_tracks.py`, cálculo de ticks y marcas de tiempo a 80 BPM.

---

## 4. Control de Calidad Obligatorio (Quality Gate)

Siempre que se efectúen cambios en la estructura de compases, tempos o melodías MIDI:
1. Recompilar el archivo: `python generate_midi_tracks.py`.
2. Ejecutar la auditoría automática: `python .agents/skills/midi-generator/scripts/verify_midi.py`.
3. El agente **no dará por concluida la tarea** si el script de verificación reporta algún fallo en tempo, compás o rango vocal.
