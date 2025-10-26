from dataclasses import dataclass, field
from typing import Callable, List, Tuple, Dict, Literal


@dataclass
class Position:
    x: float
    y: float

@dataclass
class Name:
    name: str

@dataclass
class Boundary:
    border: float  # simple circular border for now
    interact: float

@dataclass
class Faction:
    name: str
    fid: int

    def __repr__(self):
        return f'Faction({self.fid})'


@dataclass
class Production:
    inputs: Dict[str, float]
    outputs: Dict[str, float]
    efficiency: float = 1.0

@dataclass
class Criterion:
    description: str
    condition: Callable  # (game, x, y, entity?) -> bool

    def check(self, game, x, y, entity=None) -> Tuple[bool, str]:
        """Return (True/False, description)"""
        ok = self.condition(game, x, y, entity)
        return ok, self.description

@dataclass
class Criteria:
    criteria: List[Criterion] = field(default_factory=list)

    def add(self, description: str, condition: Callable):
        self.criteria.append(Criterion(description, condition))

    def resolve(self, game, x, y, entity=None):
        """
        Evaluate all criteria for a given map position.
        Returns (bool, failed_descriptions)
        """
        failed = []
        for c in self.criteria:
            ok, desc = c.check(game, x, y, entity)
            if not ok:
                failed.append(desc)
        return len(failed) == 0, failed

@dataclass
class Resource:
    rid: str
    name: str
    units: str
    offset: float = 0.0
    scale: float = 1.0

    def dn_to_val(self, value):
        return (value + self.offset) * self.scale
    
    def __eq__(self, other):
        return isinstance(other, Resource) and self.rid == other.rid

    def __hash__(self):
        return hash(self.rid)

    def __repr__(self):
        return f'Resource({self.name})'

@dataclass
class Condition:
    cid: str
    name: str
    units: str
    offset: float = 0.0
    scale: float = 1.0

    def dn_to_val(self, value):
        return (value + self.offset) * self.scale
    
    def __eq__(self, other):
        return isinstance(other, Condition) and self.cid == other.cid

    def __hash__(self):
        return hash(self.cid)

    def __repr__(self):
        return f'Condition({self.name})'

@dataclass
class Terrain:
    dn: str
    name: str
    rgb: tuple
    desc: str

    def __repr__(self):
        return f'Terrain({self.name})'
    
    def __eq__(self, other):
        return isinstance(other, Terrain) and self.rid == other.rid

    def __hash__(self):
        return hash(self.rid)


@dataclass
class ConditionModifier:
    condition: str
    attribute: str
    mode: Literal["linear", "ideal"] = "linear"
    range: Tuple[float, float] = (0.0, 1.0)
    effect_range: Tuple[float, float] = (0.5, 1.5)
    ideal: float | None = None
    width: float | None = None
    clip: bool = True

    def evaluate(self, value: float) -> float:
        vmin, vmax = self.range
        emin, emax = self.effect_range

        if self.mode == "linear":
            t = (value - vmin) / (vmax - vmin)
            if self.clip:
                t = max(0.0, min(1.0, t))
            return emin + t * (emax - emin)

        elif self.mode == "ideal":
            if self.ideal is None or self.width is None:
                raise ValueError("Ideal mode requires ideal and width.")
            dist = abs(value - self.ideal)
            t = max(0.0, 1 - (dist / self.width))
            if self.clip:
                t = max(0.0, t)
            return emin + t * (emax - emin)

        return 1.0

    def describe(self, value: float) -> str:
        eff = self.evaluate(value)
        pct = (eff - 1.0) * 100
        sign = "+" if pct >= 0 else ""
        return f"{self.condition}: {sign}{pct:.1f}%"
    


@dataclass
class ConditionModifiers:
    modifiers: List[ConditionModifier] = field(default_factory=list)

    def get_multiplier(self, game, x, y):
        total = 1.0
        for mod in self.modifiers:
            val = game.read_condition(mod.condition, x, y)
            total *= mod.evaluate(val)
        return total

    def describe(self, game, x, y):
        parts = []
        for mod in self.modifiers:
            val = game.read_condition(mod.condition, x, y)
            parts.append(mod.describe(val))
        return ", ".join(parts)