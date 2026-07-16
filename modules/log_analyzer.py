from pathlib import Path


class LogAnalyzer:
    """
    Analyze application log files.
    """

    def __init__(self, log_path: str) -> None:
        self.log_path = Path(log_path)

    def validate_file(self) -> bool:
        """
        Validate that the log file exists.

        Returns:
            bool: True if file exists.

        Raises:
            FileNotFoundError: If the file does not exist.
        """

        if not self.log_path.exists():
            raise FileNotFoundError(
                f"Log file not found: {self.log_path}"
            )

        return True