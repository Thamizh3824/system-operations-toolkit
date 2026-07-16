from modules.log_analyzer import LogAnalyzer


def main() -> None:
    analyzer = LogAnalyzer("logs/sample.log")
    analyzer.validate_file()
    print("Log file found.")


if __name__ == "__main__":
    main()