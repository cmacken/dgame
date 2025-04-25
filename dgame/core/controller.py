from PyQt5.QtCore import QObject, pyqtSignal

from dgame.core import WorldManager
from dgame.core import PlayerManager
from dgame.core.modifiers import Addition, Subtract, Multiplier

from dgame.core.entities.units import Worker
from dgame.core.entities.buildings import LumberCamp, Factory, Quarry

class GameController(QObject):

    # Optional signal to update UI
    state_updated = pyqtSignal()

    def __init__(self, num_players=1):

        super().__init__()

        self.PLAYERS = self.create_players(num_players)

        # Create initial
        WMAN = WorldManager() 

        self.T = 0

        WMAN.create(LumberCamp  , 0, 0, 0)
        WMAN.create(LumberCamp  , 0, 0, 0)
        WMAN.create(LumberCamp  , 0, 0, 0)
        WMAN.create(Quarry      , 0, 0, 0)
        WMAN.create(Quarry      , 0, 0, 0)
        WMAN.create(Quarry      , 0, 0, 0)
        WMAN.create(Factory     , 0, 0, 0)

        self.PLAYERS[0].MODIFIERS.append(Multiplier(5.0, ['wood','stone']))


    def create_players(self, nplayers):
        players = []
        for i in range(0,nplayers):
            player = PlayerManager(f'team_{i}', i)
            players.append(player)
        return players


    def update(self):

        # -- Main Game Logic --
        WMAN = WorldManager()  

        for player in self.PLAYERS:
            player.resolve()
            # Get all production facilities
            print(
                f"T-{int(self.T):<3} | {player.NAME:<10} | "
                f"wood: {int(player.resources['wood']):>3} ({int(sum(player.CHANGES['wood'])):+})   "
                f"stone: {int(player.resources['stone']):>3} ({int(sum(player.CHANGES['stone'])):+})   "
                f"money: {int(player.resources['money']):>3} ({int(sum(player.CHANGES['money'])):+})"
            )

        # Emit signal to update UI, if needed
        self.state_updated.emit()
        self.T += 1


if __name__ == '__main__':
    gc = GameController()
    gc.update()