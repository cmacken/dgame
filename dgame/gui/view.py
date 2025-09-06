import sys
from PyQt5.QtWidgets import (
    QWidget, QGraphicsScene, QGraphicsView, QVBoxLayout,
    QHBoxLayout, QLabel, QSlider,
    QApplication, QMainWindow, QWidget, QSplitter,
    QVBoxLayout, QLabel, QGraphicsRectItem,
)
from PyQt5.QtCore import Qt, QPointF, QRectF
from dgame.core.world.world import GameWorld
from PyQt5.QtGui import QPixmap, QImage, QColor, QBrush, QPainter, QPen
from PyQt5.QtWidgets import QGraphicsPixmapItem
import numpy as np

WORLD = GameWorld()


def make_checker_image():
    # 5x5 RGB array
    arr = np.zeros((5, 5, 3), dtype=np.uint8)

    for r in range(5):
        for c in range(5):
            if (r + c) % 2 == 0:
                arr[r, c] = [255, 255, 255]  # white
            else:
                arr[r, c] = [0, 0, 0]        # black

    h, w, ch = arr.shape
    # Convert to QImage (Format_RGB888 expects packed RGB bytes)
    img = QImage(arr.data, w, h, ch * w, QImage.Format_RGB888)
    return QPixmap.fromImage(img.copy())  # copy to own the buffer




class CoordGraphicsView(QGraphicsView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mouse_pos_scene = None
        self.setMouseTracking(True)
        self.checker_items = []
        self.square_size = 1000

    def mouseMoveEvent(self, event):
        self.mouse_pos_scene = self.mapToScene(event.pos())
        self.viewport().update()
        super().mouseMoveEvent(event)


    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            scene_pos = self.mapToScene(event.pos())
            pixmap = make_checker_image()

            item = QGraphicsPixmapItem(pixmap)
            item.setOffset(-pixmap.width()/2, -pixmap.height()/2)  # center on cursor
            item.setPos(scene_pos)

            # Scale only in scene (not image memory!)
            item.setScale(1000.0)

            self.scene().addItem(item)
        else:
            super().mousePressEvent(event)

    def draw_checkerboard(self, rows=8, cols=8):
        # Clear existing checkerboard
        for item in self.checker_items:
            self.scene().removeItem(item)
        self.checker_items.clear()

        size = self.square_size
        for r in range(rows):
            for c in range(cols):
                x = c * size
                y = r * size
                rect = QRectF(x, y, size, size)
                color = QColor("black") if (r + c) % 2 == 0 else QColor("white")
                item = QGraphicsRectItem(rect)
                item.setBrush(QBrush(color))
                item.setPen(QPen(Qt.NoPen))   # fix here
                self.scene().addItem(item)
                self.checker_items.append(item)


    def paintEvent(self, event):
        super().paintEvent(event)
        if self.mouse_pos_scene is None:
            return

        painter = QPainter(self.viewport())
        painter.setRenderHint(QPainter.TextAntialiasing)
        x, y = self.mouse_pos_scene.x(), self.mouse_pos_scene.y()
        lon, lat = WORLD.BASEMAP.xy_to_latlon(x,y)
        text = f"X: {x:.2f}, Y: {y:.2f}   Lat: {lat:.2f}, Lon: {lon:.2f}"
        metrics = painter.fontMetrics()
        text_width = metrics.horizontalAdvance(text) + 8
        text_height = metrics.height() + 4

        # Draw translucent background
        painter.setBrush(QColor(0, 0, 0, 150))
        painter.setPen(Qt.NoPen)
        painter.drawRect(5, self.viewport().height() - text_height - 5,
                         text_width, text_height)

        # Draw text
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(9, self.viewport().height() - 5, text)

        painter.end()
