import os
import csv
from datetime import datetime

# Create reports directory
os.makedirs("reports", exist_ok=True)


def generate_text_report(summary):

    filename = "reports/threat_report.txt"

    with open(filename, "w", encoding="utf-8") as report:

        report.write("=" * 60 + "\n")
        report.write("Threat Intelligence Aggregator Report\n")
        report.write("=" * 60 + "\n\n")

        report.write(f"Generated: {datetime.now()}\n\n")

        total = 0

        for feed, stats in summary.items():

            report.write(f"{feed.upper()}\n")
            report.write("-" * 30 + "\n")

            report.write(f"Total Indicators : {stats['total']}\n")
            report.write(f"URLs             : {stats['urls']}\n")
            report.write(f"IP Addresses     : {stats['ips']}\n")
            report.write(f"Domains          : {stats['domains']}\n")
            report.write(f"Unknown          : {stats['unknown']}\n\n")

            total += stats["total"]

        report.write("=" * 60 + "\n")
        report.write(f"TOTAL INDICATORS : {total}\n")
        report.write("=" * 60 + "\n")

    print(f"[✓] Text report saved to {filename}")


def generate_csv_report(summary):

    filename = "reports/threat_report.csv"

    with open(filename, "w", newline="", encoding="utf-8") as csvfile:

        writer = csv.writer(csvfile)

        writer.writerow([
            "Feed",
            "Total Indicators",
            "URLs",
            "IP Addresses",
            "Domains",
            "Unknown"
        ])

        for feed, stats in summary.items():

            writer.writerow([
                feed.upper(),
                stats["total"],
                stats["urls"],
                stats["ips"],
                stats["domains"],
                stats["unknown"]
            ])

    print(f"[✓] CSV report saved to {filename}")


def generate_html_report(summary):

    filename = "reports/dashboard.html"

    total = sum(stats["total"] for stats in summary.values())

    html = f"""
<!DOCTYPE html>
<html>
<head>
<title>Threat Intelligence Dashboard</title>

<style>

body {{
    font-family: Arial, sans-serif;
    background: #f4f6f8;
    margin:40px;
}}

h1 {{
    color:#1f2937;
}}

table {{
    border-collapse: collapse;
    width:100%;
}}

th {{
    background:#2563eb;
    color:white;
    padding:12px;
}}

td {{
    border:1px solid #ddd;
    padding:10px;
    text-align:center;
}}

tr:nth-child(even){{
    background:#f2f2f2;
}}

.card{{
    background:white;
    padding:20px;
    border-radius:10px;
    box-shadow:0 0 10px rgba(0,0,0,.15);
}}

</style>

</head>

<body>

<div class="card">

<h1>Threat Intelligence Dashboard</h1>

<p><strong>Generated:</strong> {datetime.now()}</p>

<h2>Total Indicators: {total:,}</h2>

<table>

<tr>
<th>Feed</th>
<th>Total</th>
<th>URLs</th>
<th>IPs</th>
<th>Domains</th>
<th>Unknown</th>
</tr>
"""

    for feed, stats in summary.items():

        html += f"""
<tr>
<td>{feed.upper()}</td>
<td>{stats['total']}</td>
<td>{stats['urls']}</td>
<td>{stats['ips']}</td>
<td>{stats['domains']}</td>
<td>{stats['unknown']}</td>
</tr>
"""

    html += """
</table>

</div>

</body>

</html>
"""

    with open(filename, "w", encoding="utf-8") as file:
        file.write(html)

    print(f"[✓] HTML dashboard saved to {filename}")
