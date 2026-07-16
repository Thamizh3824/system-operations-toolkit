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
            "search",
            "date",
            "after",
            "before",
            "alerts",
        ],
        help="Command to execute"
    )

    parser.add_argument(
        "value",
        nargs="?",
        help="Argument for the selected command"
    )

    args = parser.parse_args()

    analyzer = LogAnalyzer("logs/sample.log")

    if args.command == "summary":
        analyzer.display_summary()

    elif args.command == "export":
        analyzer.export_csv()

    elif args.command == "filter":

        if not args.value:
            print("Please provide a log level.")
            return

        logs = analyzer.filter_logs(args.value)

        print(f"\n{args.value.upper()} Logs\n")

        for log in logs:
            print(
                f"{log.timestamp} | "
                f"{log.level} | "
                f"{log.message}"
            )
    elif args.command == "search":

        if not args.value:
            print("Please provide a keyword.")
            return

        logs = analyzer.search_logs(args.value)

        print(f"\nSearch Results for '{args.value}'\n")

        if not logs:
            print("No matching log entries found.")
            return

        for log in logs:
            print(
                f"{log.timestamp} | "
                f"{log.level} | "
                f"{log.message}"
            )
    elif args.command == "date":

        if not args.value:
            print("Please provide a date (YYYY-MM-DD).")
            return

        logs = analyzer.filter_by_date(args.value)

        print(f"\nLogs for {args.value}\n")

        for log in logs:
            print(
                f"{log.timestamp.strftime('%Y-%m-%d %H:%M:%S')} | "
                f"{log.level} | "
                f"{log.message}"
            )

    elif args.command == "after":

        if not args.value:
            print("Please provide a timestamp.")
            return

        logs = analyzer.filter_after(args.value)

        print(f"\nLogs after {args.value}\n")

        for log in logs:
            print(
                f"{log.timestamp.strftime('%Y-%m-%d %H:%M:%S')} | "
                f"{log.level} | "
                f"{log.message}"
            )

    elif args.command == "before":

        if not args.value:
            print("Please provide a timestamp.")
            return

        logs = analyzer.filter_before(args.value)

        print(f"\nLogs before {args.value}\n")

        for log in logs:
            print(
                f"{log.timestamp.strftime('%Y-%m-%d %H:%M:%S')} | "
                f"{log.level} | "
                f"{log.message}"
            )

    elif args.command == "alerts":

        alerts = analyzer.check_alerts()

        print("\n========== Alerts ==========\n")

        if not alerts:
            print("No alerts.")
        else:
            for alert in alerts:
                print(f"🚨 {alert}")

        print("\n============================")


if __name__ == "__main__":
    main()