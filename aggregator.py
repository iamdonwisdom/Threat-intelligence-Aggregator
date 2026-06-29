import os
import json
import requests
from cli import banner, loading, success, finish
from parser import parse_feed
from report_generator import (
    generate_text_report,
    generate_csv_report,
    generate_html_report
)
from logger import log_info, log_error
from exporter import export_iocs

# Create feeds directory if it doesn't exist
os.makedirs("feeds", exist_ok=True)


def load_config():
    """
    Load configuration from config.json
    """
    try:
        with open("config.json", "r", encoding="utf-8") as file:
            config = json.load(file)

        log_info("Configuration loaded successfully")
        return config

    except FileNotFoundError:
        log_error("config.json not found.")
        print("[!] Error: config.json not found.")
        exit()

    except json.JSONDecodeError:
        log_error("Invalid JSON format in config.json")
        print("[!] Error: Invalid JSON format.")
        exit()


def download_feed(name, url):

    try:

        print(f"[+] Downloading {name}...")
        log_info(f"Downloading {name} feed")

        response = requests.get(url, timeout=20)
        response.raise_for_status()

        filename = f"feeds/{name}.txt"

        with open(filename, "w", encoding="utf-8") as file:
            file.write(response.text)

        print(f"[✓] Saved to {filename}")
        log_info(f"{name} feed saved successfully")

    except requests.exceptions.RequestException as error:

        print(f"[!] Failed to download {name}: {error}")
        log_error(f"Failed downloading {name}: {error}")



def main():
    banner()

    log_info("Application Started")

    config = load_config()
    feeds = config["feeds"]

    print("=" * 60)
    print(" Threat Intelligence Aggregator v1.0")
    print("=" * 60)

    summary = {}
    total_indicators = 0

    for name, url in feeds.items():
        download_feed(name, url)

    print("\n" + "=" * 60)
    print("Threat Intelligence Summary")
    print("=" * 60)

    for name in feeds.keys():

        indicators = parse_feed(f"feeds/{name}.txt")

        export_iocs(indicators)

        total = len(indicators)
        total_indicators += total

        urls = sum(1 for item in indicators if item["type"] == "URL")
        ips = sum(1 for item in indicators if item["type"] == "IP Address")
        domains = sum(1 for item in indicators if item["type"] == "Domain")
        unknown = sum(1 for item in indicators if item["type"] == "Unknown")

        summary[name] = {
            "total": total,
            "urls": urls,
            "ips": ips,
            "domains": domains,
            "unknown": unknown
        }

        print(f"\n{name.upper()}")
        print("-" * 30)
        print(f"Total Indicators : {total:,}")
        print(f"URLs             : {urls:,}")
        print(f"IP Addresses     : {ips:,}")
        print(f"Domains          : {domains:,}")
        print(f"Unknown          : {unknown:,}")

    print("\n" + "=" * 60)
    print(f"TOTAL INDICATORS : {total_indicators:,}")
    print("=" * 60)

    generate_text_report(summary)
    generate_csv_report(summary)
    generate_html_report(summary)

    print("[✓] Text report saved to reports/threat_report.txt")
    print("[✓] CSV report saved to reports/threat_report.csv")
    print("[✓] HTML dashboard saved to reports/dashboard.html")

    log_info("Reports generated successfully")
    log_info("IOC files exported successfully")
    log_info("Application Finished")
    finish()


if __name__ == "__main__":
    main()
