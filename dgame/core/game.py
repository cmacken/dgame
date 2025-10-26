from dgame.map.map import Map
from dgame.core.utils import get_logger


logger = get_logger(__name__)

# core/game.py
class GameInstance:

    def __init__(self):
        logger.info(f'Initializing game instance...')
        self.entities = {}
        self.factions = {}
        self.systems = []

    def compile(self):
        
        if not self.factions:
            raise Exception('No factions added! Use .add_faction')
        
        self.systems = [

        ]
        self.map = Map()
        self.entities = {}        
        self._t = 0

    def tick(self):
        logger.info(f'Begin tick {self._t}')

        logger.info(f'End tick {self._t}')
        self._t += 1

    def add_faction(self, faction_obj):
        self.factions[faction_obj.fid] = faction_obj

    def add_entity(self, e):
        self.entities[e.id] = e

    def get_entities(self, *component_types):
        for e in self.entities.values():
            if e.has(*component_types):
                yield e