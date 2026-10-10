# Guía de Grabación y Configuración: Cubase + Line 6 Spider V 20

Tener **Cubase** junto con el **Line 6 Spider V 20** convierte tu amplificador directamente en una **interfaz de audio USB de baja latencia**. Ya no necesitas micrófonos ni tarjetas de sonido externas adicionales para maquetar y grabar la canción con calidad de estudio.

---

## 1. Conexión y Configuración Inicial

### A. Conectar el amplificador a la PC
1. Conecta el Spider V 20 a tu computadora mediante el puerto USB trasero.
2. Asegúrate de tener instalado el **Line 6 Driver (ASIO)** para Windows (puedes descargarlo desde Line 6 si Windows no lo detecta automáticamente).

### B. Configurar el motor de audio en Cubase
1. Abre Cubase y crea un **Empty Project** (Proyecto Vacío).
2. Ve al menú superior: **Studio (Estudio) > Studio Setup (Configuración de Estudio)**.
3. En la sección **Audio System**, selecciona como controlador ASIO: **Line 6 Spider V ASIO** (o *Yamaha Steinberg USB ASIO* / *Line 6 ASIO Driver*).
4. Configura el buffer a **128 o 256 samples** para tener latencia imperceptible al tocar.

### C. Conexiones de Entrada/Salida (Buses)
1. Presiona la tecla **F4** (o ve a *Studio > Audio Connections*).
2. **Inputs (Entradas):** Comprueba que haya un bus estéreo o mono asignado a las entradas del Spider V (Input 1 / Input 2).
3. **Outputs (Salidas):** Asigna la salida principal a donde tengas conectados tus audífonos o altavoces (puedes escuchar directamente por la salida de audífonos del Spider V 20 o por tu PC).

---

## 2. Ajustes del Proyecto para la Canción

*   **Tempo:** Configura el tempo del proyecto en la barra de transporte a **80 BPM** (el punto dulce de nuestra balada de hard rock).
*   **Compás:** **4/4**.
*   **Metrónomo / Click:** Actívalo (tecla **C**) con un compás de cuenta previa (*Pre-roll* o *Count-in* de 2 compases) para entrar a tiempo en el riff.

---

## 3. Plantilla de Pistas para el Proyecto (Multitrack Hard Rock)

Crea las siguientes pistas de audio (*Project > Add Track > Audio*):

| Nombre de Pista | Tipo | Paneo (L/R) | Instrumento / Rol |
| :--- | :--- | :--- | :--- |
| **01_Rhythm_LesPaul** | Audio Mono/Stereo | **100% Izquierda (Hard L)** | Epiphone Les Paul Pro: Tono Brit 800 pesado para el riff y base rítmica de la estrofa. |
| **02_Rhythm_Hamer** | Audio Mono/Stereo | **100% Derecha (Hard R)** | Hamer (Seymour Duncan): Tono Brit 800 para doblar el riff, y Single Coil para arpegios en estrofa. |
| **03_Lead_Guitar** | Audio Mono | **Centro (Center)** | Solos y fraseos melódicos (usando el preset Lead con Overdrive + Delay). |
| **04_Drums** | Instrumento VST | **Centro** | Batería acústica de rock con **Groove Agent SE** (incluido gratis en Cubase). |
| **05_Bass** | Audio o Instrumento | **Centro** | Línea de bajo siguiendo las fundamentales ($G - D - E - C$). |
| **06_Lead_Vocal** | Audio Mono | **Centro** | Voz principal (Rango D2 - D#4). |
| **07_Backing_Vocals** | Audio Mono/Stereo | **Pan L/R (40% - 60%)** | Coros y doblajes para dar amplitud en el estribillo. |

> [!TIP]
> **El secreto del sonido "Pared de Guitarras" (Wall of Sound):**
> No copies y pegues la misma pista a la izquierda y derecha. Graba dos tomas reales: una con la Les Paul y otra con la Hamer. Las sutiles diferencias humanas y el contraste de timbres entre caoba y arce crearán ese sonido estéreo gigantesco clásico de los discos de rock de los 80s y 90s.

---

## 4. Grabación y Mezcla de Voz (Rango D2 – D#4)

Al ser una voz con registro grave/barítono, el tratamiento en Cubase debe equilibrar el peso cálido sin enturbiar la mezcla con el bajo y las guitarras:

1. **Filtro Paso Alto (High-Pass / Low Cut):**
   - Tu nota más baja es **D2 (~73.4 Hz)**.
   - Ajusta el corte pasa-altos entre **50 Hz y 65 Hz** (no en los 80-100 Hz habituales de tenores) para no cortar las frecuencias fundamentales de tus notas más graves.
2. **Control de Proximidad / Enlodamiento (Muddy Range):**
   - Aplica un filtro de campana suave atenuando 1 a 2 dB entre **180 Hz y 280 Hz** para limpiar el efecto de proximidad del micrófono y dejar respirar el bajo ($G - D - Em - C$).
3. **Presencia y Mordida Rockera:**
   - Realza suavemente entre **2.5 kHz y 4.5 kHz** para que la voz corte la distorsión de las guitarras y el grano rasgado suene al frente.
4. **Compresión:**
   - Usa un compresor tipo FET (estilo 1176 rápido) o el compresor integrado de Cubase con ratio 4:1 para domar los saltos dinámicos entre los susurros/versos graves y la pegada del estribillo en D4.

---

## 5. Batería en Cubase con Groove Agent SE

Cubase incluye el plugin **Groove Agent SE**:
1. Agrega una pista de instrumento (*Project > Add Track > Instrument*) y elige **Groove Agent SE**.
2. Carga un kit acústico de rock (ejemplo: *The Rock Toolkit*, *Raw Power Kit* o *Rock Standard*).
3. Puedes arrastrar patrones MIDI de rock a 80 BPM directamente al secuenciador para tener una base de batería real sobre la cual practicar y grabar los riffs de [tabs.md](file:///c:/repos/hard_song/tabs.md).

