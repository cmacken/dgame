import toml
from threading import Lock


class SingletonMeta(type):
    _instances = {}
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


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
