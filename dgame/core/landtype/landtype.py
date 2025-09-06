

class LandType:
    dn = None
    name = None
    shortname = None
    desc = None
    land = None
    colour = None



class Rainforest(LandType):
    dn=1
    name="Rainforest"
    shortname="rainforest"
    desc="Dense, biodiverse tropical forests with limited accessibility."
    land=True
    colour=[70, 119, 33]

class Forest(LandType):
    dn=2
    name="Forest"
    shortname="forest"
    desc="Temperate or boreal forests with moderate accessibility."
    land=True
    colour=[101, 132, 56]

class Marshland(LandType):
    dn=3
    name="Marshland"
    shortname="marsh"
    desc="Wetlands with soft ground and vegetation."
    land=True
    colour=[114, 121, 64]

class Moorland(LandType):
    dn=4
    name="Moorland"
    shortname="moor"
    desc="Open, peaty highland with rough vegetation."
    land=True
    colour=[167, 160, 98]

class Plains(LandType):
    dn=5
    name="Plains"
    shortname="plains"
    desc="Flat or gently rolling terrain suitable for development."
    land=True
    colour=[131, 173, 78]

class BareGround(LandType):
    dn=6
    name="Bare Ground"
    shortname="bare"
    desc="Exposed rock or soil with minimal vegetation."
    land=True
    colour=[230, 223, 170]

class ShallowWater(LandType):
    dn=7
    name="Shallow Water"
    shortname="shallow"
    desc="Relatively shallow water areas, making construction easier."
    land=False
    colour=[166, 206, 227]

class Snow(LandType):
    dn=8
    name="Snow"
    shortname="snow"
    desc="Snow-covered terrain, slippery and cold."
    land=True
    colour=[255, 255, 255]

class Urban(LandType):
    dn=9
    name="Urban"
    shortname="urban"
    desc="Built-up areas with high infrastructure and mobility."
    land=True
    colour=[153, 153, 153]

class DeepWater(LandType):
    dn=10
    name="Deep Water"
    shortname="deep"
    desc="Deep water areas with limited build potential."
    land=False
    colour=[147, 184, 202]

REGISTER = [Rainforest, Forest, Marshland, Moorland, Plains, BareGround, ShallowWater, Snow, Urban, DeepWater]