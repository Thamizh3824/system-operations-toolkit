from pathlib import Path
from datetime import datetime

from core.log_analyzer import LogAnalyzer
from core.alert_engine import AlertEngine
from core.health_checker import HealthChecker
from core.resource_monitor import ResourceMonitor


class ReportGenerator:
    """
    Generates an HTML dashboard.
    """

    def __init__(
        self,
        analyzer: LogAnalyzer,
        alert_engine: AlertEngine,
        health_checker: HealthChecker,
    ) -> None:

        self.analyzer = analyzer
        self.alert_engine = alert_engine
        self.health_checker = health_checker

    def generate_dashboard(self) -> None:

        self.analyzer.count_levels()

        statistics = self.analyzer.statistics
        top_errors = self.analyzer.top_errors()
        alerts = self.alert_engine.check_alerts()
        services = self.health_checker.check_services()

        cpu = ResourceMonitor.get_cpu_usage()
        memory = ResourceMonitor.get_memory_usage()
        disk = ResourceMonitor.get_disk_usage()

        generated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        html = f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<title>System Operations Dashboard</title>

<style>

body {{
    font-family: Arial, Helvetica, sans-serif;
    background:#f5f5f5;
    padding:30px;
}}

.container {{
    max-width:1000px;
    margin:auto;
}}

.card {{
    background:white;
    padding:20px;
    margin-bottom:20px;
    border-radius:10px;
    box-shadow:0 2px 8px rgba(0,0,0,.1);
}}

table {{
    width:100%;
    border-collapse:collapse;
}}

th,td {{
    border:1px solid #ddd;
    padding:10px;
}}

th {{
    background:#0078D7;
    color:white;
}}

.up {{
    color:green;
    font-weight:bold;
}}

.down {{
    color:red;
    font-weight:bold;
}}

.alert {{
    color:red;
}}

.resource {{
    font-size:18px;
}}
.summary{{
    display:flex;
    gap:20px;
    margin-top:20px;
}}

.summary-card{{
    flex:1;
    border-radius:12px;
    padding:20px;
    text-align:center;
    color:white;
}}

.summary-card h3{{
    margin:0;
    font-size:20px;
}}

.summary-card p{{
    font-size:40px;
    margin:10px 0 0;
    font-weight:bold;
}}

.info{{
    background:#1976d2;
}}

.warning{{
    background:#f9a825;
}}

.error{{
    background:#d32f2f;
}}
.badge{{
    padding:6px 14px;
    border-radius:30px;
    color:white;
    font-weight:bold;
}}

.up{{
    background:#2e7d32;
}}

.down{{
    background:#d32f2f;
}}
.progress{{
    width:100%;
    background:#ddd;
    border-radius:20px;
    overflow:hidden;
}}

.bar{{
    height:20px;
    background:#1976d2;
}}

</style>

</head>

<body>

<div class="container">

<h1>System Operations Dashboard</h1>

<div class="card">

<h2>Summary</h2>

<p>Total Logs : {len(self.analyzer.parsed_logs)}</p>

<div class="summary">

<div class="summary-card info">
<h3>INFO</h3>
<p>{statistics.get("INFO",0)}</p>
</div>

<div class="summary-card warning">
<h3>WARNING</h3>
<p>{statistics.get("WARNING",0)}</p>
</div>

<div class="summary-card error">
<h3>ERROR</h3>
<p>{statistics.get("ERROR",0)}</p>
</div>

</div>
</div>

<div class="card">

<h2>Top Recurring Errors</h2>

<table>

<tr>

<th>Error</th>

<th>Count</th>

</tr>
"""

        for message, count in top_errors:

            html += f"""
<tr>

<td>{message}</td>

<td>{count}</td>

</tr>
"""

        html += """
</table>

</div>

<div class="card">

<h2>Alerts</h2>

<ul>
"""

        if alerts:

            for alert in alerts:

                html += f"<li class='alert'>{alert}</li>"

        else:

            html += "<li>No alerts</li>"

        html += """
</ul>

</div>

<div class="card">

<h2>Health Check</h2>

<table>

<tr>

<th>Service</th>

<th>Status</th>

<th>HTTP</th>

<th>Response(ms)</th>

</tr>
"""

        for service in services:

            badge = (
                "<span class='badge up'>UP</span>"
                if service["status"] == "UP"
                else "<span class='badge down'>DOWN</span>"
            )

            html += f"""
<tr>

<td>{service["name"]}</td>

<td>{badge}</td>

<td>{service["status_code"]}</td>

<td>{service["response_time"]}</td>

</tr>
"""

        html += f"""
</table>

</div>

<div class="card">

<h2>System Resources</h2>

<h3>CPU Usage</h3>

<div class="progress">
<div class="bar" style="width:{cpu}%"></div>
</div>

<p>{cpu:.1f}%</p>

<h3>Memory Usage</h3>

<div class="progress">
<div class="bar" style="width:{memory}%"></div>
</div>

<p>{memory:.1f}%</p>

<h3>Disk Usage</h3>

<div class="progress">
<div class="bar" style="width:{disk}%"></div>
</div>

<p>{disk:.1f}%</p>

</div>

<div class="card">

Generated : {generated}

</div>

</div>

</body>

</html>
"""

        report_path = Path("reports/dashboard.html")

        report_path.parent.mkdir(exist_ok=True)

        report_path.write_text(
            html,
            encoding="utf-8",
        )