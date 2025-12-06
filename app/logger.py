
import logging

def get_logger():
    logger=logging.getLogger("app")
    if not logger.handlers:
        handler=logging.StreamHandler()
        fmt=logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(fmt)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
