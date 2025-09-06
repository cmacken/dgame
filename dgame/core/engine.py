from dgame.misc.config import Config
from dgame.core.basemap.basemap import BasemapPlugin
from dgame.core.resource.plugin import ResourcePlugin
from dgame.core.landtype.plugin import LandTypePlugin
from dgame.core.layer.plugin import LayerPlugin
from dgame.core.faction.plugin import FactionPlugin

CONFIG = Config()


class GameEngine(BasemapPlugin, 
                 ResourcePlugin,
                 LandTypePlugin,
                 LayerPlugin,
                 FactionPlugin):


    def __init__(self):

        print('Compiling game instance...')

        super().__init__()

        pass
