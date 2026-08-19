from tdos.core.engine import SimulationEngine
from tdos.models.asset import RailwayAsset
from tdos.models.scenario import SimulationScenario


def asset():
    return RailwayAsset(
        asset_id="AST-001",
        asset_name="Test Rail",
        asset_type="RAIL",
        latitude=13.0,
        longitude=80.0,
        health_score=95.0,
        degradation_rate=0.05,
        age_days=30,
    )


def scenario():
    return SimulationScenario(
        scenario_id="SCN-001",
        name="CRACK_GROWTH",
        category="INFRASTRUCTURE",
        severity=0.5,
        probability=1.0,
        duration=5,
        start_step=1,
        target_asset="AST-001",
    )


def test_end_to_end_simulation_pipeline():
    engine = SimulationEngine()
    session = engine.create_session("Integration Test", [asset()], [scenario()], total_steps=10)
    result = engine.run()

    assert session.simulation_id == result.simulation_id
    assert result.success is True
    assert result.simulation_steps == 10
    assert result.total_assets == 1
    assert len(result.asset_results) == 1
    assert result.prediction is not None
    assert result.duration_seconds >= 0
    assert int(result.metadata["replay_frames"]) == 10
    assert result.assets[0].health_score < 95.0
    assert engine.replay_engine.total_frames == 10
    assert engine.clone_manager.count == 1
