"""
Track Digital Operations Sandbox (TDOS)

simulation.py

Simulation session model for the TDOS Simulation Engine.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from tdos.models.asset import RailwayAsset
from tdos.models.scenario import SimulationScenario


class SimulationSession(BaseModel):
    """
    Represents a complete TDOS simulation session.
    """

    model_config = ConfigDict(frozen=True, validate_assignment=True)

    # ==========================================================
    # Identity
    # ==========================================================

    simulation_id: str = Field(..., description="Unique simulation identifier.")

    simulation_name: str = Field(..., description="Simulation name.")

    description: str = Field(default="", description="Simulation description.")

    # ==========================================================
    # Timing
    # ==========================================================

    created_at: datetime = Field(default_factory=lambda: datetime.now())

    started_at: Optional[datetime] = None

    finished_at: Optional[datetime] = None

    # ==========================================================
    # State
    # ==========================================================

    status: str = Field(default="IDLE", description="Current simulation state.")

    current_step: int = Field(default=0, ge=0)

    total_steps: int = Field(default=1000, gt=0)

    progress: float = Field(default=0.0, ge=0.0, le=100.0)

    # ==========================================================
    # Simulation Components
    # ==========================================================

    assets: List[RailwayAsset] = Field(default_factory=list)

    scenarios: List[SimulationScenario] = Field(default_factory=list)

    # ==========================================================
    # Runtime
    # ==========================================================

    random_seed: int = 42

    speed_multiplier: float = Field(default=1.0, gt=0)

    paused: bool = False

    completed: bool = False

    # ==========================================================
    # Statistics
    # ==========================================================

    events_processed: int = Field(default=0, ge=0)

    assets_updated: int = Field(default=0, ge=0)

    predictions_generated: int = Field(default=0, ge=0)

    replay_frames: int = Field(default=0, ge=0)

    benchmark_runs: int = Field(default=0, ge=0)

    # ==========================================================
    # Summary
    # ==========================================================

    @property
    def asset_count(self) -> int:
        """Returns the number of assets."""

        return len(self.assets)

    @property
    def scenario_count(self) -> int:
        """Returns the number of scenarios."""

        return len(self.scenarios)

    @property
    def is_running(self) -> bool:
        """True if the simulation is currently running."""

        return self.status == "RUNNING"

    @property
    def is_finished(self) -> bool:
        """True if the simulation has completed."""

        return self.completed

    # ==========================================================
    # Export
    # ==========================================================

    def summary(self) -> dict:
        """
        Returns a compact summary of the simulation.
        """

        return {
            "simulation_id": self.simulation_id,
            "simulation_name": self.simulation_name,
            "status": self.status,
            "progress": self.progress,
            "assets": self.asset_count,
            "scenarios": self.scenario_count,
            "events_processed": self.events_processed,
            "completed": self.completed,
        }
