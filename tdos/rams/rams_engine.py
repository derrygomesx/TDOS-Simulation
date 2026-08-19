"""
Track Digital Operations Sandbox (TDOS)

rams/rams_engine.py

Deterministic RAMS analysis built on top of existing TDOS simulation
results and recorded replay frames.
"""

from __future__ import annotations

from collections.abc import Iterable

from tdos.models.asset import RailwayAsset
from tdos.models.results import PredictionResult, SimulationResult
from tdos.rams.models import RAMSAssetResult, RAMSComponentScore, RAMSFleetSummary, RAMSResult


class RAMSEngine:
    """
    Calculates Reliability, Availability, Maintainability and Safety
    indices from existing TDOS outputs.

    Important:
        TDOS currently does not simulate repair duration, MTTR or field
        maintenance work orders. Therefore maintainability is explicitly
        represented as a deterministic *maintenance readiness proxy* rather
        than a standards-certified MTTR metric. Availability is measured
        directly from recorded replay uptime snapshots.
    """

    WEIGHTS = {
        "reliability": 0.30,
        "availability": 0.25,
        "maintainability": 0.20,
        "safety": 0.25,
    }

    CRITICALITY_BY_TYPE = {
        "BRIDGE": 1.00,
        "RAIL": 0.95,
        "TURNOUT": 0.90,
        "SIGNAL": 0.85,
        "SLEEPER": 0.65,
        "BALLAST": 0.60,
        "FASTENER": 0.55,
    }

    def analyze(
        self,
        result: SimulationResult,
        replay_frames: Iterable[object] | None = None,
    ) -> RAMSResult:
        frames = list(replay_frames or [])
        asset_lookup = {asset.asset_id: asset for asset in result.assets}
        prediction_lookup = self._predictions_by_asset(result)

        analyzed: list[RAMSAssetResult] = []

        for asset_result in result.asset_results:
            asset = asset_lookup.get(asset_result.asset_id)
            if asset is None:
                continue

            prediction = prediction_lookup.get(asset.asset_id)
            if prediction is None:
                continue

            availability = self._availability(asset, frames)
            reliability = self._reliability(prediction)
            maintainability = self._maintainability(asset, prediction)
            safety, criticality = self._safety(asset, prediction)

            overall = self._weighted_score(
                reliability.score,
                availability.score,
                maintainability.score,
                safety.score,
            )

            analyzed.append(
                RAMSAssetResult(
                    asset_id=asset.asset_id,
                    asset_name=asset.asset_name,
                    asset_type=asset.asset_type,
                    rams_score=round(overall, 2),
                    rams_grade=self.grade(overall),
                    reliability=reliability,
                    availability=availability,
                    maintainability=maintainability,
                    safety=safety,
                    failure_probability=prediction.failure_probability,
                    remaining_useful_life_days=prediction.remaining_useful_life_days,
                    maintenance_priority=self._maintenance_priority(asset, prediction),
                    criticality=criticality,
                    operational_availability_percent=availability.score,
                    health_score=asset.health_score,
                    failed=asset.failed,
                )
            )

        fleet = self._fleet_summary(analyzed, frames)

        return RAMSResult(
            simulation_id=result.simulation_id,
            simulation_name=result.simulation_name,
            methodology=(
                "RAMS index derived from TDOS prediction outputs and replay uptime. "
                "Maintainability is a maintenance-readiness proxy because TDOS does not "
                "yet model repair duration or work-order execution."
            ),
            weights=self.WEIGHTS.copy(),
            fleet=fleet,
            assets=analyzed,
        )

    @staticmethod
    def grade(score: float) -> str:
        if score >= 90:
            return "EXCELLENT"
        if score >= 80:
            return "GOOD"
        if score >= 65:
            return "WATCH"
        if score >= 50:
            return "DEGRADED"
        return "CRITICAL"

    @staticmethod
    def _predictions_by_asset(result: SimulationResult) -> dict[str, PredictionResult]:
        """
        Reconstruct per-asset prediction inputs from the public result.

        The current SimulationResult exposes only fleet-level prediction, so
        the same deterministic prediction models used by the engine are
        executed again for RAMS. This keeps RAMS independent of private state.
        """
        from tdos.prediction.prediction_engine import PredictionEngine

        predictor = PredictionEngine()
        return {
            asset.asset_id: predictor.predict(asset)
            for asset in result.assets
        }

    def _reliability(self, prediction: PredictionResult) -> RAMSComponentScore:
        score = max(0.0, min(100.0, (1.0 - prediction.failure_probability) * 100.0))
        return RAMSComponentScore(
            score=round(score, 2),
            grade=self.grade(score),
            rationale=f"Failure probability {prediction.failure_probability * 100:.1f}%.",
        )

    def _availability(
        self,
        asset: RailwayAsset,
        frames: list[object],
    ) -> RAMSComponentScore:
        if not frames:
            score = 0.0 if asset.failed else 100.0
            rationale = "Derived from final operational state because no replay frames were supplied."
        else:
            operational = 0
            observed = 0
            for frame in frames:
                frame_assets = getattr(frame, "assets", None)
                if frame_assets is None and isinstance(frame, dict):
                    frame_assets = frame.get("assets", [])
                for snapshot in frame_assets or []:
                    snapshot_id = getattr(snapshot, "asset_id", None)
                    if snapshot_id is None and isinstance(snapshot, dict):
                        snapshot_id = snapshot.get("asset_id")
                    if snapshot_id != asset.asset_id:
                        continue
                    observed += 1
                    failed = getattr(snapshot, "failed", False)
                    active = getattr(snapshot, "active", True)
                    if isinstance(snapshot, dict):
                        failed = snapshot.get("failed", False)
                        active = snapshot.get("active", True)
                    if active and not failed:
                        operational += 1
            score = (operational / observed * 100.0) if observed else (0.0 if asset.failed else 100.0)
            rationale = f"Operational in {operational}/{observed} recorded replay snapshots." if observed else "No asset snapshots were recorded."

        return RAMSComponentScore(
            score=round(score, 2),
            grade=self.grade(score),
            rationale=rationale,
        )

    def _maintainability(
        self,
        asset: RailwayAsset,
        prediction: PredictionResult,
    ) -> RAMSComponentScore:
        """Maintenance-readiness proxy, not an MTTR measurement."""
        health_factor = asset.health_score
        rul_factor = min(100.0, prediction.remaining_useful_life_days / 365.0 * 100.0)
        urgency_penalty = 25.0 if asset.requires_maintenance else 0.0
        failure_penalty = 35.0 if asset.failed else 0.0
        score = max(0.0, min(100.0, 0.55 * health_factor + 0.45 * rul_factor - urgency_penalty - failure_penalty))
        return RAMSComponentScore(
            score=round(score, 2),
            grade=self.grade(score),
            rationale=(
                f"Readiness proxy from health {asset.health_score:.1f}, "
                f"RUL {prediction.remaining_useful_life_days} days and maintenance state."
            ),
        )

    def _safety(
        self,
        asset: RailwayAsset,
        prediction: PredictionResult,
    ) -> tuple[RAMSComponentScore, str]:
        criticality_factor = self.CRITICALITY_BY_TYPE.get(asset.asset_type.upper(), 0.70)
        criticality = self._criticality_label(criticality_factor)
        health_risk = (100.0 - asset.health_score) / 100.0
        safety_risk = (
            0.65 * prediction.failure_probability
            + 0.25 * health_risk
            + 0.10 * criticality_factor
        )
        score = max(0.0, min(100.0, (1.0 - safety_risk) * 100.0))
        return (
            RAMSComponentScore(
                score=round(score, 2),
                grade=self.grade(score),
                rationale=(
                    f"Combines predicted failure risk, current health degradation and "
                    f"asset-type criticality ({criticality})."
                ),
            ),
            criticality,
        )

    @staticmethod
    def _criticality_label(factor: float) -> str:
        if factor >= 0.90:
            return "CRITICAL"
        if factor >= 0.75:
            return "HIGH"
        if factor >= 0.60:
            return "MEDIUM"
        return "LOW"

    @staticmethod
    def _maintenance_priority(
        asset: RailwayAsset,
        prediction: PredictionResult,
    ) -> str:
        if asset.failed or prediction.failure_probability >= 0.80:
            return "IMMEDIATE"
        if asset.requires_maintenance or prediction.failure_probability >= 0.60 or prediction.remaining_useful_life_days < 90:
            return "HIGH"
        if prediction.failure_probability >= 0.35 or prediction.remaining_useful_life_days < 180:
            return "MEDIUM"
        return "ROUTINE"

    def _fleet_summary(
        self,
        assets: list[RAMSAssetResult],
        frames: list[object],
    ) -> RAMSFleetSummary:
        if not assets:
            return RAMSFleetSummary(
                rams_score=0.0,
                rams_grade="CRITICAL",
                reliability_score=0.0,
                availability_score=0.0,
                maintainability_score=0.0,
                safety_score=0.0,
                critical_assets=0,
                immediate_maintenance=0,
                high_priority_maintenance=0,
                fleet_operational_availability_percent=0.0,
            )

        mean = lambda values: sum(values) / len(values)
        fleet_availability = mean([item.availability.score for item in assets])
        fleet_reliability = mean([item.reliability.score for item in assets])
        fleet_maintainability = mean([item.maintainability.score for item in assets])
        fleet_safety = mean([item.safety.score for item in assets])
        overall = self._weighted_score(
            fleet_reliability,
            fleet_availability,
            fleet_maintainability,
            fleet_safety,
        )

        return RAMSFleetSummary(
            rams_score=round(overall, 2),
            rams_grade=self.grade(overall),
            reliability_score=round(fleet_reliability, 2),
            availability_score=round(fleet_availability, 2),
            maintainability_score=round(fleet_maintainability, 2),
            safety_score=round(fleet_safety, 2),
            critical_assets=sum(1 for item in assets if item.criticality == "CRITICAL" or item.rams_score < 50),
            immediate_maintenance=sum(1 for item in assets if item.maintenance_priority == "IMMEDIATE"),
            high_priority_maintenance=sum(1 for item in assets if item.maintenance_priority == "HIGH"),
            fleet_operational_availability_percent=round(fleet_availability, 2),
        )

    @classmethod
    def _weighted_score(cls, reliability: float, availability: float, maintainability: float, safety: float) -> float:
        return (
            reliability * cls.WEIGHTS["reliability"]
            + availability * cls.WEIGHTS["availability"]
            + maintainability * cls.WEIGHTS["maintainability"]
            + safety * cls.WEIGHTS["safety"]
        )
