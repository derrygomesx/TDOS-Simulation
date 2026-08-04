"""
Track Digital Operations Sandbox (TDOS)

test_engine.py

Tests for the TDOS Simulation Engine.
"""

from tdos.core.engine import SimulationEngine
from tdos.models.asset import RailwayAsset
from tdos.models.scenario import SimulationScenario

# ==========================================================
# Test Data
# ==========================================================


def create_engine() -> SimulationEngine:
    """
    Create a simulation engine with a test session.
    """

    engine = SimulationEngine()

    assets = [
        RailwayAsset(
            asset_id="AST-001",
            asset_name="Test Rail",
            asset_type="RAIL",
            latitude=11.0168,
            longitude=76.9558,
            kilometer_post=12.5,
            health_score=95.0,
            degradation_rate=0.02,
            age_days=30,
        )
    ]

    scenarios: list[SimulationScenario] = []

    engine.create_session(
        name="Unit Test",
        assets=assets,
        scenarios=scenarios,
        total_steps=10,
    )

    return engine


# ==========================================================
# Engine Creation
# ==========================================================


def test_engine_creation():

    engine = SimulationEngine()

    assert engine is not None


# ==========================================================
# Session Creation
# ==========================================================


def test_create_session():

    engine = create_engine()

    session = engine.session

    assert session is not None

    assert session.simulation_name == "Unit Test"

    assert session.total_steps == 10

    assert session.asset_count == 1

    assert session.scenario_count == 0


# ==========================================================
# Status
# ==========================================================


def test_engine_status():

    engine = create_engine()

    status = engine.status()

    assert status["simulation_name"] == "Unit Test"

    assert status["completed"] is False


# ==========================================================
# Run
# ==========================================================


def test_engine_run():

    engine = create_engine()

    result = engine.run()

    assert result.success is True

    assert result.simulation_steps == 10


# ==========================================================
# Results
# ==========================================================


def test_engine_results():

    engine = create_engine()

    engine.run()

    results = engine.results()

    assert results.success is True

    assert results.total_assets == 1


# ==========================================================
# Reset
# ==========================================================


def test_engine_reset():

    engine = create_engine()

    engine.reset()

    assert engine.session is None


# ==========================================================
# Session Property
# ==========================================================


def test_session_property():

    engine = create_engine()

    assert engine.session is not None

    assert engine.session.simulation_name == "Unit Test"
