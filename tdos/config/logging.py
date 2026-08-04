"""
Track Digital Operations Sandbox (TDOS)

logging.py

Central logging configuration for the TDOS Simulation Engine.
"""

from __future__ import annotations

import sys
from pathlib import Path

from loguru import logger

from tdos.config.settings import settings


class TDOSLogger:
    """
    Configures and provides the global TDOS logger.
    """

    _configured = False

    @classmethod
    def configure(cls) -> None:
        """
        Configure Loguru only once.
        """

        if cls._configured:
            return

        logger.remove()

        # ==========================================================
        # Console Logger
        # ==========================================================

        if settings.enable_console_logging:

            logger.add(
                sys.stdout,
                level=settings.log_level,
                colorize=True,
                backtrace=True,
                diagnose=False,
                enqueue=True,
                format=(
                    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                    "<level>{level: <8}</level> | "
                    "<cyan>{name}</cyan>:"
                    "<cyan>{function}</cyan>:"
                    "<cyan>{line}</cyan> | "
                    "<level>{message}</level>"
                ),
            )

        # ==========================================================
        # File Logger
        # ==========================================================

        if settings.enable_file_logging:

            Path("logs").mkdir(exist_ok=True)

            logger.add(
                f"logs/{settings.log_file}",
                level=settings.log_level,
                rotation="10 MB",
                retention="30 days",
                compression="zip",
                enqueue=True,
                backtrace=True,
                diagnose=False,
                format=(
                    "{time:YYYY-MM-DD HH:mm:ss} | "
                    "{level} | "
                    "{name}:{function}:{line} | "
                    "{message}"
                ),
            )

        cls._configured = True

    @staticmethod
    def get():
        """
        Returns the configured logger instance.
        """

        return logger


# ==========================================================
# Initialize Logger
# ==========================================================

TDOSLogger.configure()

log = TDOSLogger.get()
