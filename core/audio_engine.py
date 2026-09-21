from pathlib import Path
import math
import struct
import wave

from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QSoundEffect


class AudioEngine:
    """Genera y reproduce los dos sonidos del metrónomo."""

    SAMPLE_RATE = 44100

    def __init__(self, resource_dir: Path):
        resource_dir.mkdir(parents=True, exist_ok=True)

        self.accent_path = resource_dir / "accent.wav"
        self.beat_path = resource_dir / "beat.wav"

        self._create_tone(
            self.accent_path,
            frequency=1050,
            duration=0.045,
            amplitude=0.92,
        )
        self._create_tone(
            self.beat_path,
            frequency=700,
            duration=0.040,
            amplitude=0.68,
        )

        self.accent = QSoundEffect()
        self.beat = QSoundEffect()

        self.accent.setSource(QUrl.fromLocalFile(str(self.accent_path.resolve())))
        self.beat.setSource(QUrl.fromLocalFile(str(self.beat_path.resolve())))

        self.set_volume(0.75)

    def set_volume(self, value: float):
        value = max(0.0, min(1.0, value))
        self.accent.setVolume(value)
        self.beat.setVolume(value)

    def play_accent(self):
        self.accent.stop()
        self.accent.play()

    def play_beat(self):
        self.beat.stop()
        self.beat.play()

    @classmethod
    def _create_tone(cls, path: Path, frequency: float, duration: float, amplitude: float):
        # No regenerar innecesariamente el archivo.
        if path.exists() and path.stat().st_size > 100:
            return

        count = int(cls.SAMPLE_RATE * duration)
        fade_samples = max(1, int(cls.SAMPLE_RATE * 0.008))

        with wave.open(str(path), "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(cls.SAMPLE_RATE)

            frames = bytearray()

            for i in range(count):
                t = i / cls.SAMPLE_RATE

                # Pequeña caída exponencial para un click limpio.
                envelope = math.exp(-34.0 * t)

                if i < fade_samples:
                    envelope *= i / fade_samples

                sample = amplitude * envelope * math.sin(
                    2.0 * math.pi * frequency * t
                )

                value = int(max(-1.0, min(1.0, sample)) * 32767)
                frames.extend(struct.pack("<h", value))

            wav.writeframes(frames)
