"""
Track Digital Operations Sandbox (TDOS)

rams/models.py

RAMS (Reliability, Availability, Maintainability & Safety) result models.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class RAMSComponentScore(BaseModel):
    """A normalized RAMS component score for one asset."""

    model_config = ConfigDict(frozen=True)

    score: float = Field(ge=0, le=100)
    grade: str
    rationale: str


class RAMSAssetResult(BaseModel):
    """RAMS analysis for a single railway asset."""

    model_config = ConfigDict(frozen=True)

    asset_id: str
    asset_name: str
    asset_type: str

    rams_score: float = Field(ge=0, le=100)
    rams_grade: str

    reliability: RAMSComponentScore
    availability: RAMSComponentScore
    maintainability: RAMSComponentScore
    safety: RAMSComponentScore

    failure_probability: float = Field(ge=0, le=1)
    remaining_useful_life_days: int = Field(ge=0)
    maintenance_priority: str
    criticality: str
    operational_availability_percent: float = Field(ge=0, le=100)
    health_score: float = Field(ge=0, le=100)
    failed: bool


class RAMSFleetSummary(BaseModel):
    """Fleet-level RAMS roll-up."""

    model_config = ConfigDict(frozen=True)

    rams_score: float = Field(ge=0, le=100)
    rams_grade: str
    reliability_score: float = Field(ge=0, le=100)
    availability_score: float = Field(ge=0, le=100)
    maintainability_score: float = Field(ge=0, le=100)
    safety_score: float = Field(ge=0, le=100)
    critical_assets: int = Field(ge=0)
    immediate_maintenance: int = Field(ge=0)
    high_priority_maintenance: int = Field(ge=0)
    fleet_operational_availability_percent: float = Field(ge=0, le=100)


class RAMSResult(BaseModel):
    """Complete RAMS analysis returned by the TDOS RAMS service."""

    model_config = ConfigDict(frozen=True)

    simulation_id: str
    simulation_name: str
    methodology: str
    weights: dict[str, float]
    fleet: RAMSFleetSummary
    assets: list[RAMSAssetResult]
