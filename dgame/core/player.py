from dgame.core import WorldManager




class PlayerManager:

    TID = None
    NAME = None
    
    MODIFIERS = [ ]

    resources = {
        'wood' : 0,
        'stone' : 0,
        'money' : 0,
    }

    def __init__(self, team_name, team_id):

        self.TID  = team_id
        self.NAME = team_name

    def get_production(self):
        WMAN = WorldManager() 
        return [v for k,v in WMAN.OBJECTS.items() if (v.TID == self.TID) and (v.TYPE == 'production')]

    def get_extraction(self):
        WMAN = WorldManager() 
        return [v for k,v in WMAN.OBJECTS.items() if (v.TID == self.TID) and (v.TYPE == 'extraction')]

    def get_units(self):
        WMAN = WorldManager() 
        return [v for k,v in WMAN.OBJECTS.items() if (v.TID == self.TID) and (v.TYPE == 'unit')]

    def get_entities(self):
        return self.get_production() + self.get_extraction() + self.get_units()
    



    def resolve(self):

        for building in self.get_extraction():
            prod = building.extract(self)
            pass

        for building in self.get_production():
            prod = building.produce(self)
            pass