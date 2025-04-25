from dgame.core.entities.buildings.extraction.extraction import Extraction

class Quarry(Extraction):

    TEXTURE_NAME = 'missing.png'

    BASE_RATES = {
        'stone' : {
            1 : 1.0,
            2 : 2.0,
            3 : 3.0
        }
    }