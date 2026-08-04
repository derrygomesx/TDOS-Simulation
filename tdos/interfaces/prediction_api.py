"""
Track Digital Operations Sandbox (TDOS)

prediction_api.py

Public API for the TDOS Prediction Engine.
"""

from __future__ import annotations

from tdos.models.asset import RailwayAsset
from tdos.prediction.prediction_engine import PredictionEngine


class PredictionAPI:
    """
    Public interface for the TDOS Prediction Engine.
    """

    def __init__(self) -> None:

        self.engine = PredictionEngine()

    # ==========================================================
    # Prediction
    # ==========================================================

    def predict(
        self,
        asset: RailwayAsset,
    ):
        """
        Generate predictions for a railway asset.
        """

        return self.engine.predict(asset)

    # ==========================================================
    # Health
    # ==========================================================

    def predict_health(
        self,
        asset: RailwayAsset,
    ) -> float:
        """
        Predict future health score.
        """

        return self.engine.health_predictor.predict(asset)

    # ==========================================================
    # Risk
    # ==========================================================

    def predict_risk(
        self,
        asset: RailwayAsset,
    ) -> float:
        """
        Predict failure probability.
        """

        health = self.predict_health(asset)

        return self.engine.risk_predictor.predict(
            asset,
            health,
        )

    # ==========================================================
    # Remaining Useful Life
    # ==========================================================

    def predict_rul(
        self,
        asset: RailwayAsset,
    ) -> int:
        """
        Predict remaining useful life.
        """

        health = self.predict_health(asset)

        return self.engine.rul_predictor.predict(
            asset,
            health,
        )

    # ==========================================================
    # Summary
    # ==========================================================

    def summary(
        self,
        asset: RailwayAsset,
    ) -> dict:
        """
        Generate a prediction summary.
        """

        result = self.predict(asset)

        return {
            "predicted_health": result.predicted_health_score,
            "failure_probability": result.failure_probability,
            "remaining_useful_life_days": result.remaining_useful_life_days,
            "confidence": result.confidence,
        }
