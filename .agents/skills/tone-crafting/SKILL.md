---
name: tone-crafting
description: >-
  Calibración de tonos de guitarra en Line 6 Spider V 20 (Spider Remote),
  dinámica de pastillas, compensación de impedancia y emparejamiento estéreo
  entre Epiphone Les Paul Pro y Hamer Superstrat.
---

# Tone Crafting & Hardware Engineering Runbook

Este skill define la ingeniería de audio de guitarra y modelado físico para el proyecto, aprovechando el amplificador **Line 6 Spider V 20** y la combinación estéreo de dos maderas y arquitecturas de pastillas diferentes.

---

## 1. Asignación Estéreo y Carácter de Guitarras

Para lograr el sonido masivo del Hard Rock Old School británico/argentino (Riff, Pappo, Zeppelin, Sabbath):

```text
       CANAL IZQUIERDO (100% L)                       CANAL DERECHO (100% R)
  ┌────────────────────────────────┐            ┌────────────────────────────────┐
  │ Epiphone Les Paul Pro          │            │ Hamer Superstrat               │
  │ • Cuerpo: Caoba sólida         │            │ • Mástil: Arce (Snap/Ataque)   │
  │ • Pastilla: Alnico Classic Pro │            │ • Pastilla: Seymour Duncan     │
  │ • Carácter: Grave, denso, peso │            │ • Carácter: Mordida, armónicos │
  │ • Preset: Brit 800 + Greenback │            │ • Preset: Brit 800 + V30       │
  └────────────────────────────────┘            └────────────────────────────────┘
```

---

## 2. Presets Oficiales en Line 6 Spider Remote

### Preset 1: Rítmica Pesada Les Paul (100% L)
- **Amp Model:** Brit 800 (Marshall JCM800).
- **Cab:** 4x12 Greenback 25.
- **Drive / Gain:** 6.5 – 6.8.
- **EQ:** Bass 5.0 | Mid 8.0 | Treble 5.5 | Presence 6.0.
- **Booster / Stomp:** Screamer (Drive 1.8, Tone 6.0, Level 7.8) para apretar la respuesta del transitorio.
- **Dinámica:** Pote de volumen al 10 en Riff/Estribillo; bajar a **4–5** en estrofas para limpiar a *crunch* clásico.

### Preset 2: Rítmica Definida Hamer (100% R)
- **Amp Model:** Brit 800.
- **Cab:** 4x12 Vintage 30 (mayor dispersión y corte en agudos).
- **Drive / Gain:** 6.2.
- **EQ:** Bass 6.0 | Mid 7.0 | Treble 5.0 | Presence 4.8 (compensar el brillo natural del arce).
- **Estrofa melódica:** Cambiar a la Single Coil angulada del mástil para campaneo cristalino.

### Preset 3: Lead Solo (Centro)
- **Drive:** 6.0 + Screamer al frente (Drive 2.5, Tone 5.8, Level 8.2).
- **EQ:** Mid 8.0 – 8.5 (corte total de mezcla).
- **Delay:** Tape Delay / Analog Echo sincronizado a corchea con puntillo o ~375ms (Mix 22%, Feedback 3–4 repeticiones).
- **Reverb:** Plate Reverb (Mix 25%).

---

## 3. Protocolo de Verificación de Audio
1. **Verificación de Fase en Mono:** En Cubase, pulsar el botón "Mono" en el bus Master. Si las guitarras pierden cuerpo o cancelan frecuencias fundamentales en 200–500 Hz, invertir la fase (Phase Invert Ø) en uno de los canales.
2. **Puerta de Ruido (Noise Gate):** Umbral suave en Spider Remote para eliminar el zumbido de bobinas sin comerse el decaimiento natural de los acordes sostenidos.
