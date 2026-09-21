import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Metrónomo")
    style_path = Path(__file__).resolve().parent / "resources" / "style.qss"
    app.setStyleSheet(style_path.read_text(encoding="utf-8"))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
