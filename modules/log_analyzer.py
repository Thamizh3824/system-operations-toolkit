from pathlib import Path


class LogAnalyzer:
    """
    Analyze application log files.
    """

    def __init__(self, log_path: str) -> None:
        self.log_path = Path(log_path)
        self.log_entries: list[str] = []

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
    
    def read_log(self) -> list[str]:
        """
        Read all log entries from the log file.

        Returns:
            list[str]: List of log entries.
        """

        self.validate_file()

        with self.log_path.open("r", encoding="utf-8") as file:
            self.log_entries = [
                line.strip()
                for line in file
                if line.strip()
            ]

        return self.log_entries