from dgame.core.entities.buildings.extraction.extraction import Extraction

class Quarry(Extraction):

    TEXTURE_NAME = 'missing.png'

    BASE_RATES = {
        'stone' : {
            1 : 0.5,
            2 : 1.0,
            3 : 1.5
        }
    }