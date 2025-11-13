import sys

from src.core.config import log

import logging


def init_logger() -> logging.Logger:
    logger = logging.getLogger("app")

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)

        formatter = logging.Formatter(log.format)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        level = logging.getLevelName(log.level.upper())
        logger.setLevel(level)

        logger.propagate = False

    return logger


logger = init_logger()
