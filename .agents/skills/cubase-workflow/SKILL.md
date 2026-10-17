---
name: cubase-workflow
description: >-
  Procedimiento de ruteo multitrack en Steinberg Cubase, configuración ASIO
  para Line 6 Spider V 20, tratamiento de voz de barítono y mezcla Old School.
---

# Cubase Workflow & Studio Production Runbook

Este skill cubre la configuración de sesión, ruteo de buses, procesamiento de voz de barítono y mezcla analógica en **Steinberg Cubase** usando el **Line 6 Spider V 20** como interfaz de audio USB.

---

## 1. Configuración de Sesión y Motor ASIO

- **Controlador:** *Line 6 Spider V ASIO* o *Yamaha Steinberg USB ASIO*.
- **Buffer Size:** 128 o 256 samples para latencia imperceptible durante la monitorización directa.
- **Formato de Grabación:** 24-bit / 44.1 kHz o 48 kHz WAV.
- **Tempo:** 80 BPM con compás 4/4 y 2 compases de cuenta previa (*Count-in / Pre-roll*).

---

## 2. Matriz de Pistas y Paneo Estricto

| Pista | Tipo | Paneo | Rol y Procesamiento |
| :--- | :--- | :--- | :--- |
| `01_Rhythm_LesPaul` | Audio Mono | **100% L** | Caoba, cuerpo cálido. HPF a 35 Hz. Volumen al 5 en estrofa. |
| `02_Rhythm_Hamer` | Audio Mono | **100% R** | Mástil arce + Duncan. HPF a 35 Hz. Single coil en versos. |
| `03_Lead_Guitar` | Audio Mono | **Centro** | Solos con Screamer + Tape Delay (~375ms, 20% mix). |
| `04_Drums` | VST | **Centro** | Groove Agent SE (*Rock Kit*), redoble continuo en toms en Pre-Chorus. |
| `05_Bass` | Audio | **Centro** | Fundamental en Sol menor. HPF a 35 Hz, sidechain suave con bombo. |
| `06_Lead_Vocal` | Audio Mono | **Centro** | Barítono (D2–D#4). HPF en 55–65 Hz, dip en 220 Hz, boost en 3 kHz. |
| `07_Vocal_OctDown`| Audio Mono | **Centro** | Octava inferior en D3 durante el estribillo. |
| `08_Backing_Vocals`| Audio St. | **L 50% / R 50%** | Gritos rasgados en acordes de transición (C5 / D5). |

---

## 3. Cadena de Procesamiento para Voz de Barítono (D2 – D#4)

1. **High-Pass Filter (HPF):**
   - Configurar el corte entre **55 Hz y 65 Hz** (pendiente 18 dB/oct).
   - *Nunca* colocarlo en 80–100 Hz porque se destruye la nota fundamental D2 (73.4 Hz).
2. **Corte de Proximidad / Enlodamiento:**
   - Atenuar 1.5 a 2.5 dB en forma de campana en **200 Hz – 280 Hz** para despejar el espacio del bajo.
3. **Presencia y Corte de Distorsión:**
   - Realce suave de campana ancha entre **2.8 kHz y 4.2 kHz** para que la voz corte la pared de guitarras distorsionadas.
4. **Dinámica:**
   - Compresor estilo FET o VCA (ratio 4:1, ataque medio-rápido, release 100ms) para contener los picos en el estribillo.
5. **Efectos de Época:**
   - **Estrofas:** Slapback Tape Delay a 1/8 con realimentación al mínimo y mezcla al 12–15%.
   - **Estribillo:** Reverb de Placas (Plate) cálida y apertura estéreo.

---

## 4. Limpieza del Bus Maestro
- Aplicar filtro paso alto a **35 Hz** (24 dB/oct) en las pistas de guitarras y bajo antes de entrar a la compresión del bus master para evitar que los infrasonidos consuman el *headroom* del master.
