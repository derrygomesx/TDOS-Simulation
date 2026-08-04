"""
Track Digital Operations Sandbox (TDOS)

results.py

Simulation result models.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from tdos.models.asset import RailwayAsset
from tdos.models.scenario import SimulationScenario


class AssetResult(BaseModel):
    """
    Final state of an individual asset after simulation.
    """

    model_config = ConfigDict(frozen=True)

    asset_id: str

    health_score: float = Field(
        ge=0,
        le=100,
    )

    degradation: float = Field(
        ge=0,
    )

    predicted_risk: str

    maintenance_required: bool

    failed: bool


class PredictionResult(BaseModel):
    """
    Prediction engine output.
    """

    model_config = ConfigDict(frozen=True)

    failure_probability: float = Field(
        ge=0,
        le=1,
    )

    remaining_useful_life_days: int = Field(
        ge=0,
    )

    predicted_health_score: float = Field(
        ge=0,
        le=100,
    )

    confidence: float = Field(
        ge=0,
        le=1,
    )


class BenchmarkResult(BaseModel):
    """
    AI Benchmark results.
    """

    model_config = ConfigDict(frozen=True)

    model_name: str

    accuracy: float = Field(
        ge=0,
        le=100,
    )

    precision: float = Field(
        ge=0,
        le=100,
    )

    recall: float = Field(
        ge=0,
        le=100,
    )

    f1_score: float = Field(
        ge=0,
        le=100,
    )

    latency_ms: float = Field(
        ge=0,
    )

    throughput_fps: float = Field(
        ge=0,
    )


class SimulationResult(BaseModel):
    """
    Final output of a TDOS simulation.

    This object acts as the public interface between
    the TDOS engine and external applications.
    """

    model_config = ConfigDict(
        frozen=True,
        validate_assignment=True,
    )

    # ==========================================================
    # Identity
    # ==========================================================

    simulation_id: str

    simulation_name: str

    completed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    success: bool = True

    # ==========================================================
    # Simulation
    # ==========================================================

    duration_seconds: float = Field(
        ge=0,
    )

    simulation_steps: int = Field(
        ge=0,
    )

    scenarios: List[SimulationScenario] = Field(
        default_factory=list,
    )

    # ==========================================================
    # Assets
    # ==========================================================

    assets: List[RailwayAsset] = Field(
        default_factory=list,
    )

    asset_results: List[AssetResult] = Field(
        default_factory=list,
    )

    # ==========================================================
    # Prediction
    # ==========================================================

    prediction: Optional[PredictionResult] = None

    # ==========================================================
    # Benchmark
    # ==========================================================

    benchmark: Optional[BenchmarkResult] = None

    # ==========================================================
    # Statistics
    # ==========================================================

    total_assets: int = Field(
        ge=0,
    )

    healthy_assets: int = Field(
        ge=0,
    )

    degraded_assets: int = Field(
        ge=0,
    )

    failed_assets: int = Field(
        ge=0,
    )

    average_health_score: float = Field(
        ge=0,
        le=100,
    )

    # ==========================================================
    # Metadata
    # ==========================================================

    metadata: Dict[str, str] = Field(
        default_factory=dict,
    )

    # ==========================================================
    # Helper Properties
    # ==========================================================

    @property
    def success_rate(self) -> float:
        """
        Percentage of healthy assets.
        """

        if self.total_assets == 0:
            return 0.0

        return (self.healthy_assets / self.total_assets) * 100

    # ==========================================================
    # Export
    # ==========================================================

    def summary(self) -> dict:
        """
        Returns a compact simulation summary.
        """

        return {
            "simulation_id": self.simulation_id,
            "simulation_name": self.simulation_name,
            "success": self.success,
            "duration_seconds": self.duration_seconds,
            "total_assets": self.total_assets,
            "healthy_assets": self.healthy_assets,
            "failed_assets": self.failed_assets,
            "average_health_score": self.average_health_score,
            "success_rate": round(
                self.success_rate,
                2,
            ),
        }
