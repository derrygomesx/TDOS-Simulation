"""
Track Digital Operations Sandbox (TDOS)

logger.py

Central logging utility for TDOS.
"""

from __future__ import annotations

import logging
import sys


class TDOSLogger:
    """
    Central logger used throughout TDOS.
    """

    LOGGER_NAME = "TDOS"

    FORMAT = "[%(asctime)s] " "[%(levelname)s] " "%(name)s: " "%(message)s"

    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    @classmethod
    def create(
        cls,
        level: int = logging.INFO,
    ) -> logging.Logger:
        """
        Create or retrieve the TDOS logger.
        """

        logger = logging.getLogger(cls.LOGGER_NAME)

        if logger.handlers:
            return logger

        logger.setLevel(level)

        handler = logging.StreamHandler(sys.stdout)

        formatter = logging.Formatter(
            fmt=cls.FORMAT,
            datefmt=cls.DATE_FORMAT,
        )

        handler.setFormatter(formatter)

        logger.addHandler(handler)

        logger.propagate = False

        return logger


# ==========================================================
# Global Logger
# ==========================================================

log = TDOSLogger.create()
