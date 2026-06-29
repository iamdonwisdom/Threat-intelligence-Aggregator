import os

# Create exports directory if it doesn't exist
os.makedirs("exports", exist_ok=True)


def export_iocs(indicators):

    urls = []
    domains = []
    ip_addresses = []
    unknown = []

    for item in indicators:

        if item["type"] == "URL":
            urls.append(item["value"])

        elif item["type"] == "Domain":
            domains.append(item["value"])

        elif item["type"] == "IP Address":
            ip_addresses.append(item["value"])

        else:
            unknown.append(item["value"])

    save_file("exports/urls.txt", urls)
    save_file("exports/domains.txt", domains)
    save_file("exports/ip_addresses.txt", ip_addresses)
    save_file("exports/unknown.txt", unknown)


def save_file(filename, data):

    with open(filename, "w", encoding="utf-8") as file:

        for item in sorted(set(data)):
            file.write(item + "\n")
