import logging
import os
from logging.handlers import RotatingFileHandler

def configuration_logging(logs_path: str = "logs/my_log.log", logging_level: int = logging.INFO):
    log_dir = os.path.dirname(logs_path)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
        
    fileHandler = RotatingFileHandler(logs_path, maxBytes=1024, backupCount=5) # 5 MB per file, 5 backup files
    consoleHandler = logging.StreamHandler()
    logging.basicConfig(
        level=logging_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            fileHandler,
            consoleHandler
        ]
    )