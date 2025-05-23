import logging, coloredlogs


def get_logger(name: str) -> logging.Logger:
    coloredlogs.install(level=logging.DEBUG, fmt='%(asctime)s - [%(pathname)s: %(lineno)d line in %(funcName)s] - %(levelname)s - %(message)s')
    logger = logging.getLogger(name)
    logger.info("Information: ")
    logger.debug("Debug: ")
    logger.warning("Warning: ")
    logger.error("Error: ")
    formatter = coloredlogs.ColoredFormatter('%(asctime)s - [%(pathname)s: %(lineno)d line in %(funcName)s] - %(levelname)s - %(message)s')
    fh = logging.FileHandler('debug.log', mode='w')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

logger = get_logger(__name__)
