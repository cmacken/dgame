import logging

def get_logger(name: str = None):
    """Return a shared project logger."""
    logger = logging.getLogger(name or "project")
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            handlers=[
                logging.FileHandler("app.log", mode="a"),
                logging.StreamHandler(),
            ],
        )
    return logger