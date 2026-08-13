"""
TDOS backend simulation API schemas.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from tdos.models.asset import RailwayAsset
from tdos.models.scenario import SimulationScenario


class SimulationCreateRequest(BaseModel):
    """Request payload used to create a TDOS simulation."""

    name: str = Field(min_length=1, max_length=200)
    experiment_id: str | None = None
    assets: list[RailwayAsset] = Field(default_factory=list)
    scenarios: list[SimulationScenario] = Field(default_factory=list)
    total_steps: int = Field(default=1000, gt=0, le=1_000_000)


class SimulationActionResponse(BaseModel):
    """Small response returned by lifecycle actions."""

    simulation_id: str
    status: str
    progress: float
    message: str
