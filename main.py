from modules.log_analyzer import LogAnalyzer


def main() -> None:
    analyzer = LogAnalyzer("logs/sample.log")

    analyzer.display_summary()

    analyzer.export_csv()


if __name__ == "__main__":
    main()