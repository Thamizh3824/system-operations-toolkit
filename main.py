from modules.log_analyzer import LogAnalyzer


def main() -> None:
    analyzer = LogAnalyzer("logs/sample.log")

    parsed_logs = analyzer.parse_logs()

    for log in parsed_logs:
        print(log)


if __name__ == "__main__":
    main()