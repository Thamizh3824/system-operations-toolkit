import argparse

from modules.log_analyzer import LogAnalyzer
from modules.health_checker import HealthChecker
from modules.resource_monitor import ResourceMonitor


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
            "health",
            "top-errors",
            "monitor",
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

    elif args.command == "health":

        checker = HealthChecker()

        results = checker.check_services()

        print("\n========== Service Health ==========\n")

        print(
            f"{'Service':<20}"
            f"{'Status':<10}"
            f"{'Time(ms)':<12}"
            f"{'HTTP'}"
        )

        print("-" * 50)

        for result in results:

            print(
                f"{result['name']:<20}"
                f"{result['status']:<10}"
                f"{str(result['response_time']):<12}"
                f"{result['status_code']}"
            )

        print("\n====================================")

    elif args.command == "top-errors":

        errors = analyzer.top_errors()

        print("\n========== Top Recurring Errors ==========\n")

        if not errors:
            print("No ERROR logs found.")
        else:
            for message, count in errors:
                print(f"{message:<40} {count}")

        print("\n==========================================")

    elif args.command == "monitor":

        monitor = ResourceMonitor()

        print("\n========== System Resources ==========\n")

        print(f"CPU Usage      : {monitor.get_cpu_usage():.1f}%")
        print(f"Memory Usage   : {monitor.get_memory_usage():.1f}%")
        print(f"Disk Usage     : {monitor.get_disk_usage():.1f}%")

        print("\n======================================")
    
if __name__ == "__main__":
    main()