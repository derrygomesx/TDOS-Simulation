"""
Track Digital Operations Sandbox (TDOS)

prediction_engine.py

Central prediction engine for TDOS.
"""

from __future__ import annotations

from tdos.config.logging import log
from tdos.models.asset import RailwayAsset
from tdos.models.results import PredictionResult
from tdos.prediction.health import HealthPredictor
from tdos.prediction.risk import RiskPredictor
from tdos.prediction.rul import RULPredictor


class PredictionEngine:
    """
    Coordinates all prediction models.

    Responsibilities
    ----------------
    • Future Health Prediction
    • Risk Estimation
    • Remaining Useful Life (RUL)
    """

    def __init__(self) -> None:

        self.health_predictor = HealthPredictor()

        self.risk_predictor = RiskPredictor()

        self.rul_predictor = RULPredictor()

    # ==========================================================
    # Prediction
    # ==========================================================

    def predict(
        self,
        asset: RailwayAsset,
    ) -> PredictionResult:
        """
        Generate a complete prediction for an asset.
        """

        predicted_health = self.health_predictor.predict(asset)

        failure_probability = self.risk_predictor.predict(
            asset,
            predicted_health,
        )

        rul = self.rul_predictor.predict(
            asset,
            predicted_health,
        )

        confidence = self._calculate_confidence(asset)

        log.debug(f"Prediction completed for " f"{asset.asset_id}")

        return PredictionResult(
            failure_probability=failure_probability,
            remaining_useful_life_days=rul,
            predicted_health_score=predicted_health,
            confidence=confidence,
        )

    # ==========================================================
    # Confidence
    # ==========================================================

    @staticmethod
    def _calculate_confidence(
        asset: RailwayAsset,
    ) -> float:
        """
        Estimate prediction confidence.

        Confidence decreases as degradation increases.
        """

        confidence = 1.0 - (asset.degradation_rate * 0.1)

        confidence = max(0.50, min(1.0, confidence))

        return round(confidence, 3)
