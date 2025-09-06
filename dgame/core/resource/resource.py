from dgame.misc.tools import get_asset_path, load_json
from dgame.misc.config import Config



CONFIG = Config()



class Resource:
    name = None
    shortname = None
    rid = None
    unit = None
    texture = None
    desc = None



class Ore(Resource):
    name="Ore"
    shortname="ore"
    rid=1001
    unit="tn"
    texture="ore-icon.png"
    desc="Unprocessed metal ore."

class Steel(Resource):
    name="Steel"
    shortname="steel"
    rid=1002
    unit="tn"
    texture="steel-icon.png"
    desc="Refined metal for industrial use."

class Wood(Resource):
    name="Wood"
    shortname="wood"
    rid=1003
    unit="tn"
    texture="wood-icon.png"
    desc="Raw harvested timber."

class Planks(Resource):
    name="Planks"
    shortname="plank"
    rid=1004
    unit="tn"
    texture="planks-icon.png"
    desc="Processed wooden planks."

class Stone(Resource):
    name="Stone"
    shortname="stone"
    rid=1005
    unit="tn"
    texture="stone-icon.png"
    desc="Roughly hewn stone."

class Food(Resource):
    name="Food"
    shortname="food"
    rid=1006
    unit="tn"
    texture="food-icon.png"
    desc="Consumable resources."

class Oil(Resource):
    name="Oil"
    shortname="oil"
    rid=1007
    unit="m3"
    texture="oil-icon.png"
    desc="Crude petroleum."

class Energy(Resource):
    name="Energy"
    shortname="energy"
    rid=1008
    unit="w"
    texture="energy-icon.png"
    desc="Electrical or mechanical power."

REGISTER = [Ore, Steel, Wood, Planks, Stone, Food, Oil, Energy]