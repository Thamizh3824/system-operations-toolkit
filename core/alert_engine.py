from utils.config_manager import ConfigManager
from utils.logger import logger


class AlertEngine:
    """
    Evaluates log statistics against configured thresholds.
    """

    def __init__(self, statistics: dict[str, int]) -> None:
        self.statistics = statistics

    def check_alerts(self) -> list[str]:
        """
        Check log statistics against configured thresholds.

        Returns:
            List of alert messages.
        """

        config = ConfigManager.load()
        thresholds = config["thresholds"]

        alerts = []

        for level, threshold in thresholds.items():

            actual = self.statistics.get(level, 0)

            if actual >= threshold:

                logger.warning(
                    "%s threshold exceeded (%d)",
                    level,
                    actual,
                )

                alerts.append(
                    f"{level} count ({actual}) exceeded threshold ({threshold})"
                )

        return alerts