from dgame.core.entities.buildings.extraction.extraction import Extraction

class LumberCamp(Extraction):

    TEXTURE_NAME = 'missing.png'

    BASE_RATES = {
        'wood' : {
            1 : 1.0,
            2 : 2.0,
            3 : 3.0,
        },
    }