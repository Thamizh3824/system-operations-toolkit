import json
from pathlib import Path


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
            return json.load(file)