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

> [!TIP]
> **El secreto del sonido "Pared de Guitarras" (Wall of Sound):**
> No copies y pegues la misma pista a la izquierda y derecha. Graba dos tomas reales: una con la Les Paul y otra con la Hamer. Las sutiles diferencias humanas y el contraste de timbres entre caoba y arce crearán ese sonido estéreo gigantesco clásico de los discos de rock de los 80s y 90s.

---

## 4. Batería en Cubase con Groove Agent SE

Cubase incluye el plugin **Groove Agent SE**:
1. Agrega una pista de instrumento (*Project > Add Track > Instrument*) y elige **Groove Agent SE**.
2. Carga un kit acústico de rock (ejemplo: *The Rock Toolkit*, *Raw Power Kit* o *Rock Standard*).
3. Puedes arrastrar patrones MIDI de rock a 80 BPM directamente al secuenciador para tener una base de batería real sobre la cual practicar y grabar los riffs de [tabs.md](file:///c:/repos/hard_song/tabs.md).
