"""
TrackGuard AI
Track Digital Operations Sandbox (TDOS)

enums.py

Enumerations used throughout TDOS.

Author  : TrackGuard AI Team
Version : 1.0.0
"""

from enum import Enum


# ==========================================================
# EXPERIMENT STATUS
# ==========================================================

class ExperimentStatus(str, Enum):

    CREATED = "CREATED"

    RUNNING = "RUNNING"

    PAUSED = "PAUSED"

    COMPLETED = "COMPLETED"

    FAILED = "FAILED"


# ==========================================================
# SIMULATION STATUS
# ==========================================================

class SimulationStatus(str, Enum):

    IDLE = "IDLE"

    STARTING = "STARTING"

    RUNNING = "RUNNING"

    PAUSED = "PAUSED"

    STOPPED = "STOPPED"

    COMPLETED = "COMPLETED"

    FAILED = "FAILED"


# ==========================================================
# DATASET STATUS
# ==========================================================

class DatasetStatus(str, Enum):

    ACTIVE = "ACTIVE"

    ARCHIVED = "ARCHIVED"

    DELETED = "DELETED"


# ==========================================================
# MODEL STATUS
# ==========================================================

class ModelStatus(str, Enum):

    TRAINING = "TRAINING"

    VALIDATING = "VALIDATING"

    CERTIFIED = "CERTIFIED"

    DEPLOYED = "DEPLOYED"

    RETIRED = "RETIRED"


# ==========================================================
# REPORT TYPE
# ==========================================================

class ReportType(str, Enum):

    SIMULATION = "SIMULATION"

    BENCHMARK = "BENCHMARK"

    FLEET = "FLEET"

    MAINTENANCE = "MAINTENANCE"

    VALIDATION = "VALIDATION"

    EXPERIMENT = "EXPERIMENT"

    SYSTEM = "SYSTEM"


# ==========================================================
# USER ROLE
# ==========================================================

class UserRole(str, Enum):

    ADMIN = "ADMIN"

    ENGINEER = "ENGINEER"

    OPERATOR = "OPERATOR"

    VIEWER = "VIEWER"


# ==========================================================
# WEBSOCKET EVENT
# ==========================================================

class WebSocketEvent(str, Enum):

    DASHBOARD_UPDATE = "DASHBOARD_UPDATE"

    SIMULATION_PROGRESS = "SIMULATION_PROGRESS"

    TRAINING_PROGRESS = "TRAINING_PROGRESS"

    REPLAY_PROGRESS = "REPLAY_PROGRESS"

    FLEET_UPDATE = "FLEET_UPDATE"

    NOTIFICATION = "NOTIFICATION"


# ==========================================================
# SYSTEM STATUS
# ==========================================================

class SystemStatus(str, Enum):

    HEALTHY = "HEALTHY"

    WARNING = "WARNING"

    CRITICAL = "CRITICAL"

    OFFLINE = "OFFLINE"