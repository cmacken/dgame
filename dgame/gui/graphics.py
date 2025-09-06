import sys
from PyQt5.QtWidgets import (
    QWidget, QGraphicsScene, QGraphicsView, QVBoxLayout,
    QHBoxLayout, QLabel, QSlider,
    QApplication, QMainWindow, QWidget, QSplitter,
    QVBoxLayout, QLabel, QGraphicsRectItem
)
from PyQt5.QtCore import Qt, QPointF
from dgame.core import GameInstance
from PyQt5.QtGui import QPixmap, QImage, QColor, QBrush, QPainter, QPen
from dgame.gui.view import CoordGraphicsView
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsPolygonItem, QGraphicsItemGroup, QGraphicsPathItem

class GraphicsWindow(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.items = {}  # {layer_name: QGraphicsItem}

        self.INSTANCE = GameInstance()

        # Graphics setup
        self.scene = QGraphicsScene()
        self.view = CoordGraphicsView(self.scene)
        self.view.setRenderHints(self.view.renderHints() | QPainter.Antialiasing)
        self.view.setDragMode(QGraphicsView.ScrollHandDrag)  # Pan with mouse drag
        self.view.wheelEvent = self.wheelEvent

        layout = QVBoxLayout(self)
        layout.addWidget(self.view)

        self.update()

    def update(self):
        """Clears and redraws all layers from the layer manager."""

        layers = self.INSTANCE.WORLD.LAYERS

        print('Creating map view...')
        self.scene.clear()
        self.items.clear()

        bm = self._get_basemap_pixmap()
        self.scene.addItem(bm)
        self.items["_basemap"] = bm

        for layer_name, layer in layers.items():

            item = layer.to_canvas_item()
            self.scene.addItem(item)
            self.items[layer_name] = item






    def _get_basemap_pixmap(self):

        arr = self.INSTANCE.WORLD.BASEMAP.render() 
        h, w, ch = arr.shape

        pixmap = QPixmap.fromImage(QImage(arr.data, w, h, 3 * w, QImage.Format_RGB888))
        return QGraphicsPixmapItem(pixmap)


    def remove_layer(self, layer_name):
        """Removes a specific layer from scene and manager."""
        if layer_name in self.items:
            self.scene.removeItem(self.items[layer_name])
            del self.items[layer_name]

        if layer_name in self.layer_manager:
            del self.layer_manager[layer_name]


    def opacity_controller(self):
        """
        Creates and returns a QWidget with sliders for each layer's opacity.
        This widget can be added anywhere (e.g., as a tab in another widget).
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)

        for layer_name, item in self.items.items():
            if layer_name[0] == '_':
                continue
            row = QHBoxLayout()
            label = QLabel(layer_name)
            slider = QSlider(Qt.Horizontal)
            slider.setRange(0, 100)
            slider.setValue(int(item.opacity() * 100))
            slider.valueChanged.connect(lambda val, it=item: it.setOpacity(val / 100))
            row.addWidget(label)
            row.addWidget(slider)
            layout.addLayout(row)

        return widget

    def wheelEvent(self, event):
        """Zoom in/out with mouse wheel centered on mouse pointer."""
        zoomInFactor = 1.25
        zoomOutFactor = 1 / zoomInFactor

        if event.angleDelta().y() > 0:
            zoomFactor = zoomInFactor
        else:
            zoomFactor = zoomOutFactor

        self.view.scale(zoomFactor, zoomFactor)

# ---- Main Application ----
def main():

    app = QApplication(sys.argv)

    # Main map widget
    map_widget = GraphicsWindow()

    # Opacity control panel
    opacity_controls = map_widget.opacity_controller()

    # Split view
    splitter = QSplitter(Qt.Horizontal)
    splitter.addWidget(map_widget)
    splitter.addWidget(opacity_controls)
    splitter.setSizes([800, 200])  # initial size ratio

    # Main window
    main_win = QMainWindow()
    main_win.setWindowTitle("Layered Graphics Window with Opacity Control")
    main_win.setCentralWidget(splitter)
    main_win.resize(1000, 600)
    main_win.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()