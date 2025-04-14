from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QMainWindow
from dgame.gui.navigation import MapLogPanel
from dgame.gui.character import StatsInventoryPanel
from dgame.gui.user import InputPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text RPG")
        self.resize(800, 600)

        main_widget = QWidget()
        main_layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        self.map_log = MapLogPanel()
        self.stats_inventory = StatsInventoryPanel()

        top_layout.addWidget(self.map_log, stretch=2)
        top_layout.addWidget(self.stats_inventory, stretch=1)

        self.input_panel = InputPanel()

        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.input_panel)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)