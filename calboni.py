
import sys
import time
import random

import pyautogui
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLabel, QSpinBox, QPushButton
)

pyautogui.FAILSAFE = True


class Calboni(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CALBONI")
        self.setMinimumWidth(440)

        self.running = False
        self.last_position = pyautogui.position()
        self.last_activity = time.monotonic()

        layout = QVBoxLayout(self)

        title = QLabel("CALBONI")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")
        layout.addWidget(title)

        subtitle = QLabel(
            "Ufficio Assenteismo e Produttività Apparente\n"
            "Il software che lavora per non lavorare"
        )
        layout.addWidget(subtitle)

        layout.addWidget(QLabel("Idle time (seconds):"))

        self.idle_input = QSpinBox()
        self.idle_input.setRange(2, 3600)
        self.idle_input.setValue(30)
        layout.addWidget(self.idle_input)

        self.button = QPushButton("START")
        self.button.clicked.connect(self.toggle)
        layout.addWidget(self.button)

        self.status = QLabel("Calboni è in pausa.")
        layout.addWidget(self.status)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_mouse)
        self.timer.start(500)

    def toggle(self):
        self.running = not self.running
        self.last_position = pyautogui.position()
        self.last_activity = time.monotonic()

        self.button.setText("STOP" if self.running else "START")
        self.idle_input.setEnabled(not self.running)
        self.status.setText(
            "Calboni sta lavorando duramente..."
            if self.running else "Calboni è in pausa."
        )

    def check_mouse(self):
        if not self.running:
            return

        current_position = pyautogui.position()
        now = time.monotonic()

        if current_position != self.last_position:
            self.last_position = current_position
            self.last_activity = now
            return

        if now - self.last_activity >= self.idle_input.value():
            self.move_mouse()
            self.last_activity = time.monotonic()

    def move_mouse(self):
        width, height = pyautogui.size()

        x = random.randint(50, max(50, width - 50))*.5
        y = random.randint(50, max(50, height - 50))*.5

        pyautogui.moveTo(x, y, duration=0.3)
        self.last_position = pyautogui.position()

        self.status.setText("Calboni ha mosso un dito. Che fatica.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calboni()
    window.show()
    sys.exit(app.exec())
