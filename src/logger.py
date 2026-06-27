import logging
from src.config import config

def get_logger(name: str) -> logging.Logger:
    """
    Creates and configures a logger for the given module name.
    """
    logger = logging.getLogger(name)
    
    # Only configure if it doesn't already have handlers to avoid duplicate logs
    if not logger.handlers:
        level = getattr(logging, config.LOG_LEVEL, logging.INFO)
        logger.setLevel(level)
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | [%(name)s] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        
    return logger
