# Metrónomo

Aplicación de escritorio para músicos que permite practicar ritmo y mantener un tempo constante de forma simple y visual.

## Descripción breve

Pulse es un metrónomo digital desarrollado en Python con PyQt6. Su objetivo es ofrecer una herramienta clara y eficaz para practicar tempo, subdivisiones y pulso musical sin depender de un dispositivo externo.

La aplicación permite ajustar el BPM, cambiar el compás, controlar el volumen y visualizar el pulso actual de forma intuitiva en una interfaz de escritorio.

## Características principales

- Control de BPM con rango configurable
- Inicio y pausa del metrónomo
- Cambio rápido de tempo mediante botones y slider
- Diferentes compases y subdivisiones
- Indicador visual del beat actual
- Sonido de clic con acento en el primer tiempo
- Ajuste de volumen
- Interfaz de usuario intuitiva y enfocada en la práctica musical
- Generación automática de sonidos del metrónomo en la primera ejecución

## Tecnologías utilizadas

- Python
- PyQt6
- Qt Multimedia
- Archivos WAV generados localmente para los clics del metrónomo

## Requisitos previos

Antes de ejecutar el proyecto, asegúrate de contar con:

- Python 3.x instalado
- Pip disponible en el entorno de Python
- Dependencias del proyecto instaladas

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/hugenri/metronome-app.git
cd metronome-app
```

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

> El proyecto actual define la siguiente dependencia en [requirements.txt](requirements.txt):
>
> ```text
> PyQt6>=6.7
> ```

## Cómo ejecutar la aplicación en modo desarrollo

Desde la raíz del proyecto, ejecuta:

```bash
python main.py
```

La primera ejecución crea automáticamente los archivos de audio del metrónomo dentro de la carpeta `resources` si no existen:

```text
resources/accent.wav
resources/beat.wav
```

## Cómo compilar/generar la aplicación para escritorio

Actualmente el proyecto no incluye un proceso de empaquetado definido ni un comando de compilación configurado dentro del repositorio.

Si deseas generar una versión ejecutable para escritorio, debes configurar la herramienta de empaquetado que prefieras, por ejemplo:

- [PyInstaller]
- [auto-py-to-exe]
- [NOMBRE_DE_TU_HERRAMIENTA_DE_EMPAQUETADO]

Ejemplo de estructura a completar una vez esté configurado:

```bash
[COMANDO_DE_EMPAQUETADO]
```

> Reemplaza el placeholder anterior con el comando real que utilices en tu entorno para generar la versión desktop de la aplicación.

## Uso de la aplicación

1. Abre la aplicación ejecutando `python main.py`.
2. Ajusta el tempo usando el control de BPM o los botones `+` y `-`.
3. Selecciona el compás y la subdivisión según lo que quieras practicar.
4. Controla el volumen con el slider correspondiente.
5. Pulsa el botón de inicio para comenzar el metrónomo.
6. Observa el indicador visual del pulso y escucha el clic generado por la aplicación.
7. Usa el botón de detener cuando quieras pausar la reproducción.

### Funcionamiento básico

- El metrónomo marca el pulso con sonidos distintos para el primer tiempo y para los tiempos siguientes.
- El indicador visual refleja el beat actual para ayudarte a mantener el ritmo.
- Los cambios de tempo y compás se aplican en tiempo real.

## Estructura del proyecto

```text
.
├── main.py
├── README.md
├── requirements.txt
├── core/
│   ├── __init__.py
│   ├── audio_engine.py
│   └── metronome.py
├── resources/
│   ├── accent.wav
│   ├── beat.wav
│   └── style.qss
└── ui/
    ├── __init__.py
    └── main_window.py
```

