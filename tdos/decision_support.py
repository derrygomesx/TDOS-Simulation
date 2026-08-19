"""TDOS decision-support and maintenance recommendation engine."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from tdos.rams.models import RAMSAssetResult, RAMSResult


@dataclass(frozen=True)
class MaintenanceDecision:
    asset_id: str
    asset_name: str
    asset_type: str
    priority: str
    action: str
    timing: str
    reason: str
    health_score: float
    rams_score: float
    failure_probability: float
    remaining_useful_life_days: int
    criticality: str
    maintenance_required: bool
    factors: dict[str, float]


class DecisionSupportEngine:
    """Converts TDOS/RAMS outputs into explainable operator actions."""

    def analyze(self, rams: RAMSResult) -> dict:
        decisions = [self._decide(asset) for asset in rams.assets]
        priority_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        decisions.sort(key=lambda x: (priority_order[x.priority], x.rams_score))
        counts = {p: sum(d.priority == p for d in decisions) for p in priority_order}
        return {
            "simulation_id": rams.simulation_id,
            "simulation_name": rams.simulation_name,
            "methodology": "Rule-based, explainable maintenance decisions derived from TDOS health, failure probability, RUL and RAMS outputs.",
            "summary": {
                "critical": counts["CRITICAL"],
                "high": counts["HIGH"],
                "medium": counts["MEDIUM"],
                "low": counts["LOW"],
                "immediate_actions": counts["CRITICAL"],
                "planned_actions": counts["HIGH"] + counts["MEDIUM"],
            },
            "decisions": [d.__dict__ for d in decisions],
        }

    def what_if(self, rams: RAMSResult, asset_id: str, health_recovery: float = 15.0, degradation_reduction_percent: float = 30.0) -> dict:
        asset = next((a for a in rams.assets if a.asset_id == asset_id), None)
        if asset is None:
            raise KeyError(f"Asset '{asset_id}' not found in RAMS analysis.")
        health_recovery = max(0.0, min(50.0, health_recovery))
        degradation_reduction_percent = max(0.0, min(100.0, degradation_reduction_percent))
        before = self._decide(asset)
        new_health = min(100.0, asset.health_score + health_recovery)
        new_failure_probability = max(0.0, asset.failure_probability * (1.0 - health_recovery / 100.0))
        new_rams = min(100.0, asset.rams_score + health_recovery * 0.65 + degradation_reduction_percent * 0.08)
        simulated = RAMSAssetResult(
            asset_id=asset.asset_id, asset_name=asset.asset_name, asset_type=asset.asset_type,
            rams_score=new_rams, rams_grade=self._grade(new_rams),
            reliability=asset.reliability, availability=asset.availability,
            maintainability=asset.maintainability, safety=asset.safety,
            failure_probability=new_failure_probability,
            remaining_useful_life_days=int(asset.remaining_useful_life_days + health_recovery * 4),
            maintenance_priority=asset.maintenance_priority, criticality=asset.criticality,
            operational_availability_percent=asset.operational_availability_percent,
            health_score=new_health, failed=False,
        )
        after = self._decide(simulated)
        return {
            "asset_id": asset.asset_id,
            "asset_name": asset.asset_name,
            "intervention": {"health_recovery": health_recovery, "degradation_reduction_percent": degradation_reduction_percent},
            "before": before.__dict__,
            "after": after.__dict__,
            "changes": {
                "health_score": round(new_health - asset.health_score, 2),
                "rams_score": round(new_rams - asset.rams_score, 2),
                "failure_probability": round(new_failure_probability - asset.failure_probability, 4),
                "remaining_useful_life_days": after.remaining_useful_life_days - asset.remaining_useful_life_days,
            },
        }

    def what_if_batch(self, rams: RAMSResult, scenarios: list[dict]) -> dict:
        """Evaluate multiple independent maintenance what-if scenarios."""
        results = []
        for index, scenario in enumerate(scenarios, start=1):
            asset_id = str(scenario.get("asset_id", ""))
            result = self.what_if(
                rams,
                asset_id,
                float(scenario.get("health_recovery", 15.0)),
                float(scenario.get("degradation_reduction_percent", 30.0)),
            )
            result["scenario_id"] = str(scenario.get("scenario_id", f"MW-{index:02d}"))
            result["scenario_name"] = str(scenario.get("scenario_name", f"Maintenance Scenario {index}"))
            results.append(result)
        return {
            "simulation_id": rams.simulation_id,
            "scenario_count": len(results),
            "scenarios": results,
        }

    def _decide(self, a: RAMSAssetResult) -> MaintenanceDecision:
        if (
            a.failed
            or a.health_score < 40
            or a.failure_probability >= 0.50
        ):
            priority, action, timing = (
                "CRITICAL",
                "Immediate detailed inspection and isolate/repair if confirmed.",
                "NOW",
            )
        elif a.health_score < 60 or a.failure_probability >= 0.35 or a.remaining_useful_life_days <= 30 or a.rams_score < 65:
            priority, action, timing = "HIGH", "Schedule targeted maintenance intervention and engineering inspection.", "WITHIN 7 DAYS"
        elif a.health_score < 75 or a.failure_probability >= 0.20 or a.remaining_useful_life_days <= 90 or a.rams_score < 80:
            priority, action, timing = "MEDIUM", "Increase condition monitoring and plan maintenance work.", "WITHIN 30 DAYS"
        else:
            priority, action, timing = "LOW", "Continue routine monitoring and scheduled inspection.", "ROUTINE"
        reasons = []
        if a.health_score < 75: reasons.append(f"health {a.health_score:.1f}")
        if a.failure_probability >= 0.20: reasons.append(f"failure probability {a.failure_probability*100:.1f}%")
        if a.remaining_useful_life_days <= 90: reasons.append(f"RUL {a.remaining_useful_life_days} days")
        if a.safety.score < 80: reasons.append(f"safety score {a.safety.score:.1f}")
        if not reasons: reasons.append("asset remains within routine operating thresholds")
        return MaintenanceDecision(a.asset_id, a.asset_name, a.asset_type, priority, action, timing, "; ".join(reasons), a.health_score, a.rams_score, a.failure_probability, a.remaining_useful_life_days, a.criticality, a.maintenance_priority != "ROUTINE" or a.health_score < 75, {"health": round(a.health_score,2), "rams": round(a.rams_score,2), "failure_probability": round(a.failure_probability*100,2), "rul_days": float(a.remaining_useful_life_days), "safety": round(a.safety.score,2)})

    @staticmethod
    def _grade(score: float) -> str:
        if score >= 90: return "EXCELLENT"
        if score >= 80: return "GOOD"
        if score >= 65: return "WATCH"
        if score >= 50: return "DEGRADED"
        return "CRITICAL"
