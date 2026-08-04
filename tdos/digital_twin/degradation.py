"""
Track Digital Operations Sandbox (TDOS)

degradation.py

Asset degradation model used by the Digital Twin.
"""

from __future__ import annotations

from tdos.config.logging import log
from tdos.models.asset import RailwayAsset


class DegradationModel:
    """
    Simulates asset degradation over time.

    Health decreases according to:

        Base Degradation
        + Scenario Severity
        + Environmental Factor
        + Operational Stress

    Health is always clamped to the range [0, 100].
    """

    def __init__(
        self,
        base_rate: float = 0.02,
    ) -> None:

        self.base_rate = base_rate

    # ==========================================================
    # Public API
    # ==========================================================

    def apply(
        self,
        asset: RailwayAsset,
        *,
        scenario_factor: float = 1.0,
        environmental_factor: float = 1.0,
        operational_factor: float = 1.0,
    ) -> RailwayAsset:
        """
        Applies one degradation cycle and returns
        a NEW RailwayAsset.
        """

        degradation = self.calculate_degradation(
            asset,
            scenario_factor=scenario_factor,
            environmental_factor=environmental_factor,
            operational_factor=operational_factor,
        )

        new_health = max(
            0.0,
            asset.health_score - degradation,
        )

        updated_asset = asset.model_copy(
            update={
                "health_score": new_health,
                "age_days": asset.age_days + 1,
            }
        )

        log.debug(f"{asset.asset_id} degraded " f"{asset.health_score:.2f} -> " f"{new_health:.2f}")

        return updated_asset

    # ==========================================================
    # Calculation
    # ==========================================================

    def calculate_degradation(
        self,
        asset: RailwayAsset,
        *,
        scenario_factor: float,
        environmental_factor: float,
        operational_factor: float,
    ) -> float:
        """
        Calculates degradation for one simulation step.
        """

        degradation = (
            (self.base_rate + asset.degradation_rate)
            * scenario_factor
            * environmental_factor
            * operational_factor
        )

        return max(0.0, degradation)

    # ==========================================================
    # Health Classification
    # ==========================================================

    @staticmethod
    def health_status(
        health_score: float,
    ) -> str:
        """
        Converts a health score into a health status.
        """

        if health_score >= 90:
            return "EXCELLENT"

        if health_score >= 75:
            return "GOOD"

        if health_score >= 60:
            return "FAIR"

        if health_score >= 40:
            return "POOR"

        return "CRITICAL"

    # ==========================================================
    # Maintenance
    # ==========================================================

    @staticmethod
    def maintenance_required(
        health_score: float,
    ) -> bool:
        """
        Determines whether maintenance is required.
        """

        return health_score < 60

    # ==========================================================
    # Failure
    # ==========================================================

    @staticmethod
    def asset_failed(
        health_score: float,
    ) -> bool:
        """
        Determines whether the asset has failed.
        """

        return health_score <= 20
