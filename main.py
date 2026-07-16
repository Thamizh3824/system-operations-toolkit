import argparse

from modules.log_analyzer import LogAnalyzer


def main() -> None:

    parser = argparse.ArgumentParser(
        description="System Operations Toolkit"
    )

    parser.add_argument(
        "command",
        choices=[
            "summary",
            "export",
            "filter",
        ],
        help="Command to execute"
    )

    parser.add_argument(
        "level",
        nargs="?",
        help="Log level for filter command"
    )

    args = parser.parse_args()

    analyzer = LogAnalyzer("logs/sample.log")

    if args.command == "summary":
        analyzer.display_summary()

    elif args.command == "export":
        analyzer.export_csv()

    elif args.command == "filter":

        if not args.level:
            print("Please provide a log level.")
            return

        logs = analyzer.filter_logs(args.level)

        print(f"\n{args.level.upper()} Logs\n")

        for log in logs:
            print(
                f"{log['timestamp']} | "
                f"{log['level']} | "
                f"{log['message']}"
            )


if __name__ == "__main__":
    main()