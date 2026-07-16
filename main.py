from modules.log_analyzer import LogAnalyzer


def main() -> None:
    analyzer = LogAnalyzer("logs/sample.log")

    analyzer.display_summary()

    analyzer.export_csv()

    print("\nERROR Logs\n")

    error_logs = analyzer.filter_logs("ERROR")

    for log in error_logs:
        print(
            f"{log['timestamp']} | "
            f"{log['level']} | "
            f"{log['message']}"
        )


if __name__ == "__main__":
    main()