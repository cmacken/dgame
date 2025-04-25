from dgame.core.misc.coordinates import Coordinate

from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QImage
from importlib.resources import files

class Entity:

    NAME  = None
    COORD = None
    ID    = None
    TID   = None

    TEXTURE_NAME = None
    TEXTURE_IMG  = None
    TEXTURE      = None

    LEVEL = 1

    ACTIVE = True
    HIDE   = False

    TYPE = None

    def __init__(self, id, tid, x, y , hide=False, active=True, level=1):
        self.NAME = self.__class__.__name__
        self.COORD = Coordinate(x,y)
        self.ID = id
        self.TID = tid
        self.load_texture()
        ACTIVE = active
        HIDE = hide
        LEVEL = level


    def load_texture(self):
        if self.TEXTURE_NAME is None:
            png_path = files('dgame.assets.textures') / 'missing.png'
        else:
            png_path = files('dgame.assets.textures') / self.TEXTURE_NAME
        self.TEXTURE_IMG = QImage(str(png_path))


    @property
    def TEXTURE(self):
        return QPixmap.fromImage(self.TEXTURE_IMG)