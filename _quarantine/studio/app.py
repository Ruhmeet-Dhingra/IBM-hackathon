import sys

from PySide6.QtWidgets import QApplication

from studio.main_window import MainWindow
from pathlib import Path

style = Path(
    "studio/resources/styles/dark.qss"
).read_text()


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(style)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()