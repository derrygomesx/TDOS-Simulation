"""
Track Digital Operations Sandbox (TDOS)

experiment.py

Experiment model for AI benchmarking and validation.
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class AIExperiment(BaseModel):
    """
    Represents an AI experiment executed inside TDOS.

    An experiment may include training, validation,
    benchmarking, stress testing, or certification.
    """

    model_config = ConfigDict(frozen=True, validate_assignment=True)

    # ==========================================================
    # Identity
    # ==========================================================

    experiment_id: str = Field(..., description="Unique experiment identifier.")

    experiment_name: str = Field(..., description="Human-readable experiment name.")

    description: str = Field(default="", description="Experiment description.")

    # ==========================================================
    # AI Model
    # ==========================================================

    model_name: str = Field(..., description="Name of the evaluated AI model.")

    model_version: str = Field(default="1.0.0", description="Model version.")

    dataset_name: str = Field(..., description="Dataset used during the experiment.")

    # ==========================================================
    # Execution
    # ==========================================================

    experiment_type: str = Field(
        ..., description="TRAINING, VALIDATION, BENCHMARK, STRESS_TEST, CERTIFICATION."
    )

    status: str = Field(default="PENDING", description="Current experiment status.")

    started_at: Optional[datetime] = None

    completed_at: Optional[datetime] = None

    duration_seconds: float = Field(default=0.0, ge=0.0)

    # ==========================================================
    # Performance Metrics
    # ==========================================================

    accuracy: float = Field(default=0.0, ge=0.0, le=100.0)

    precision: float = Field(default=0.0, ge=0.0, le=100.0)

    recall: float = Field(default=0.0, ge=0.0, le=100.0)

    f1_score: float = Field(default=0.0, ge=0.0, le=100.0)

    latency_ms: float = Field(default=0.0, ge=0.0)

    throughput_fps: float = Field(default=0.0, ge=0.0)

    memory_mb: float = Field(default=0.0, ge=0.0)

    # ==========================================================
    # Configuration
    # ==========================================================

    parameters: Dict[str, str | int | float | bool] = Field(
        default_factory=dict, description="Experiment configuration."
    )

    metrics: Dict[str, float] = Field(
        default_factory=dict, description="Additional custom metrics."
    )

    notes: Optional[str] = None

    # ==========================================================
    # Helper Properties
    # ==========================================================

    @property
    def successful(self) -> bool:
        """
        Returns True if the experiment completed successfully.
        """
        return self.status.upper() == "COMPLETED"

    @property
    def failed(self) -> bool:
        """
        Returns True if the experiment failed.
        """
        return self.status.upper() == "FAILED"

    # ==========================================================
    # Export
    # ==========================================================

    def summary(self) -> dict:
        """
        Returns a compact summary of the experiment.
        """

        return {
            "experiment_id": self.experiment_id,
            "experiment_name": self.experiment_name,
            "model": self.model_name,
            "dataset": self.dataset_name,
            "status": self.status,
            "accuracy": self.accuracy,
            "precision": self.precision,
            "recall": self.recall,
            "f1_score": self.f1_score,
            "latency_ms": self.latency_ms,
        }
