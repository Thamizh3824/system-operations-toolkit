import time
import requests

from modules.config_manager import ConfigManager


class HealthChecker:
    """
    Monitor configured HTTP services.
    """

    def __init__(self) -> None:
        
        self.config = ConfigManager.load()

    def check_services(self) -> list[dict]:

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

                results.append(
                    {
                        "name": service["name"],
                        "status": "UP",
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