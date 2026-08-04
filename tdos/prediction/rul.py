"""
Track Digital Operations Sandbox (TDOS)

rul.py

Remaining Useful Life (RUL) prediction model.
"""

from __future__ import annotations

from tdos.models.asset import RailwayAsset


class RULPredictor:
    """
    Estimates the Remaining Useful Life (RUL) of a railway asset.
    """

    def __init__(
        self,
        critical_health: float = 40.0,
    ) -> None:

        self.critical_health = critical_health

    # ==========================================================
    # Prediction
    # ==========================================================

    def predict(
        self,
        asset: RailwayAsset,
        predicted_health: float,
    ) -> int:
        """
        Estimate remaining useful life in days.

        Returns 0 if the asset has already reached
        the critical health threshold.
        """

        if predicted_health <= self.critical_health:
            return 0

        degradation = max(
            asset.degradation_rate,
            0.01,
        )

        remaining_health = predicted_health - self.critical_health

        rul = int(remaining_health / degradation)

        return max(0, rul)

    # ==========================================================
    # Lifecycle Stage
    # ==========================================================

    @staticmethod
    def lifecycle_stage(
        rul_days: int,
    ) -> str:
        """
        Returns the asset lifecycle stage.
        """

        if rul_days >= 365:
            return "HEALTHY"

        if rul_days >= 180:
            return "STABLE"

        if rul_days >= 90:
            return "AGING"

        if rul_days >= 30:
            return "DEGRADING"

        return "END_OF_LIFE"

    # ==========================================================
    # Maintenance Window
    # ==========================================================

    @staticmethod
    def maintenance_window(
        rul_days: int,
    ) -> str:
        """
        Returns the recommended maintenance window.
        """

        if rul_days >= 180:
            return "Routine Maintenance"

        if rul_days >= 90:
            return "Schedule Maintenance"

        if rul_days >= 30:
            return "Priority Maintenance"

        return "Immediate Maintenance"

    # ==========================================================
    # Inspection Interval
    # ==========================================================

    @staticmethod
    def inspection_interval(
        rul_days: int,
    ) -> int:
        """
        Recommended inspection interval in days.
        """

        if rul_days >= 365:
            return 90

        if rul_days >= 180:
            return 60

        if rul_days >= 90:
            return 30

        if rul_days >= 30:
            return 14

        return 7
