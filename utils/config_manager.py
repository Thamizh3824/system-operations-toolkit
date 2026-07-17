import json
from pathlib import Path
from utils.logger import logger

class ConfigManager:
    """
    Handles application configuration.
    """

    CONFIG_PATH = Path("config/config.json")

    @classmethod
    def load(cls) -> dict:
        """
        Load configuration from JSON.
        """

        with cls.CONFIG_PATH.open(
            "r",
            encoding="utf-8"
        ) as file:
            config = json.load(file)

        logger.info("Configuration loaded")

        return config