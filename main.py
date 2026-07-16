from modules.log_analyzer import LogAnalyzer


def main() -> None:
    analyzer = LogAnalyzer("logs/sample.log")

    logs = analyzer.read_log()

    print(f"Successfully loaded {len(logs)} log entries.\n")

    for log in logs:
        print(log)


if __name__ == "__main__":
    main()