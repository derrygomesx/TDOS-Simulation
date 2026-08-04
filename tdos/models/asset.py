"""
Track Digital Operations Sandbox (TDOS)

asset.py

Core railway asset model used throughout the TDOS Simulation Engine.
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class RailwayAsset(BaseModel):
    """
    Represents a railway infrastructure asset participating
    in a TDOS simulation.
    """

    model_config = ConfigDict(frozen=True, validate_assignment=True)

    # ==========================================================
    # Asset Identity
    # ==========================================================

    asset_id: str = Field(..., description="Unique asset identifier.")

    asset_name: str = Field(..., description="Human-readable asset name.")

    asset_type: str = Field(..., description="Type of railway asset.")

    # ==========================================================
    # Location
    # ==========================================================

    latitude: float = Field(..., ge=-90, le=90, description="Latitude.")

    longitude: float = Field(..., ge=-180, le=180, description="Longitude.")

    kilometer_post: float = Field(default=0.0, ge=0, description="Railway kilometer location.")

    # ==========================================================
    # Health
    # ==========================================================

    health_score: float = Field(default=100.0, ge=0, le=100, description="Current asset health.")

    degradation_rate: float = Field(
        default=0.0, ge=0, description="Health degradation per simulation cycle."
    )

    age_days: int = Field(default=0, ge=0, description="Asset age in days.")

    # ==========================================================
    # Operational State
    # ==========================================================

    active: bool = True

    under_maintenance: bool = False

    failed: bool = False

    # ==========================================================
    # Metadata
    # ==========================================================

    installation_date: Optional[datetime] = None

    last_inspection: Optional[datetime] = None

    last_maintenance: Optional[datetime] = None

    metadata: Dict[str, str] = Field(default_factory=dict, description="Additional asset metadata.")

    # ==========================================================
    # Helper Properties
    # ==========================================================

    @property
    def is_operational(self) -> bool:
        """
        Returns True if the asset is operational.
        """
        return self.active and not self.failed

    @property
    def requires_maintenance(self) -> bool:
        """
        Returns True if maintenance should be scheduled.
        """
        return self.health_score < 60

    @property
    def is_critical(self) -> bool:
        """
        Returns True if the asset health is critical.
        """
        return self.health_score < 40

    # ==========================================================
    # Summary
    # ==========================================================

    def summary(self) -> dict:
        """
        Returns a compact asset summary.
        """

        return {
            "asset_id": self.asset_id,
            "asset_name": self.asset_name,
            "asset_type": self.asset_type,
            "health_score": self.health_score,
            "active": self.active,
            "failed": self.failed,
            "maintenance_required": self.requires_maintenance,
        }
