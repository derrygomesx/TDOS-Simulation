"""
TrackGuard AI
Track Digital Operations Sandbox (TDOS)

constants.py

Global constants used throughout TDOS.

Author  : TrackGuard AI Team
Version : 1.0.0
"""

# ==========================================================
# APPLICATION
# ==========================================================

APP_NAME = "TrackGuard Digital Operations Sandbox"

APP_SHORT_NAME = "TDOS"

APP_VERSION = "1.0.0"

API_VERSION = "v1"

# ==========================================================
# DATABASE
# ==========================================================

DATABASE_NAME = "tdos.db"

DATABASE_URL = f"sqlite:///{DATABASE_NAME}"

# ==========================================================
# STORAGE
# ==========================================================

UPLOAD_DIRECTORY = "storage/uploads"

EXPORT_DIRECTORY = "storage/exports"

REPORT_DIRECTORY = "storage/reports"

# ==========================================================
# REPORTS
# ==========================================================

DEFAULT_REPORT_FORMAT = "PDF"

SUPPORTED_REPORT_FORMATS = (

    "PDF",

    "EXCEL",

    "WORD",

)

# ==========================================================
# DATASETS
# ==========================================================

MAX_DATASET_SIZE_MB = 500

SUPPORTED_DATASET_TYPES = (

    ".csv",

    ".xlsx",

    ".json",

)

# ==========================================================
# MODELS
# ==========================================================

SUPPORTED_MODEL_TYPES = (

    "YOLO",

    "CNN",

    "TRANSFORMER",

)

# ==========================================================
# WEBSOCKET
# ==========================================================

WEBSOCKET_ROUTE = "/ws"

# ==========================================================
# DASHBOARD
# ==========================================================

DASHBOARD_REFRESH_SECONDS = 5

MAX_RECENT_REPORTS = 10

MAX_RECENT_EXPERIMENTS = 10