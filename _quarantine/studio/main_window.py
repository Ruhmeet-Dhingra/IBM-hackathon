from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout
)

from studio.sidebar import Sidebar
from studio.pages.home import HomePage


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("ROV Studio")
        self.resize(1200, 800)

        central = QWidget()

        layout = QHBoxLayout()

        layout.addWidget(Sidebar())
        layout.addWidget(HomePage(), 1)

        central.setLayout(layout)

        self.setCentralWidget(central)