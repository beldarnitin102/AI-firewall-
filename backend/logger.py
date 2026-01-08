import logging

logging.basicConfig(
    filename="firewall.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("AI_FIREWALL")
