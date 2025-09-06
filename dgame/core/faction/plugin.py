



from dgame.core.faction.faction import REGISTER

class FactionPlugin:
    """Stores layers and allows access by SHORTNAME or NAME."""

    def __init__(self):

        print('Compiling layers...')
        self.FACTIONS = {}
        for faction_obj in REGISTER:
            print(f'     ... adding {faction_obj.shortname}')
            self.FACTIONS[faction_obj.lid] = faction_obj