from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout
)

from PySide6.QtCore import Qt

from studio.widgets.orb import OrbWidget

class HomePage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        layout.setAlignment(Qt.AlignCenter)

        orb = OrbWidget()

        title = QLabel("Welcome to ROV Studio")

        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Your AI Workspace")

        subtitle.setAlignment(Qt.AlignCenter)

        layout.addWidget(orb)

        layout.addWidget(title)

        layout.addWidget(subtitle)

        self.setLayout(layout)