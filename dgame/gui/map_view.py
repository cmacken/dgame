from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import QRectF, Qt

class MapView(QGraphicsView):
    def __init__(self, world_data):

        self._zoom = 0
        self._zoom_step = 1.25  # zoom factor per wheel tick
        self._max_zoom = 10
        self._min_zoom = -10

        self.colormap = {
            10: "darkGreen",
            20: "darkGreen",
            30: "green",
            40: "green",
            50: "green",
            60: "darkGray",
            70: "white",          
            80: "blue",  # optional background,
            90: "darkYellow"
        }
        
        
        super().__init__()
        self.world_data = world_data
        self.tile_size = 32  # pixels
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.load_world(world_data)

    def load_world(self, data):
        for row_idx, row in enumerate(data):
            for col_idx, tile_val in enumerate(row):
                color = self.colormap.get(tile_val, "magenta")  # fallback for unknown classes
                x = col_idx * self.tile_size
                y = row_idx * self.tile_size
                rect = QGraphicsRectItem(QRectF(x, y, self.tile_size, self.tile_size))
                rect.setBrush(QBrush(QColor(color)))
                self.scene.addItem(rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            scene_pos = self.mapToScene(event.pos())
            col = int(scene_pos.x() // self.tile_size)
            row = int(scene_pos.y() // self.tile_size)

            if 0 <= row < len(self.world_data) and 0 <= col < len(self.world_data[0]):
                self.on_tile_clicked(row, col)

    def on_tile_clicked(self, row, col):
        print(f"Clicked tile at row={row}, col={col}")
        # You can trigger game logic here

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0 and self._zoom < self._max_zoom:
            zoom_factor = self._zoom_step
            self._zoom += 1
        elif event.angleDelta().y() < 0 and self._zoom > self._min_zoom:
            zoom_factor = 1 / self._zoom_step
            self._zoom -= 1
        else:
            return

        self.scale(zoom_factor, zoom_factor)