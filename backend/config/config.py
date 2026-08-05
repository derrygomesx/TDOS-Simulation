"""
TrackGuard AI
Track Digital Operations Sandbox (TDOS)

config.py

Application configuration.

Author  : TrackGuard AI Team
Version : 1.0.0
"""

from pathlib import Path

from pydantic import BaseModel

from config.constants import (
    APP_NAME,
    APP_SHORT_NAME,
    APP_VERSION,
    API_VERSION,
    DATABASE_URL,
    UPLOAD_DIRECTORY,
    EXPORT_DIRECTORY,
    REPORT_DIRECTORY,
    DASHBOARD_REFRESH_SECONDS,
)


class Settings(BaseModel):
    """
    Global TDOS configuration.
    """

    app_name: str = APP_NAME

    app_short_name: str = APP_SHORT_NAME

    app_version: str = APP_VERSION

    api_version: str = API_VERSION

    database_url: str = DATABASE_URL

    upload_directory: Path = Path(UPLOAD_DIRECTORY)

    export_directory: Path = Path(EXPORT_DIRECTORY)

    report_directory: Path = Path(REPORT_DIRECTORY)

    dashboard_refresh_seconds: int = DASHBOARD_REFRESH_SECONDS


settings = Settings()