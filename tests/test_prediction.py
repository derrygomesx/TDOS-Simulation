"""
Track Digital Operations Sandbox (TDOS)

test_prediction.py

Tests for the TDOS Prediction Engine.
"""

from tdos.models.asset import RailwayAsset
from tdos.prediction.health import HealthPredictor
from tdos.prediction.prediction_engine import PredictionEngine
from tdos.prediction.risk import RiskPredictor
from tdos.prediction.rul import RULPredictor

# ==========================================================
# Test Asset
# ==========================================================


def create_asset() -> RailwayAsset:
    """
    Create a sample railway asset for testing.
    """

    return RailwayAsset(
        asset_id="AST-001",
        asset_name="Test Rail",
        asset_type="RAIL",
        latitude=11.0168,
        longitude=76.9558,
        kilometer_post=12.5,
        health_score=95.0,
        degradation_rate=0.10,
        age_days=30,
    )


# ==========================================================
# Health Predictor
# ==========================================================


def test_health_prediction():

    asset = create_asset()

    predictor = HealthPredictor()

    health = predictor.predict(asset)

    assert 0 <= health <= 100


# ==========================================================
# Risk Predictor
# ==========================================================


def test_risk_prediction():

    asset = create_asset()

    health = HealthPredictor().predict(asset)

    risk = RiskPredictor().predict(
        asset,
        health,
    )

    assert 0.0 <= risk <= 1.0


# ==========================================================
# RUL Predictor
# ==========================================================


def test_rul_prediction():

    asset = create_asset()

    health = HealthPredictor().predict(asset)

    rul = RULPredictor().predict(
        asset,
        health,
    )

    assert rul >= 0


# ==========================================================
# Complete Prediction Engine
# ==========================================================


def test_prediction_engine():

    asset = create_asset()

    engine = PredictionEngine()

    result = engine.predict(asset)

    assert result.predicted_health_score >= 0

    assert result.failure_probability >= 0

    assert result.remaining_useful_life_days >= 0

    assert 0.0 <= result.confidence <= 1.0


# ==========================================================
# Health Grade
# ==========================================================


def test_health_grade():

    predictor = HealthPredictor()

    assert predictor.grade(95) == "A"

    assert predictor.grade(85) == "B"

    assert predictor.grade(75) == "C"

    assert predictor.grade(65) == "D"

    assert predictor.grade(50) == "F"


# ==========================================================
# Health Status
# ==========================================================


def test_health_status():

    predictor = HealthPredictor()

    assert predictor.status(95) == "EXCELLENT"

    assert predictor.status(80) == "GOOD"

    assert predictor.status(65) == "FAIR"

    assert predictor.status(45) == "POOR"

    assert predictor.status(20) == "CRITICAL"


# ==========================================================
# Risk Level
# ==========================================================


def test_risk_level():

    predictor = RiskPredictor()

    assert predictor.risk_level(0.20) == "LOW"

    assert predictor.risk_level(0.45) == "MEDIUM"

    assert predictor.risk_level(0.65) == "HIGH"

    assert predictor.risk_level(0.90) == "CRITICAL"


# ==========================================================
# Maintenance Priority
# ==========================================================


def test_maintenance_priority():

    predictor = RiskPredictor()

    assert predictor.maintenance_priority(0.20) == "LOW"

    assert predictor.maintenance_priority(0.45) == "MEDIUM"

    assert predictor.maintenance_priority(0.70) == "HIGH"

    assert predictor.maintenance_priority(0.90) == "IMMEDIATE"


# ==========================================================
# Lifecycle Stage
# ==========================================================


def test_lifecycle_stage():

    predictor = RULPredictor()

    assert predictor.lifecycle_stage(400) == "HEALTHY"

    assert predictor.lifecycle_stage(250) == "STABLE"

    assert predictor.lifecycle_stage(120) == "AGING"

    assert predictor.lifecycle_stage(45) == "DEGRADING"

    assert predictor.lifecycle_stage(10) == "END_OF_LIFE"
