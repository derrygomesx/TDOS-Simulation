"""
Track Digital Operations Sandbox (TDOS)

health.py

Health prediction model.
"""

from __future__ import annotations

from tdos.models.asset import RailwayAsset


class HealthPredictor:
    """
    Predicts the future health score of a railway asset.
    """

    def __init__(
        self,
        prediction_days: int = 30,
    ) -> None:

        self.prediction_days = prediction_days

    # ==========================================================
    # Prediction
    # ==========================================================

    def predict(
        self,
        asset: RailwayAsset,
    ) -> float:
        """
        Predict future health score.

        Uses a simple degradation projection that can
        later be replaced by an ML model.
        """

        predicted_health = asset.health_score - (asset.degradation_rate * self.prediction_days)

        predicted_health = max(
            0.0,
            min(100.0, predicted_health),
        )

        return round(predicted_health, 2)

    # ==========================================================
    # Trend
    # ==========================================================

    @staticmethod
    def trend(
        current: float,
        predicted: float,
    ) -> str:
        """
        Determine health trend.
        """

        delta = predicted - current

        if delta >= 5:
            return "IMPROVING"

        if delta <= -5:
            return "DECLINING"

        return "STABLE"

    # ==========================================================
    # Health Grade
    # ==========================================================

    @staticmethod
    def grade(
        health: float,
    ) -> str:
        """
        Convert health score to grade.
        """

        if health >= 90:
            return "A"

        if health >= 80:
            return "B"

        if health >= 70:
            return "C"

        if health >= 60:
            return "D"

        return "F"

    # ==========================================================
    # Health Status
    # ==========================================================

    @staticmethod
    def status(
        health: float,
    ) -> str:
        """
        Convert health score into status.
        """

        if health >= 90:
            return "EXCELLENT"

        if health >= 75:
            return "GOOD"

        if health >= 60:
            return "FAIR"

        if health >= 40:
            return "POOR"

        return "CRITICAL"
