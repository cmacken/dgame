import sys

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QMainWindow
from dgame.core.gui.navigation import MapLogPanel
from dgame.core.gui.character import StatsInventoryPanel
from dgame.core.gui.user import InputPanel
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtCore import QTimer

class MainWindow(QMainWindow):

    def __init__(self, engine):
        
        super().__init__()
        self.engine = engine

        # Connect the signal to the slot
        self.engine.state_updated.connect(self.update)

        # Example UI element
        self.label = QLabel("Position: (0, 0)", self)
        self.label.move(10, 10)
        self.resize(200, 100)

        # Start the game tick
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.engine.update)
        self.timer.start(500)

    def update(self):
        # Update UI with new game state
        #print('boom')
        pass