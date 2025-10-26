from dgame.core.component import Name, Position, Criteria, Production, ConditionModifier, ConditionModifiers
from dgame.core.criteria import is_forest, is_land
from dgame.core.entity import Entity

class LumberCamp:
    criteria = Criteria([
        ("Must be built on forest terrain", is_forest),
        ("Must be built on land", is_land),
    ])

    @staticmethod
    def check(game, x, y):
        return LumberCamp.criteria.resolve(game, x, y)

    @staticmethod
    def create(x, y):
        e = Entity()
        e.add(Name("Lumber Camp"))
        e.add(Position(x, y))
        e.add(LumberCamp.criteria)

        # production baseline
        e.add(Production(inputs={}, outputs={"wood": 5}, efficiency=1.0))

        # condition-based modifiers
        e.add(ConditionModifiers([
            ConditionModifier(
                condition="rainfall",
                attribute="efficiency",
                mode="linear",
                range=(200, 1000),
                effect_range=(0.8, 1.2),
            ),
            ConditionModifier(
                condition="temp",
                attribute="efficiency",
                mode="ideal",
                ideal=20,
                width=10,
                effect_range=(0.5, 1.5),
            )
        ]))

        return e