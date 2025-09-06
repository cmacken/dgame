from dgame.misc.tools import get_asset_path, load_json
from dgame.misc.config import Config

from pathlib import Path
import rioxarray as rxr
import rasterio as rio
import numpy as np

CONFIG = Config()

class BasemapPlugin:

    def __init__(self):

        super().__init__()

        print('Initialising basemap...')

        print('     ... loading landtype')
        self.LANDTYPE = rxr.open_rasterio(
            get_asset_path(*CONFIG.get('BASEMAP', 'LANDTYPE_PATH'))
        ).astype(np.uint8)

        print('     ... loading elevation')
        self.ELEVATION = rxr.open_rasterio(
            get_asset_path(*CONFIG.get('BASEMAP', 'ELEVATION_PATH'))
        ).astype(np.uint8)
        
        self.shape = self.LANDTYPE.shape          