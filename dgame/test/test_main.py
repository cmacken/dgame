from dgame.core.game import GameInstance
from dgame.core.component import Faction
from dgame.core.utils import get_logger
import time

logger = get_logger(__name__)

limit, _ = 100, 0

game = GameInstance()
game.add_faction(Faction(name='Kingdom of Babylon', fid='babylon'))
game.compile()

while _ < limit:


    # Perform query
    game.map.query(8.15, 40.15)

    game.tick()
    _ += 1
    #time.sleep(1)