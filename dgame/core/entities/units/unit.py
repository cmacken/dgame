from dgame.core.entities.entity import Entity
from dgame.core.misc.coordinates import Coordinate

class Unit(Entity):

    TYPE = 'unit'

    def update_position(self,x, y):
        self.COORD = Coordinate(x,y)