from abc import ABC, abstractmethod


class Modifier(ABC):
    
    def __init__(self, modval, applies_to, ref=None):
        self.modval     = modval
        self.applies_to = applies_to
        self.ref = ref

    @abstractmethod
    def apply(self, value):
        """Apply the modification to the given value."""
        pass


class Multiplier(Modifier):
    def apply(self, value):
        return value * self.modval


class Subtract(Modifier):
    def apply(self, value):
        return value - self.modval


class Addition(Modifier):
    def apply(self, value):
        return value + self.modval
    

class Override(Modifier):
    def apply(self, value):
        return self.modval
    
    
def apply_modifiers(resource_name, base_value, modifiers: list[Modifier]) -> float:
    
    additive = 0
    subtractive = 0
    multiplier = 1.0

    for mod in modifiers:

        if resource_name not in mod.applies_to:
            continue

        if isinstance(mod, Addition):
            additive += mod.modval
        elif isinstance(mod, Subtract):
            subtractive += mod.modval
        elif isinstance(mod, Multiplier):
            multiplier *= mod.modval

    intermediate = base_value + additive - subtractive
    final = intermediate * multiplier
    return final