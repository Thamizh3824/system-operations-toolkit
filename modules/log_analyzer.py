from pathlib import Path
from collections import Counter
import csv

class LogAnalyzer:
    """
    Analyze application log files.
    """

    def __init__(self, log_path: str) -> None:
        self.log_path = Path(log_path)
        self.log_entries: list[str] = []
        self.parsed_logs: list[dict[str, str]] = []
        self.statistics: Counter[str] = Counter()

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
    
    def parse_logs(self) -> list[dict[str, str]]:
        """
        Parse log entries into structured dictionaries.

        Returns:
            list[dict[str, str]]
        """

        if not self.log_entries:
            self.read_log()

        self.parsed_logs = []

        for entry in self.log_entries:

            parts = entry.split(" ", 3)

            if len(parts) < 4:
                continue

            timestamp = f"{parts[0]} {parts[1]}"
            level = parts[2]
            message = parts[3]

            self.parsed_logs.append(
                {
                    "timestamp": timestamp,
                    "level": level,
                    "message": message,
                }
            )

        return self.parsed_logs
    
    def count_levels(self) -> Counter[str]:
        """
        Count the occurrence of each log level.

        Returns:
            Counter[str]: Frequency of each log level.
        """

        if not self.parsed_logs:
            self.parse_logs()

        self.statistics = Counter(
            log["level"]
            for log in self.parsed_logs
        )

        return self.statistics
    
    def display_summary(self) -> None:
        """
        Display a formatted log summary.
        """

        if not self.statistics:
            self.count_levels()

        print("\n========== Log Summary ==========")
        print(f"Total Entries : {len(self.parsed_logs)}\n")

        for level in ["INFO", "WARNING", "ERROR"]:
            print(f"{level:<14}: {self.statistics.get(level, 0)}")

        print("=" * 33)

    def export_csv(self) -> None:
        """
        Export parsed log entries to a CSV report.
        """

        if not self.parsed_logs:
            self.parse_logs()

        report_path = Path("logs/reports/log_report.csv")

        report_path.parent.mkdir(parents=True, exist_ok=True)

        with report_path.open(
            "w",
            newline="",
            encoding="utf-8"
        ) as csv_file:

            writer = csv.DictWriter(
                csv_file,
                fieldnames=[
                    "timestamp",
                    "level",
                    "message"
                ]
            )

            writer.writeheader()
            writer.writerows(self.parsed_logs)

        print(f"\nCSV report generated: {report_path}")

    def filter_logs(self, level: str) -> list[dict[str, str]]:
        """
        Filter log entries by severity level.

        Args:
            level (str): INFO, WARNING or ERROR.

        Returns:
            list[dict[str, str]]
        """

        if not self.parsed_logs:
            self.parse_logs()

        level = level.upper()

        return [
            log
            for log in self.parsed_logs
            if log["level"] == level
        ]