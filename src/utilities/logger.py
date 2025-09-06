import logging
import os

# Base log directory:
# - Use APP_LOG_DIR if set (so you can override in .env or docker-compose)
# - Otherwise default to Airflow's logs path
LOG_DIR = os.getenv("APP_LOG_DIR", "/opt/airflow/logs/custom")

try:
    os.makedirs(LOG_DIR, exist_ok=True)
except PermissionError:
    # Fallback if we don't have permission (e.g. read-only volume)
    LOG_DIR = "/tmp/app_logs"
    os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "fetcher.log")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()  # also show logs in stdout (good for Docker logs)
    ]
)

logger = logging.getLogger(__name__)
