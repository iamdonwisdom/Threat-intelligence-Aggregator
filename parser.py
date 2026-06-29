import os
import re
from urllib.parse import urlparse

# Regular expression for IPv4 addresses
ip_pattern = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$")


def classify_indicator(indicator):
    indicator = indicator.strip()

    # URL
    if indicator.startswith("http://") or indicator.startswith("https://"):
        return "URL"

    # IP Address
    if ip_pattern.match(indicator):
        return "IP Address"

    # Domain
    parsed = urlparse("http://" + indicator)
    if parsed.hostname and "." in parsed.hostname:
        return "Domain"

    return "Unknown"


def parse_feed(filepath):
    indicators = []

    if not os.path.exists(filepath):
        return indicators

    with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            indicator_type = classify_indicator(line)

            indicators.append({
                "value": line,
                "type": indicator_type
            })

    return indicators
