from loguru import logger
import sys

LOG_FILE = "service.log"

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time} {level} {message}")
logger.add(LOG_FILE, rotation="1 week", level="INFO", format="{time} {level} {message}")

def get_logger():
    """Возвращает настроенный logger."""
    return logger
