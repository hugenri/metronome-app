from PyQt6.QtCore import QObject, QTimer, Qt, pyqtSignal
from .audio_engine import AudioEngine


class Metronome(QObject):
    """
    Motor musical.
    No conoce widgets ni elementos de la interfaz.
    """

    position_changed = pyqtSignal(int, int, bool)
    running_changed = pyqtSignal(bool)

    def __init__(self, audio_engine: AudioEngine):
        super().__init__()

        self.audio = audio_engine

        self._bpm = 120
        self._numerator = 4
        self._denominator = 4
        self._subdivision = "quarter"
        self._volume = 0.75

        self._step = 0
        self._running = False

        self._timer = QTimer(self)
        self._timer.setTimerType(Qt.TimerType.PreciseTimer)
        self._timer.timeout.connect(self._on_tick)

    @property
    def bpm(self):
        return self._bpm

    @property
    def beats_per_bar(self):
        return self.main_beats

    @property
    def numerator(self):
        return self._numerator

    @property
    def denominator(self):
        return self._denominator

    @property
    def main_beats(self):
        if self.is_compound:
            return self._numerator // 3
        return self._numerator

    @property
    def is_compound(self):
        return (self._numerator, self._denominator) in {
            (6, 8),
            (9, 8),
            (12, 8),
        }

    @property
    def subdivisions_per_beat(self):
        if self.is_compound:
            return 6 if self._subdivision == "sixteenth" else 3
        if self._denominator == 8:
            return 2 if self._subdivision == "sixteenth" else 1
        return 2 if self._subdivision == "eighth" else 1

    @property
    def subdivision(self):
        return self._subdivision

    @property
    def volume(self):
        return self._volume

    @property
    def running(self):
        return self._running

    @property
    def steps_per_bar(self):
        return self.main_beats * self.subdivisions_per_beat

    def set_bpm(self, bpm: int):
        self._bpm = max(40, min(240, int(bpm)))
        if self._running:
            self._update_interval()

    def set_time_signature(self, numerator: int, denominator: int = 4):
        valid = {
            (2, 4),
            (3, 4),
            (4, 4),
            (5, 4),
            (6, 4),
            (7, 4),
            (2, 8),
            (3, 8),
            (4, 8),
            (6, 8),
            (9, 8),
            (12, 8),
        }
        if (numerator, denominator) not in valid:
            return
        self._numerator = numerator
        self._denominator = denominator
        self._step = 0
        self._update_interval()
        if self._running:
            self._play_current()

    def set_subdivision(self, subdivision: str):
        if subdivision not in ("quarter", "eighth", "sixteenth"):
            return
        self._subdivision = subdivision
        self._step = 0
        self._update_interval()
        if self._running:
            self._play_current()

    def set_volume(self, value: float):
        self._volume = max(0.0, min(1.0, float(value)))
        self.audio.set_volume(self._volume)

    def start(self):
        if self._running:
            return

        self._running = True
        self._step = 0
        self._update_interval()
        self._timer.start()
        self._play_current()
        self.running_changed.emit(True)

    def stop(self):
        if not self._running:
            return

        self._timer.stop()
        self._running = False
        self._step = 0
        self.running_changed.emit(False)

    def _update_interval(self):
        if self._denominator == 8 and self.is_compound:
            dotted_quarter_ms = 90000.0 / self._bpm
            interval = dotted_quarter_ms / self.subdivisions_per_beat
        elif self._denominator == 8:
            eighth_ms = 30000.0 / self._bpm
            interval = eighth_ms / self.subdivisions_per_beat
        else:
            quarter_ms = 60000.0 / self._bpm
            interval = quarter_ms / self.subdivisions_per_beat
        self._timer.setInterval(max(1, round(interval)))

    def _on_tick(self):
        self._step = (self._step + 1) % self.steps_per_bar
        self._play_current()

    def _play_current(self):
        if self.is_compound:
            beat = self._step // self.subdivisions_per_beat
            is_accent = self._step == 0
        elif self._denominator == 8:
            beat = self._step // self.subdivisions_per_beat
            is_accent = self._step == 0
        elif self._subdivision == "quarter":
            beat = self._step
            is_accent = beat == 0
        else:
            beat = self._step // self.subdivisions_per_beat
            is_accent = self._step == 0

        if is_accent:
            self.audio.play_accent()
        else:
            self.audio.play_beat()

        self.position_changed.emit(
            beat,
            self._step,
            is_accent,
        )
