from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton

class InputPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.enter_button = QPushButton("Enter")
        layout.addWidget(self.input_field)
        layout.addWidget(self.enter_button)
        self.setLayout(layout)