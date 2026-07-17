from pathlib import Path
from collections import Counter
import csv
from datetime import datetime
from models.log_entry import LogEntry
import json
from utils.logger import logger


class LogAnalyzer:
    """
    Analyze application log files.
    """

    def __init__(self, log_path: str) -> None:
        self.log_path = Path(log_path)
        self.log_entries: list[str] = []
        self.parsed_logs: list[LogEntry] = []
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
    
    def parse_logs(self) -> list[LogEntry]:
        """
        Parse log entries into structured dictionaries.

        Returns:
            list[LogEntry]
        """

        if not self.log_entries:
            self.read_log()

        self.parsed_logs = []

        for entry in self.log_entries:

            parts = entry.split(" ", 3)

            if len(parts) < 4:
                continue

            timestamp = datetime.strptime(
                f"{parts[0]} {parts[1]}",
                "%Y-%m-%d %H:%M:%S"
            )
            level = parts[2]
            message = parts[3]

            self.parsed_logs.append(
                LogEntry(
                    timestamp=timestamp,
                    level=level,
                    message=message,
                )
            )
        logger.info(
            "Parsed %d log entries",
            len(self.parsed_logs),
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
            log.level
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

        report_path = Path("reports/log_report.csv")

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
            rows = [
                {
                    "timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "level": log.level,
                    "message": log.message,
                }
                for log in self.parsed_logs
            ]

            writer.writerows(rows)

            logger.info(
                "CSV exported to reports/log_report.csv"
            )

        print(f"\nCSV report generated: {report_path}")

    def filter_logs(self, level: str) -> list[LogEntry]:
        """
        Filter log entries by severity level.

        Args:
            level (str): INFO, WARNING or ERROR.

        Returns:
            list[LogEntry]
        """

        if not self.parsed_logs:
            self.parse_logs()

        level = level.upper()

        return [
            log
            for log in self.parsed_logs
            if log.level == level
        ]
    
    def search_logs(self, keyword: str) -> list[LogEntry]:
        """
        Search log messages for a keyword.

        Args:
            keyword: Text to search for.

        Returns:
            Matching log entries.
        """

        if not self.parsed_logs:
            self.parse_logs()

        keyword = keyword.lower()

        return [
            log
            for log in self.parsed_logs
            if keyword in log.message.lower()
        ]
    
    def filter_by_date(self, date: str) -> list[LogEntry]:
        """
        Filter logs by a specific date.

        Args:
            date: Date in YYYY-MM-DD format.

        Returns:
            Matching log entries.
        """

        if not self.parsed_logs:
            self.parse_logs()

        return [
            log
            for log in self.parsed_logs
            if log.timestamp.strftime("%Y-%m-%d") == date
        ]
    
    def filter_after(self, timestamp: str) -> list[LogEntry]:
        """
        Return logs after the given timestamp.
        """

        if not self.parsed_logs:
            self.parse_logs()

        target = datetime.strptime(
            timestamp,
            "%Y-%m-%d %H:%M:%S",
        )

        return [
            log
            for log in self.parsed_logs
            if log.timestamp >= target
        ]
    
    def filter_before(self, timestamp: str) -> list[LogEntry]:
        """
        Return logs before the given timestamp.
        """

        if not self.parsed_logs:
            self.parse_logs()

        target = datetime.strptime(
            timestamp,
            "%Y-%m-%d %H:%M:%S",
        )

        return [
            log
            for log in self.parsed_logs
            if log.timestamp <= target
        ]
    
        
    def top_errors(self, limit: int = 5) -> list[tuple[str, int]]:
        """
        Return the most frequent ERROR messages.

        Args:
            limit: Maximum number of results.

        Returns:
            List of (error_message, count).
        """

        if not self.parsed_logs:
            self.parse_logs()

        error_counter = Counter(
            log.message
            for log in self.parsed_logs
            if log.level == "ERROR"
        )

        return error_counter.most_common(limit)