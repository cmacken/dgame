from dgame.misc.tools import get_asset_path, load_json
from dataclasses import dataclass, field



class BaseLayer:
    name = None
    lid = None
    shortname = None
    path = None
    visualise = None


class ConditionLayer(BaseLayer):
    units = None
    scale = None
    offset = None


class ResourceLayer(BaseLayer):
    field = None
    rid = None



class Elevation(ConditionLayer):
    name="Elevation"
    lid=0
    shortname="elev"
    path=["maps", "elevation.tif"]
    visualise={
        "TYPE": "QUANTILE",
        "NQUANT": 15,
        "COLOURMAP": "Greys",
        "IGNORE": [0.0],
    }
    units="m"
    scale=100.0
    offset=0.0

class OilField(ResourceLayer):
    name="Oil Fields"
    lid=1
    shortname="oil"
    path=["maps", "oil.geojson"]
    visualise={
        "TYPE": "LINEAR",
        "COLOURMAP": "Reds",
    }
    rid=1007
    field="DN"


REGISTER = [Elevation, OilField]