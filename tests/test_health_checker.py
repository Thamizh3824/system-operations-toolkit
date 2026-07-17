from unittest.mock import patch, Mock

from core.health_checker import HealthChecker
import requests


@patch("requests.get")
def test_service_up(mock_get):

    response = Mock()

    response.status_code = 200

    mock_get.return_value = response

    checker = HealthChecker()

    results = checker.check_services()

    assert results[0]["status"] == "UP"


@patch("requests.get")
def test_service_down(mock_get):

    mock_get.side_effect = requests.RequestException()

    checker = HealthChecker()

    results = checker.check_services()

    assert results[0]["status"] == "DOWN"