import os
import logging

# Create logs directory
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("ThreatIntel")


def log_info(message):
    logger.info(message)


def log_error(message):
    logger.error(message)
