"""
TrackGuard AI
Track Digital Operations Sandbox (TDOS)

models.py

Database models for TDOS.

Author  : TrackGuard AI Team
Version : 1.0.0
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Text,
)

from database.database import Base


# ==========================================================
# EXPERIMENT
# ==========================================================

class ExperimentModel(Base):

    __tablename__ = "experiments"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))

    name = Column(String, nullable=False)

    description = Column(Text)

    status = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(DateTime, default=datetime.utcnow)


# ==========================================================
# DATASET
# ==========================================================

class DatasetModel(Base):

    __tablename__ = "datasets"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))

    name = Column(String, nullable=False)

    version = Column(String)

    status = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(DateTime, default=datetime.utcnow)


# ==========================================================
# MODEL REGISTRY
# ==========================================================

class ModelRegistryModel(Base):

    __tablename__ = "models"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))

    name = Column(String, nullable=False)

    version = Column(String)

    architecture = Column(String)

    precision = Column(Float)

    recall = Column(Float)

    inference_time = Column(Float)

    status = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(DateTime, default=datetime.utcnow)


# ==========================================================
# REPORT
# ==========================================================

class ReportModel(Base):

    __tablename__ = "reports"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))

    title = Column(String, nullable=False)

    report_type = Column(String)

    file_path = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)


# ==========================================================
# SIMULATION
# ==========================================================

class SimulationModel(Base):

    __tablename__ = "simulations"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))

    experiment_id = Column(String)

    scenario_name = Column(String)

    status = Column(String)

    progress = Column(Float, default=0.0)

    created_at = Column(DateTime, default=datetime.utcnow)


# ==========================================================
# DASHBOARD CACHE
# ==========================================================

class DashboardCacheModel(Base):

    __tablename__ = "dashboard"

    id = Column(Integer, primary_key=True)

    active_experiments = Column(Integer, default=0)

    active_models = Column(Integer, default=0)

    datasets = Column(Integer, default=0)

    reports = Column(Integer, default=0)

    running_simulations = Column(Integer, default=0)

    system_health = Column(String, default="HEALTHY")