from dgame.core.entities.buildings.production.production import Production


class Factory(Production):


    RECIPE = ({'stone' : 5, 'wood' : 5},
              {'money' : 1})

    def produce(self, player):


        in_res, out_res = self.RECIPE
        
        # Check have the resources
        for res, v in in_res.items():
            if player.resources[res] < v:
                return

        # Consume
        for res, v in in_res.items():
            player.resources[res]  = player.resources[res] - v

        # Add
        for res, v in out_res.items():
            player.resources[res]  = player.resources[res] + v


