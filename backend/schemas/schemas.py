"""
TrackGuard AI
Track Digital Operations Sandbox (TDOS)

schemas.py

Pydantic schemas used throughout TDOS.

Author  : TrackGuard AI Team
Version : 1.0.0
"""

from datetime import datetime
from typing import Dict, Optional
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from config.enums import (
    DatasetStatus,
    ExperimentStatus,
    ModelStatus,
    ReportType,
    SimulationStatus,
)


# ==========================================================
# BASE ENTITY
# ==========================================================

class BaseEntity(BaseModel):
    """
    Base schema inherited by all TDOS entities.
    """

    model_config = ConfigDict(from_attributes=True)

    id: str = Field(default_factory=lambda: str(uuid4()))

    created_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(default_factory=datetime.utcnow)

    status: str = "ACTIVE"

    metadata: Dict[str, str] = Field(default_factory=dict)


# ==========================================================
# EXPERIMENT
# ==========================================================

class Experiment(BaseEntity):

    name: str

    description: Optional[str] = None

    status: ExperimentStatus = ExperimentStatus.CREATED


# ==========================================================
# DATASET
# ==========================================================

class Dataset(BaseEntity):

    name: str

    version: str

    status: DatasetStatus = DatasetStatus.ACTIVE


# ==========================================================
# MODEL
# ==========================================================

class ModelRegistry(BaseEntity):

    name: str

    version: str

    architecture: str

    precision: float = 0.0

    recall: float = 0.0

    inference_time: float = 0.0

    status: ModelStatus = ModelStatus.TRAINING


# ==========================================================
# SIMULATION
# ==========================================================

class Simulation(BaseEntity):

    experiment_id: str

    scenario_name: str

    status: SimulationStatus = SimulationStatus.IDLE

    progress: float = 0.0


# ==========================================================
# REPORT
# ==========================================================

class Report(BaseEntity):

    title: str

    report_type: ReportType

    file_path: str


# ==========================================================
# DASHBOARD
# ==========================================================

class DashboardMetrics(BaseModel):

    active_experiments: int = 0

    active_models: int = 0

    datasets: int = 0

    reports: int = 0

    running_simulations: int = 0

    system_health: str = "HEALTHY"