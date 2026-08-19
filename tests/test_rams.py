from tdos.core.engine import SimulationEngine
from tdos.models.asset import RailwayAsset
from tdos.models.scenario import SimulationScenario
from tdos.rams.rams_engine import RAMSEngine


def asset(asset_id="AST-001", health=96.0, rate=0.08):
    return RailwayAsset(
        asset_id=asset_id,
        asset_name="Mainline Rail A",
        asset_type="RAIL",
        latitude=13.0827,
        longitude=80.2707,
        health_score=health,
        degradation_rate=rate,
        age_days=120,
    )


def scenario():
    return SimulationScenario(
        scenario_id="SCN-CRACK_GROWTH",
        name="CRACK_GROWTH",
        category="INFRASTRUCTURE",
        type="CRACK_GROWTH",
        severity=0.7,
        start_step=0,
        duration_steps=10,
    )


def test_rams_engine_produces_asset_and_fleet_scores():
    engine = SimulationEngine()
    session = engine.create_session("RAMS Test", [asset()], [scenario()], total_steps=10)
    result = engine.run()

    rams = RAMSEngine().analyze(result, engine.replay_engine.frames())

    assert rams.simulation_id == session.simulation_id
    assert len(rams.assets) == 1
    assert 0 <= rams.fleet.rams_score <= 100
    assert 0 <= rams.assets[0].reliability.score <= 100
    assert 0 <= rams.assets[0].availability.score <= 100
    assert 0 <= rams.assets[0].maintainability.score <= 100
    assert 0 <= rams.assets[0].safety.score <= 100
    assert rams.fleet.fleet_operational_availability_percent == 100.0


def test_rams_availability_detects_failed_replay_snapshots():
    engine = SimulationEngine()
    session = engine.create_session("RAMS Failure Test", [asset(health=41.0, rate=1.0)], [scenario()], total_steps=5)
    result = engine.run()

    rams = RAMSEngine().analyze(result, engine.replay_engine.frames())

    assert rams.assets[0].availability.score < 100.0
    assert rams.assets[0].maintenance_priority in {"HIGH", "IMMEDIATE"}
