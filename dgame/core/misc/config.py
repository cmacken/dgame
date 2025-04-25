import toml
from dgame.core.misc.singleton import SingletonMeta

class Config(metaclass=SingletonMeta):
    
    def __init__(self, filepath="config.toml"):
        self._config = toml.load(filepath)

    def get(self, key, default=None):
        """Access nested keys using dot notation."""
        keys = key.split(".")
        val = self._config
        for k in keys:
            val = val.get(k)
            if val is None:
                return default
        return val

    def as_dict(self):
        return self._config
