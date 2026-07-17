import time
import requests

from utils.config_manager import ConfigManager
from typing import Any


class HealthChecker:
    """
    Monitor configured HTTP services.
    """

    def __init__(self) -> None:
        
        self.config = ConfigManager.load()

    def check_services(self) -> list[dict[str, Any]]:

        results = []

        for service in self.config["services"]:

            start = time.perf_counter()

            try:

                response = requests.get(
                    service["url"],
                    timeout=5,
                )

                elapsed = (
                    time.perf_counter() - start
                ) * 1000

                status = "UP" if response.ok else "DOWN"

                results.append(
                    {
                        "name": service["name"],
                        "status": status,
                        "status_code": response.status_code,
                        "response_time": round(elapsed, 2),
                    }
                )

            except requests.RequestException:
                

                results.append(
                    {
                        "name": service["name"],
                        "status": "DOWN",
                        "status_code": "-",
                        "response_time": "Timeout",
                    }
                )

        return results