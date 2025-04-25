from dgame.core.entities.buildings.production.production import Production


class Factory(Production):


    RECIPE = {'stone' : -5, 
               'wood' : -5, 
               'money' : 1}

    def produce(self, player):

        for res, v in self.RECIPE.items():
            if (player.resources[res] + v) < 0:
                return

        # Check have the resources
        for res, v in self.RECIPE.items():
            player.edit_resource(res, v)



