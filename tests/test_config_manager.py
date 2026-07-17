from utils.config_manager import ConfigManager


def test_load_config():

    config = ConfigManager.load()

    assert isinstance(config, dict)


def test_thresholds_exist():

    config = ConfigManager.load()

    assert "thresholds" in config


def test_services_exist():

    config = ConfigManager.load()

    assert "services" in config