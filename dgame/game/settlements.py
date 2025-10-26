from dgame.core.component import Name, Position, Criteria
from dgame.core.criteria import is_forest, is_land
from dgame.core.entity import Entity

# --- Building factory ---
class Settlement:

    # class-level criteria set (used both pre- and post-creation)
    criteria = Criteria([
        ("Must be built on forest terrain", is_land),
    ])

    @staticmethod
    def check(game, x, y):
        return Settlement.criteria.resolve(game, x, y)

    @staticmethod
    def create(x, y):
        e = Entity()
        e.add(Name("Settlement"))
        e.add(Position(x, y))
        e.add(Settlement.criteria)
        return e