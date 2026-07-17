from pathlib import Path
import csv
import pytest

from core.log_analyzer import LogAnalyzer
from models.log_entry import LogEntry


LOG_FILE = "tests/sample_test.log"
INVALID_LOG_FILE = "tests/invalid_test.log"


# -------------------------
# Constructor
# -------------------------

def test_log_analyzer_creation():
    analyzer = LogAnalyzer(LOG_FILE)
    assert analyzer is not None


def test_log_path_is_path():
    analyzer = LogAnalyzer(LOG_FILE)
    assert isinstance(analyzer.log_path, Path)


def test_initial_log_entries_empty():
    analyzer = LogAnalyzer(LOG_FILE)
    assert analyzer.log_entries == []


def test_initial_parsed_logs_empty():
    analyzer = LogAnalyzer(LOG_FILE)
    assert analyzer.parsed_logs == []


def test_initial_statistics_empty():
    analyzer = LogAnalyzer(LOG_FILE)
    assert len(analyzer.statistics) == 0


# -------------------------
# Validation
# -------------------------

def test_validate_existing_file():
    analyzer = LogAnalyzer(LOG_FILE)
    assert analyzer.validate_file() is True


def test_validate_missing_file():
    analyzer = LogAnalyzer("tests/missing.log")

    with pytest.raises(FileNotFoundError):
        analyzer.validate_file()


# -------------------------
# Reading
# -------------------------

def test_read_logs():
    analyzer = LogAnalyzer(LOG_FILE)

    logs = analyzer.read_log()

    assert len(logs) == 8


# -------------------------
# Parsing
# -------------------------

def test_parse_logs_returns_logentry():
    analyzer = LogAnalyzer(LOG_FILE)

    logs = analyzer.parse_logs()

    assert isinstance(logs[0], LogEntry)


def test_parse_log_count():
    analyzer = LogAnalyzer(LOG_FILE)

    logs = analyzer.parse_logs()

    assert len(logs) == 8


def test_invalid_logs_skipped():
    analyzer = LogAnalyzer(INVALID_LOG_FILE)

    logs = analyzer.parse_logs()

    assert len(logs) == 1


# -------------------------
# Statistics
# -------------------------

def test_count_levels():
    analyzer = LogAnalyzer(LOG_FILE)

    stats = analyzer.count_levels()

    assert stats["INFO"] == 3
    assert stats["WARNING"] == 2
    assert stats["ERROR"] == 3


# -------------------------
# Filter
# -------------------------

def test_filter_info():
    analyzer = LogAnalyzer(LOG_FILE)

    logs = analyzer.filter_logs("INFO")

    assert len(logs) == 3


def test_filter_warning():
    analyzer = LogAnalyzer(LOG_FILE)

    logs = analyzer.filter_logs("WARNING")

    assert len(logs) == 2


def test_filter_error():
    analyzer = LogAnalyzer(LOG_FILE)

    logs = analyzer.filter_logs("ERROR")

    assert len(logs) == 3


# -------------------------
# Search
# -------------------------

def test_search_existing_keyword():
    analyzer = LogAnalyzer(LOG_FILE)

    logs = analyzer.search_logs("database")

    assert len(logs) == 2


def test_search_case_insensitive():
    analyzer = LogAnalyzer(LOG_FILE)

    logs = analyzer.search_logs("DATABASE")

    assert len(logs) == 2


def test_search_missing_keyword():
    analyzer = LogAnalyzer(LOG_FILE)

    logs = analyzer.search_logs("python")

    assert logs == []


# -------------------------
# Date
# -------------------------

def test_filter_by_date():
    analyzer = LogAnalyzer(LOG_FILE)

    logs = analyzer.filter_by_date("2026-07-15")

    assert len(logs) == 6


def test_filter_after():
    analyzer = LogAnalyzer(LOG_FILE)

    logs = analyzer.filter_after("2026-07-16 00:00:00")

    assert len(logs) == 2


def test_filter_before():
    analyzer = LogAnalyzer(LOG_FILE)

    logs = analyzer.filter_before("2026-07-15 09:01:00")

    assert len(logs) == 4


# -------------------------
# Top Errors
# -------------------------

def test_top_errors():
    analyzer = LogAnalyzer(LOG_FILE)

    errors = analyzer.top_errors()

    assert errors[0][0] == "Database connection failed"
    assert errors[0][1] == 2


def test_top_errors_limit():
    analyzer = LogAnalyzer(LOG_FILE)

    errors = analyzer.top_errors(limit=1)

    assert len(errors) == 1


# -------------------------
# CSV
# -------------------------

def test_export_csv():
    analyzer = LogAnalyzer(LOG_FILE)

    analyzer.export_csv()

    report = Path("reports/log_report.csv")

    assert report.exists()


def test_export_csv_header():
    analyzer = LogAnalyzer(LOG_FILE)

    analyzer.export_csv()

    with open("reports/log_report.csv", newline="", encoding="utf-8") as f:

        reader = csv.reader(f)

        header = next(reader)

    assert header == ["timestamp", "level", "message"]

#-------------------------
# Summary
#-------------------------

def test_display_summary(capsys):
    analyzer = LogAnalyzer(LOG_FILE)

    analyzer.display_summary()

    captured = capsys.readouterr()

    assert "Log Summary" in captured.out
    assert "INFO" in captured.out
    assert "WARNING" in captured.out
    assert "ERROR" in captured.out