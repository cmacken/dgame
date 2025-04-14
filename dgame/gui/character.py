from PyQt5.QtWidgets import QTabWidget, QWidget, QLabel, QVBoxLayout

class StatsInventoryPanel(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(self.create_tab("Character stats here"), "Stats")
        self.addTab(self.create_tab("Inventory items here"), "Inventory")

    def create_tab(self, text):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(text))
        widget.setLayout(layout)
        return widget