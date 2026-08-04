"""
Track Digital Operations Sandbox (TDOS)

risk.py

Risk prediction model.
"""

from __future__ import annotations

from tdos.models.asset import RailwayAsset


class RiskPredictor:
    """
    Estimates the probability of failure and overall
    operational risk of a railway asset.
    """

    # ==========================================================
    # Prediction
    # ==========================================================

    def predict(
        self,
        asset: RailwayAsset,
        predicted_health: float,
    ) -> float:
        """
        Returns failure probability between 0 and 1.
        """

        current_factor = (100.0 - asset.health_score) / 100.0

        future_factor = (100.0 - predicted_health) / 100.0

        degradation_factor = min(
            1.0,
            asset.degradation_rate,
        )

        probability = (0.45 * current_factor) + (0.40 * future_factor) + (0.15 * degradation_factor)

        probability = max(
            0.0,
            min(1.0, probability),
        )

        return round(probability, 3)

    # ==========================================================
    # Risk Level
    # ==========================================================

    @staticmethod
    def risk_level(
        probability: float,
    ) -> str:
        """
        Converts probability into a risk level.
        """

        if probability >= 0.80:
            return "CRITICAL"

        if probability >= 0.60:
            return "HIGH"

        if probability >= 0.35:
            return "MEDIUM"

        return "LOW"

    # ==========================================================
    # Maintenance Priority
    # ==========================================================

    @staticmethod
    def maintenance_priority(
        probability: float,
    ) -> str:
        """
        Determines maintenance urgency.
        """

        if probability >= 0.80:
            return "IMMEDIATE"

        if probability >= 0.60:
            return "HIGH"

        if probability >= 0.35:
            return "MEDIUM"

        return "LOW"

    # ==========================================================
    # Recommended Action
    # ==========================================================

    @staticmethod
    def recommended_action(
        probability: float,
    ) -> str:
        """
        Returns the recommended maintenance action.
        """

        if probability >= 0.80:
            return "Replace asset immediately."

        if probability >= 0.60:
            return "Schedule urgent maintenance."

        if probability >= 0.35:
            return "Increase inspection frequency."

        return "Continue normal monitoring."
