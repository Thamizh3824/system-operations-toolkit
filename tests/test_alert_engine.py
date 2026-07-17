from collections import Counter

from core.alert_engine import AlertEngine


def test_error_threshold_exceeded():

    stats = Counter(
        {
            "INFO": 2,
            "WARNING": 1,
            "ERROR": 5,
        }
    )

    alerts = AlertEngine(stats).check_alerts()

    assert len(alerts) > 0


def test_no_alerts():

    stats = Counter(
        {
            "INFO": 1,
            "WARNING": 0,
            "ERROR": 0,
        }
    )

    alerts = AlertEngine(stats).check_alerts()

    assert alerts == []


def test_empty_statistics():

    alerts = AlertEngine(Counter()).check_alerts()

    assert isinstance(alerts, list)


def test_statistics_type():

    stats = Counter(
        {
            "ERROR": 2
        }
    )

    engine = AlertEngine(stats)

    assert engine.statistics["ERROR"] == 2