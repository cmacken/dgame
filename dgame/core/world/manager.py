from dgame.core.misc.singleton import SingletonMeta
from dgame.core.world.generation import WorldGeneration
from dgame.core.misc.coordinates import Coordinate

from dgame.core.entities.units import Worker



class WorldManager(WorldGeneration, metaclass=SingletonMeta):

    """
    Stores information on units, buildings, and terrain/resouces maps.
    """

    OBJECTS = {}

    def __init__(self):
        # -- Create a new world
        # Load/Generate Terrain
        self.terrain = self.load_terrain()
        self.resource = self.load_resource()


    def query(self, x, y):
        search_coord = Coordinate(x, y)
        entities = [v.ID for k,v in self.OBJECTS.items() if search_coord == v.COORD]
        return entities


    def active(self):
        return [v.ID for k, v in self.OBJECTS.items() if v.ACTIVE == True]


    def inactive(self):
        return [v.ID for k, v in self.OBJECTS.items() if v.ACTIVE == False]


    def all_ids(self):
        return self.active() + self.inactive()


    def create(self, entity_class, x, y, tid):
        ids = self.all_ids()
        max_id = max(ids) if len(ids) > 0 else 0
        new_id = max_id + 1
        self.OBJECTS[new_id] = entity_class(new_id, tid, x,y)


    def delete(self, entity_id):
        entity = self.OBJECTS.pop(entity_id)
        self.TRASH.append(entity)




if __name__ == '__main__':
    wman = WorldManager()
    wman.create(Worker, 0, 0)
    wman.create(Worker, 0, 0)
    wman.create(Worker, 0, 0)
    wman.delete(1)
    wman.delete(3)
    pass