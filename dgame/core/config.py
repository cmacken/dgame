import json
from importlib.resources import files
from dgame.core.utils import get_logger

logger = get_logger(__name__)

class Config:
    
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            logger.info('Loading global configuration...')
            cls._instance = super().__new__(cls)
            cls._instance._load_default_config()
        return cls._instance

    def _load_default_config(self):
        # Access embedded config file
        config_path = files("dgame") / "config.json"
        with config_path.open("r") as f:
            self._config = json.load(f)

    def get(self, *keys, default=None):
        """Retrieve a value from nested dicts using a sequence of keys."""
        d = self._config
        for k in keys:
            if not isinstance(d, dict) or k not in d:
                return default
            d = d[k]
        return d

    def set(self, *keys, value):
        """Set a value in nested dicts, creating intermediate dicts if needed."""
        d = self._config
        for k in keys[:-1]:
            if k not in d or not isinstance(d[k], dict):
                d[k] = {}
            d = d[k]
        d[keys[-1]] = value

    def as_dict(self):
        return self._config.copy()