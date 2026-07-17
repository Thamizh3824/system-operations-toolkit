from core.resource_monitor import ResourceMonitor


def test_cpu_usage():

    assert isinstance(
        ResourceMonitor.get_cpu_usage(),
        float,
    )


def test_memory_usage():

    assert isinstance(
        ResourceMonitor.get_memory_usage(),
        float,
    )


def test_disk_usage():

    assert isinstance(
        ResourceMonitor.get_disk_usage(),
        float,
    )


def test_network_usage():

    network = ResourceMonitor.get_network_usage()

    assert isinstance(network, dict)


def test_network_keys():

    network = ResourceMonitor.get_network_usage()

    assert "bytes_sent" in network
    assert "bytes_recv" in network