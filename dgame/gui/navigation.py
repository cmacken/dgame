from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QLabel
from dgame.gui.map import MapView

class MapLogPanel(QTabWidget):
    def __init__(self):
        super().__init__()


        ###########
        import rasterio

        with rasterio.open("C:\\Users\\camth\\Development\\dgame\\.hidden\\example_map.tif") as src:
            band1 = src.read(1)  # shape: (height, width)
            world_data = band1.tolist()  # Convert NumPy array to list of lists



        # Example world data: each tile is a color string
        #world_data = [
        #    ["green", "green", "blue", "gray"],
        #    ["green", "gray", "blue", "blue"],
        #    ["green", "green", "green", "gray"],
        #    ["blue", "blue", "green", "green"]
        #]



        self.map_view = MapView(world_data)
        self.addTab(self.create_map_tab(), "Map")
        self.addTab(self.create_log_tab(), "Log")

    def create_map_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.map_view)
        widget.setLayout(layout)
        return widget

    def create_log_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Log output here"))
        widget.setLayout(layout)
        return widget