from dgame.core.landtype.landtype import REGISTER
from dgame.misc.tools import get_asset_path, load_json

class LandTypePlugin:
    """Stores layers and allows access by SHORTNAME or NAME."""

    def __init__(self):
        
        super().__init__()
        
        print('Compiling land types...')        

        self.LANDTYPES = {}
        for ltype_obj in REGISTER:
            print(f'     ... adding {ltype_obj.shortname}')
            self.LANDTYPES[ltype_obj.dn] = ltype_obj