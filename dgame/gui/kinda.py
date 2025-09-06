import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QSlider, QGraphicsView, QGraphicsScene,
    QGraphicsPixmapItem, QGraphicsRectItem
)
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPixmap, QImage, QColor, QBrush, QPainter

class SimpleGeoViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simplified Raster + Vector Viewer")

        layout = QVBoxLayout(self)

        # Graphics View and Scene
        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        self.view.setRenderHints(self.view.renderHints() | QPainter.Antialiasing)
        self.view.setDragMode(QGraphicsView.ScrollHandDrag)  # Pan with mouse drag
        layout.addWidget(self.view)

        # Create two random raster QPixmaps with different positions/sizes
        self.raster1 = self.create_random_raster(200, 150)
        self.raster2 = self.create_random_raster(150, 200)

        # Add raster1 at (0, 0)
        self.raster_item1 = QGraphicsPixmapItem(self.raster1)
        self.raster_item1.setOffset(0, 0)
        self.scene.addItem(self.raster_item1)

        # Add raster2 at (250, 100) - shifted to demonstrate different coverage
        self.raster_item2 = QGraphicsPixmapItem(self.raster2)
        self.raster_item2.setOffset(250, 100)
        self.scene.addItem(self.raster_item2)

        # Add simple vector rectangles on top of rasters
        # Rectangle over raster1
        self.vector_rect1 = QGraphicsRectItem(QRectF(50, 40, 80, 60))
        self.vector_rect1.setBrush(QBrush(QColor(255, 0, 0, 100)))  # Semi-transparent red
        self.vector_rect1.setPen(QColor(255, 0, 0))
        self.scene.addItem(self.vector_rect1)

        # Rectangle over raster2
        self.vector_rect2 = QGraphicsRectItem(QRectF(300, 150, 90, 90))
        self.vector_rect2.setBrush(QBrush(QColor(0, 0, 255, 100)))  # Semi-transparent blue
        self.vector_rect2.setPen(QColor(0, 0, 255))
        self.scene.addItem(self.vector_rect2)

        # Controls for opacity
        control_layout = QHBoxLayout()

        # Raster1 opacity
        control_layout.addWidget(QLabel("Raster 1 Opacity"))
        self.raster1_opacity_slider = QSlider(Qt.Horizontal)
        self.raster1_opacity_slider.setRange(0, 100)
        self.raster1_opacity_slider.setValue(255)
        self.raster1_opacity_slider.valueChanged.connect(self.set_raster1_opacity)
        control_layout.addWidget(self.raster1_opacity_slider)

        # Raster2 opacity
        control_layout.addWidget(QLabel("Raster 2 Opacity"))
        self.raster2_opacity_slider = QSlider(Qt.Horizontal)
        self.raster2_opacity_slider.setRange(0, 100)
        self.raster2_opacity_slider.setValue(255)
        self.raster2_opacity_slider.valueChanged.connect(self.set_raster2_opacity)
        control_layout.addWidget(self.raster2_opacity_slider)

        # Vector opacity
        control_layout.addWidget(QLabel("Vector Opacity"))
        self.vector_opacity_slider = QSlider(Qt.Horizontal)
        self.vector_opacity_slider.setRange(0, 100)
        self.vector_opacity_slider.setValue(40)
        self.vector_opacity_slider.valueChanged.connect(self.set_vector_opacity)
        control_layout.addWidget(self.vector_opacity_slider)

        layout.addLayout(control_layout)

        # Enable zooming with mouse wheel
        self.view.wheelEvent = self.wheelEvent

    def create_random_raster(self, width, height):
        """Create a random grayscale QPixmap."""
        arr = np.random.randint(0, 256, (height, width), dtype=np.uint8)
        # Create QImage from numpy array
        qimg = QImage(arr.data, width, height, width, QImage.Format_Grayscale8)
        pix = QPixmap.fromImage(qimg)
        return pix

    def set_raster1_opacity(self, val):
        opacity = val / 100
        self.raster_item1.setOpacity(opacity)

    def set_raster2_opacity(self, val):
        opacity = val / 100
        self.raster_item2.setOpacity(opacity)

    def set_vector_opacity(self, val):
        opacity = val / 100
        c1 = self.vector_rect1.brush().color()
        c1.setAlphaF(opacity)
        self.vector_rect1.setBrush(QBrush(c1))

        c2 = self.vector_rect2.brush().color()
        c2.setAlphaF(opacity)
        self.vector_rect2.setBrush(QBrush(c2))

    def wheelEvent(self, event):
        """Zoom in/out with mouse wheel centered on mouse pointer."""
        zoomInFactor = 1.25
        zoomOutFactor = 1 / zoomInFactor

        if event.angleDelta().y() > 0:
            zoomFactor = zoomInFactor
        else:
            zoomFactor = zoomOutFactor

        self.view.scale(zoomFactor, zoomFactor)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = SimpleGeoViewer()
    viewer.resize(800, 600)
    viewer.show()
    sys.exit(app.exec_())
