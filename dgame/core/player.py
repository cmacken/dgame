from dgame.core import WorldManager
import numpy as np



class PlayerManager:

    TID = None
    NAME = None
    
    MODIFIERS = []

    resources = {
        'wood' : 150,
        'stone' : 150,
        'money' : 0,
    }

    resources_max = {
        'wood' : 250,
        'stone' : 250,
        'money' : 250,
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
    
    def edit_resource(self, name, value):
        if name in self.CHANGES:
            self.CHANGES[name].append(value)
        else:
            self.CHANGES[name] = [value]
        self.resources[name] = self.resources[name] + value

    def resolve(self):

        self.CHANGES = {}

        for building in self.get_extraction():
            building.extract(self)
        for building in self.get_production():
            building.produce(self)

        # Cap resources
        for res, nmax in self.resources_max.items():
            self.resources[res] = np.clip(self.resources[res], 0,nmax)