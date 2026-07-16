import psutil


class ResourceMonitor:
    """
    Monitor local system resources.
    """

    @staticmethod
    def get_cpu_usage() -> float:
        """
        Return CPU usage percentage.
        """
        return psutil.cpu_percent(interval=1)


    @staticmethod
    def get_memory_usage() -> float:
        """
        Return memory usage percentage.
        """
        return psutil.virtual_memory().percent


    @staticmethod
    def get_disk_usage() -> float:
        """
        Return disk usage percentage.
        """
        return psutil.disk_usage("/").percent