from dgame.core.entities.buildings.building import Building
from dgame.core.modifiers import apply_modifiers


class Extraction(Building):

    TYPE = 'extraction'

    def base_resource(self,res):
        return self.BASE_RATES[res][self.LEVEL]

    def extract(self, player):
        out = {}
        for resource in self.BASE_RATES:
            base = self.base_resource(resource)
            final = apply_modifiers(resource, base, player.MODIFIERS)
            player.resources[resource] = player.resources[resource] + final
        return out