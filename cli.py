import os

def banner():
    os.system("clear")

    print("=" * 60)
    print("      THREAT INTELLIGENCE AGGREGATOR v2.0")
    print("=" * 60)
    print(" Author  : Ede Chidozie Philip")
    print(" Role    : Cybersecurity | Threat Intelligence")
    print("=" * 60)
    print()


def loading(message):
    print(f"[+] {message}")


def success(message):
    print(f"[✓] {message}")


def warning(message):
    print(f"[!] {message}")


def error(message):
    print(f"[X] {message}")


def separator():
    print("-" * 60)


def finish():
    separator()
    print("[✓] Scan Completed Successfully")
    separator()

