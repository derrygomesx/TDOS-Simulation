from tdos.decision_support import DecisionSupportEngine
from tdos.rams.models import RAMSAssetResult, RAMSComponentScore, RAMSFleetSummary, RAMSResult


def component(score):
    return RAMSComponentScore(score=score, grade="GOOD", rationale="test")


def sample():
    asset = RAMSAssetResult(
        asset_id="AST-001", asset_name="Rail A", asset_type="RAIL", rams_score=55,
        rams_grade="DEGRADED", reliability=component(50), availability=component(100),
        maintainability=component(55), safety=component(45), failure_probability=.55,
        remaining_useful_life_days=20, maintenance_priority="IMMEDIATE", criticality="HIGH",
        operational_availability_percent=100, health_score=52, failed=False,
    )
    fleet = RAMSFleetSummary(rams_score=55,rams_grade="DEGRADED",reliability_score=50,availability_score=100,
        maintainability_score=55,safety_score=45,critical_assets=1,immediate_maintenance=1,
        high_priority_maintenance=1,fleet_operational_availability_percent=100)
    return RAMSResult(simulation_id="SIM-TEST",simulation_name="Test",methodology="test",weights={},fleet=fleet,assets=[asset])


def test_decision_marks_high_risk_asset_critical():
    result = DecisionSupportEngine().analyze(sample())
    d = result["decisions"][0]
    assert d["priority"] == "CRITICAL"
    assert d["timing"] == "NOW"


def test_what_if_improves_rams():
    out = DecisionSupportEngine().what_if(sample(), "AST-001")
    assert out["after"]["rams_score"] > out["before"]["rams_score"]
    assert out["changes"]["health_score"] > 0
