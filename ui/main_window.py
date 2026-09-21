from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QSlider, QComboBox, QFrame
)

from core.audio_engine import AudioEngine
from core.metronome import Metronome


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        base = Path(__file__).resolve().parent.parent
        self.audio = AudioEngine(base / "resources")
        self.metronome = Metronome(self.audio)

        self.setWindowTitle("Metrónomo")
        self.setMinimumSize(640, 560)
        self.resize(700, 620)

        self._build_ui()
        self._connect()
        self._sync_ui()

    def _build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)

        layout = QVBoxLayout(root)
        layout.setContentsMargins(24, 18, 24, 18)
        layout.setSpacing(10)

        # Header
        
        header = QHBoxLayout()
        brand_box = QVBoxLayout()
       
        subtitle = QLabel("M E T R Ó N O M O")
        subtitle.setObjectName("subtitle")
        brand_box.addWidget(subtitle)

        header.addLayout(brand_box)
        header.addStretch()
        #header.addWidget(tagline)
        layout.addLayout(header)
        

        # Tempo
        tempo_card = QFrame()
        tempo_card.setObjectName("card")
        tempo_layout = QVBoxLayout(tempo_card)
        tempo_layout.setContentsMargins(14, 8, 14, 10)

        tempo_title = QLabel("TEMPO")
        tempo_title.setObjectName("section")
        tempo_layout.addWidget(tempo_title)

        tempo_row = QHBoxLayout()
        self.minus_btn = QPushButton("−")
        self.minus_btn.setObjectName("tempoButton")

        self.bpm_label = QLabel("120 BPM")
        self.bpm_label.setObjectName("bpm")
        self.bpm_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bpm_label.setMinimumWidth(120)

        self.plus_btn = QPushButton("+")
        self.plus_btn.setObjectName("tempoButton")

        tempo_row.addWidget(self.minus_btn)
        tempo_row.addStretch()
        tempo_row.addWidget(self.bpm_label)
        tempo_row.addStretch()
        tempo_row.addWidget(self.plus_btn)

        tempo_layout.addLayout(tempo_row)

        self.bpm_slider = QSlider(Qt.Orientation.Horizontal)
        self.bpm_slider.setRange(40, 240)
        self.bpm_slider.setValue(120)
        tempo_layout.addWidget(self.bpm_slider)

        layout.addWidget(tempo_card)

        # Beat ring
        beat_area = QVBoxLayout()
        beat_area.setSpacing(10)

        self.beat_ring = QFrame()
        self.beat_ring.setObjectName("beatRing")
        self.beat_ring.setFixedSize(180, 180)

        ring_layout = QVBoxLayout(self.beat_ring)
        ring_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.beat_number = QLabel("1")
        self.beat_number.setObjectName("beatNumber")
        self.beat_number.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ring_layout.addWidget(self.beat_number)

        center_row = QHBoxLayout()
        center_row.addStretch()
        center_row.addWidget(self.beat_ring)
        center_row.addStretch()
        beat_area.addLayout(center_row)

        self.steps_layout = QHBoxLayout()
        self.steps_layout.setSpacing(6)
        self.steps_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        beat_area.addLayout(self.steps_layout)

        layout.addLayout(beat_area)

        # Options
        grid = QGridLayout()
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(8)

        sig_box = QVBoxLayout()
        sig_box.setSpacing(6)
        sig_title = QLabel("COMPÁS")
        sig_title.setObjectName("section")
        self.signature = QComboBox()
        self.signature.addItems([
            "2/4", "3/4", "4/4", "5/4", "6/4", "7/4",
            "2/8", "3/8", "4/8",
            "6/8", "9/8", "12/8",
        ])
        self.signature.setCurrentText("4/4")
        self.signature.setFixedHeight(38)
        sig_box.addWidget(sig_title)
        sig_box.addWidget(self.signature)

        div_box = QVBoxLayout()
        div_box.setSpacing(6)
        div_title = QLabel("DIVISIÓN")
        div_title.setObjectName("section")
        self.division = QComboBox()
        self.division.setFixedHeight(38)
        self.division.addItems(["Negras", "Corcheas"])
        div_box.addWidget(div_title)
        div_box.addWidget(self.division)

        grid.addLayout(sig_box, 0, 0)
        grid.addLayout(div_box, 0, 1)
        layout.addLayout(grid)

        # Volume
        volume_card = QFrame()
        volume_card.setObjectName("card")
        volume_layout = QVBoxLayout(volume_card)
        volume_layout.setContentsMargins(16, 10, 16, 12)

        vol_top = QHBoxLayout()
        vol_title = QLabel("VOLUMEN")
        vol_title.setObjectName("section")
        self.volume_percent = QLabel("75%")
        self.volume_percent.setObjectName("percent")
        vol_top.addWidget(vol_title)
        vol_top.addStretch()
        vol_top.addWidget(self.volume_percent)

        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(75)

        volume_layout.addLayout(vol_top)
        volume_layout.addWidget(self.volume_slider)
        layout.addWidget(volume_card)

        # Buttons
        buttons = QHBoxLayout()
        buttons.setSpacing(22)

        self.start_btn = QPushButton("▶   Iniciar")
        self.start_btn.setObjectName("start")
        self.start_btn.setMinimumHeight(50)

        self.stop_btn = QPushButton("■   Detener")
        self.stop_btn.setObjectName("stop")
        self.stop_btn.setMinimumHeight(50)

        buttons.addWidget(self.start_btn)
        buttons.addWidget(self.stop_btn)
        layout.addLayout(buttons)

        layout.addStretch()

        self._rebuild_steps()

    def _connect(self):
        self.start_btn.clicked.connect(self.metronome.start)
        self.stop_btn.clicked.connect(self.metronome.stop)

        self.bpm_slider.valueChanged.connect(self._bpm_changed)
        self.minus_btn.clicked.connect(lambda: self._change_bpm(-1))
        self.plus_btn.clicked.connect(lambda: self._change_bpm(1))

        self.signature.currentTextChanged.connect(self._signature_changed)
        self.division.currentTextChanged.connect(self._division_changed)
        self.volume_slider.valueChanged.connect(self._volume_changed)

        self.metronome.position_changed.connect(self._position_changed)
        self.metronome.running_changed.connect(self._running_changed)

    def _sync_ui(self):
        self._update_bpm_label(self.metronome.bpm)
        self._rebuild_steps()
        self._position_changed(0, 0, True)
        self._running_changed(False)

    def _bpm_changed(self, value):
        self.metronome.set_bpm(value)
        self._update_bpm_label(value)

    def _change_bpm(self, delta):
        value = max(40, min(240, self.metronome.bpm + delta))
        self.bpm_slider.setValue(value)

    def _update_bpm_label(self, value):
        self.bpm_label.setText(f"{value} BPM")

    def _signature_changed(self, value):
        numerator, denominator = map(int, value.split("/"))
        self.metronome.set_time_signature(numerator, denominator)
        self._configure_division_options()
        self._rebuild_steps()
        self._position_changed(0, 0, True)

    def _division_changed(self, value):
        if self.metronome.denominator == 8:
            subdivision = "sixteenth" if value == "Semicorcheas" else "eighth"
        else:
            subdivision = "eighth" if value == "Corcheas" else "quarter"
        self.metronome.set_subdivision(subdivision)
        self._rebuild_steps()
        self._position_changed(0, 0, True)

    def _configure_division_options(self):
        options = ["Corcheas", "Semicorcheas"] if self.metronome.denominator == 8 else [
            "Negras", "Corcheas"
        ]
        current = options[0]
        self.division.blockSignals(True)
        self.division.clear()
        self.division.addItems(options)
        self.division.setCurrentText(current)
        self.division.blockSignals(False)
        self.metronome.set_subdivision(
            "eighth" if self.metronome.denominator == 8 else "quarter"
        )

    def _volume_changed(self, value):
        self.metronome.set_volume(value / 100.0)
        self.volume_percent.setText(f"{value}%")

    def _rebuild_steps(self):
        while self.steps_layout.count():
            item = self.steps_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if self.metronome.denominator == 8:
            syllables = []
            for eighth in range(self.metronome.numerator):
                syllables.append(str(eighth + 1))
                if self.metronome.subdivision == "sixteenth":
                    syllables.append("&")
        else:
            syllables = []
            for beat in range(self.metronome.main_beats):
                syllables.append(str(beat + 1))
                if self.metronome.subdivision in ("eighth", "sixteenth"):
                    syllables.append("&")

        for text in syllables:
            label = QLabel(text)
            label.setObjectName("step")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.steps_layout.addWidget(label)

    def _position_changed(self, beat, step, is_accent):
        self.beat_number.setText(str(beat + 1))

        self.beat_ring.setProperty("class", None)
        if is_accent:
            self.beat_ring.setProperty("class", "accent")
        elif self.metronome.running:
            self.beat_ring.setProperty("class", "active")

        self.beat_ring.style().unpolish(self.beat_ring)
        self.beat_ring.style().polish(self.beat_ring)

        # Actualizar el pulso y la subdivisión visibles.
        if self.metronome.is_compound:
            active_index = step
        elif self.metronome.subdivision in ("eighth", "sixteenth"):
            active_index = step
        else:
            active_index = beat

        for i in range(self.steps_layout.count()):
            widget = self.steps_layout.itemAt(i).widget()
            if widget is None:
                continue

            active = i == active_index

            widget.setProperty("class", "active" if active else None)

            if is_accent and active:
                widget.setProperty("class", "accent")

            widget.style().unpolish(widget)
            widget.style().polish(widget)

    def _running_changed(self, running):
        self.start_btn.setEnabled(not running)
        self.stop_btn.setEnabled(running)

        if running:
            self.start_btn.setText("●   Ejecutando")
        else:
            self.start_btn.setText("▶   Iniciar")
            self.beat_ring.setProperty("class", None)
            self.beat_ring.style().unpolish(self.beat_ring)
            self.beat_ring.style().polish(self.beat_ring)
