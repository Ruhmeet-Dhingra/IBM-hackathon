import math
import random

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QPointF
from PySide6.QtGui import (
    QPainter,
    QColor,
    QPen,
    QRadialGradient
)


class OrbWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.setMinimumSize(320, 320)

        self.radius = 80
        self.scale = 1.0
        self.direction = 1

        self.angle = 0

        # Create particles
        self.particles = []

        for _ in range(70):

            self.particles.append({
                "angle": random.uniform(0, 360),
                "distance": random.uniform(110, 150),
                "size": random.uniform(1.5, 3.5),
                "speed": random.uniform(0.2, 0.8),
                "alpha": random.randint(80, 180)
            })

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)

    def animate(self):

        self.angle += 0.4

        self.scale += self.direction * 0.0025

        if self.scale > 1.05:
            self.direction = -1

        elif self.scale < 0.95:
            self.direction = 1

        for particle in self.particles:
            particle["angle"] += particle["speed"]

        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        center = self.rect().center()

        self.draw_particles(painter, center)
        self.draw_glow(painter, center)
        self.draw_rings(painter, center)
        self.draw_core(painter, center)

    def draw_particles(self, painter, center):

        painter.setPen(Qt.NoPen)

        for p in self.particles:

            angle = math.radians(p["angle"])

            x = center.x() + math.cos(angle) * p["distance"]

            y = center.y() + math.sin(angle) * p["distance"]

            painter.setBrush(
                QColor(120, 210, 255, p["alpha"])
            )

            painter.drawEllipse(
                QPointF(x, y),
                p["size"],
                p["size"]
            )

    def draw_glow(self, painter, center):

        painter.setPen(Qt.NoPen)

        r = self.radius * self.scale

        for i in range(18):

            alpha = max(2, 22 - i)

            painter.setBrush(
                QColor(50, 170, 255, alpha)
            )

            painter.drawEllipse(
                QPointF(center),
                r + i * 6,
                r + i * 6
            )

    def draw_core(self, painter, center):

        r = self.radius * self.scale

        gradient = QRadialGradient(
            QPointF(center),
            r
        )

        gradient.setColorAt(
            0,
            QColor(230, 250, 255)
        )

        gradient.setColorAt(
            0.25,
            QColor(120, 220, 255)
        )

        gradient.setColorAt(
            0.7,
            QColor(60, 170, 255)
        )

        gradient.setColorAt(
            1,
            QColor(20, 90, 180)
        )

        painter.setPen(Qt.NoPen)

        painter.setBrush(gradient)

        painter.drawEllipse(
            QPointF(center),
            r,
            r
        )

    def draw_rings(self, painter, center):

        painter.setBrush(Qt.NoBrush)

        r = self.radius * self.scale

        pen = QPen(
            QColor(120, 220, 255, 80),
            2
        )

        painter.setPen(pen)

        painter.save()

        painter.translate(center)

        painter.rotate(self.angle)

        painter.drawEllipse(
            QPointF(0, 0),
            r + 22,
            r + 22
        )

        painter.restore()

        painter.save()

        painter.translate(center)

        painter.rotate(-self.angle * 0.7)

        painter.drawEllipse(
            QPointF(0, 0),
            r + 36,
            r + 36
        )

        painter.restore()