"""
Track Digital Operations Sandbox (TDOS)

scenario.py

Core simulation scenario model.
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class SimulationScenario(BaseModel):
    """
    Represents a simulation scenario executed by TDOS.
    """

    model_config = ConfigDict(frozen=True, validate_assignment=True)

    # ==========================================================
    # Identity
    # ==========================================================

    scenario_id: str = Field(..., description="Unique scenario identifier.")

    name: str = Field(..., description="Scenario name.")

    category: str = Field(..., description="Scenario category.")

    description: str = Field(default="", description="Scenario description.")

    # ==========================================================
    # Configuration
    # ==========================================================

    enabled: bool = True

    severity: float = Field(default=0.5, ge=0.0, le=1.0, description="Scenario severity.")

    probability: float = Field(
        default=1.0, ge=0.0, le=1.0, description="Probability of occurrence."
    )

    duration: int = Field(default=60, ge=1, description="Scenario duration in simulation steps.")

    start_step: int = Field(
        default=0, ge=0, description="Simulation step at which the scenario starts."
    )

    # ==========================================================
    # Target
    # ==========================================================

    target_asset: Optional[str] = Field(default=None, description="Target asset identifier.")

    affected_assets: list[str] = Field(
        default_factory=list, description="Assets affected by the scenario."
    )

    # ==========================================================
    # Parameters
    # ==========================================================

    parameters: Dict[str, float | int | str | bool] = Field(
        default_factory=dict, description="Scenario-specific parameters."
    )

    # ==========================================================
    # Metadata
    # ==========================================================

    created_at: datetime = Field(default_factory=datetime.now())

    author: Optional[str] = None

    tags: list[str] = Field(default_factory=list)

    # ==========================================================
    # Helper Properties
    # ==========================================================

    @property
    def end_step(self) -> int:
        """
        Returns the final simulation step.
        """
        return self.start_step + self.duration

    @property
    def is_global(self) -> bool:
        """
        True if the scenario affects the whole simulation.
        """
        return self.target_asset is None

    @property
    def affects_multiple_assets(self) -> bool:
        """
        True if multiple assets are affected.
        """
        return len(self.affected_assets) > 1

    # ==========================================================
    # Summary
    # ==========================================================

    def summary(self) -> dict:
        """
        Returns a compact scenario summary.
        """

        return {
            "scenario_id": self.scenario_id,
            "name": self.name,
            "category": self.category,
            "severity": self.severity,
            "duration": self.duration,
            "enabled": self.enabled,
        }
