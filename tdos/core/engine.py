"""
Track Digital Operations Sandbox (TDOS)

engine.py

Integrated simulation runtime for TDOS.
"""

from __future__ import annotations

from datetime import datetime
from random import Random
from time import perf_counter
from uuid import uuid4

from tdos.config.logging import log
from tdos.config.settings import settings
from tdos.core.event_bus import Event, EventBus
from tdos.digital_twin.clone_manager import CloneManager
from tdos.digital_twin.degradation import DegradationModel
from tdos.models.asset import RailwayAsset
from tdos.models.results import AssetResult, PredictionResult, SimulationResult
from tdos.models.scenario import SimulationScenario
from tdos.models.simulation import SimulationSession
from tdos.prediction.prediction_engine import PredictionEngine
from tdos.prediction.risk import RiskPredictor
from tdos.replay.replay_engine import ReplayEngine
from tdos.scenarios.registry import registry
# Import concrete scenarios so their registration side effects run.
from tdos.scenarios import infrastructure as _infrastructure
from tdos.scenarios import operations as _operations
from tdos.scenarios import sensors as _sensors
from tdos.scenarios import weather as _weather


class SimulationEngine:
    """Execute a complete deterministic TDOS simulation."""

    def __init__(self) -> None:
        self._session: SimulationSession | None = None
        self.event_bus = EventBus()
        self.degradation_model = DegradationModel()
        self.prediction_engine = PredictionEngine()
        self.replay_engine = ReplayEngine()
        self.clone_manager = CloneManager()
        self._rng = Random()
        self._scenario_instances = []
        self._scenario_triggered: dict[str, bool] = {}
        self._latest_predictions: dict[str, PredictionResult] = {}
        self._last_result: SimulationResult | None = None
        self._started_perf = 0.0

    def create_session(
        self,
        name: str,
        assets: list[RailwayAsset],
        scenarios: list[SimulationScenario],
        total_steps: int = 1000,
    ) -> SimulationSession:
        if total_steps <= 0:
            raise ValueError("total_steps must be greater than zero.")

        asset_ids = [asset.asset_id for asset in assets]
        if len(asset_ids) != len(set(asset_ids)):
            raise ValueError("Asset IDs must be unique.")

        scenario_ids = [scenario.scenario_id for scenario in scenarios]
        if len(scenario_ids) != len(set(scenario_ids)):
            raise ValueError("Scenario IDs must be unique.")

        session = SimulationSession(
            simulation_id=f"SIM-{uuid4().hex[:8].upper()}",
            simulation_name=name,
            assets=list(assets),
            scenarios=list(scenarios),
            total_steps=total_steps,
            status="INITIALIZING",
        )

        self._session = session
        self._last_result = None
        self._scenario_triggered = {scenario.scenario_id: False for scenario in scenarios}
        self._rng.seed(session.random_seed)
        self._scenario_instances = [self._build_scenario(scenario) for scenario in scenarios]
        self.clone_manager.clear()
        self.clone_manager.create_twins(session.assets)
        self._latest_predictions.clear()

        log.info("Simulation created: %s", session.simulation_id)
        return session

    def run(self) -> SimulationResult:
        if self._session is None:
            raise RuntimeError("Simulation session not initialized.")

        if self._session.completed:
            return self._last_result or self._build_result()

        self._started_perf = perf_counter()
        session = self._session.model_copy(
            update={
                "status": "RUNNING",
                "paused": False,
                "completed": False,
                "started_at": datetime.now(),
            }
        )
        self._session = session
        self.replay_engine.start()
        self.event_bus.publish(Event("START", "simulation_engine", {"simulation_id": session.simulation_id}))

        try:
            for step in range(session.current_step + 1, session.total_steps + 1):
                if self._session.paused or self._session.status != "RUNNING":
                    break

                self._tick(step)

            if self._session.status == "RUNNING":
                finished = datetime.now()
                self.replay_engine.stop()
                self._session = self._session.model_copy(
                    update={
                        "status": "COMPLETED",
                        "completed": True,
                        "paused": False,
                        "progress": 100.0,
                        "finished_at": finished,
                        "replay_frames": self.replay_engine.total_frames,
                    }
                )
                self.event_bus.publish(Event("STOP", "simulation_engine", {"simulation_id": self._session.simulation_id}))
                self._last_result = self._build_result()
                log.success("Simulation completed: %s", self._session.simulation_id)
                return self._last_result

            return self._build_result()
        except Exception:
            self.replay_engine.stop()
            self._session = self._session.model_copy(
                update={"status": "FAILED", "finished_at": datetime.now()}
            )
            self.event_bus.publish(Event("ERROR", "simulation_engine", {"simulation_id": self._session.simulation_id}))
            raise

    def _tick(self, step: int) -> None:
        assert self._session is not None

        self._activate_scenarios(step)
        self._process_events(step)
        assets = self._update_assets(self._session.assets, step)
        self._session = self._session.model_copy(
            update={
                "current_step": step,
                "progress": (step / self._session.total_steps) * 100.0,
                "assets": assets,
                "assets_updated": self._session.assets_updated + len(assets),
                "replay_frames": self.replay_engine.total_frames + 1,
            }
        )
        self._execute_predictions(assets)
        self.replay_engine.record(step, assets)
        self._session = self._session.model_copy(
            update={
                "predictions_generated": self._session.predictions_generated + len(assets),
                "replay_frames": self.replay_engine.total_frames,
            }
        )
        self.event_bus.publish(
            Event(
                "HEALTH_UPDATE",
                "simulation_engine",
                {"step": step, "asset_count": len(assets)},
            )
        )

    def _process_events(self, step: int) -> None:
        assert self._session is not None
        active = sum(1 for scenario in self._scenario_instances if scenario.active)
        self._session = self._session.model_copy(
            update={
                "events_processed": self._session.events_processed + active,
            }
        )
        if active:
            self.event_bus.publish(Event("SCENARIO", "scenario_engine", {"step": step, "active": active}))

    def _update_assets(self, assets: list[RailwayAsset], step: int) -> list[RailwayAsset]:
        updated: list[RailwayAsset] = []
        for asset in assets:
            current = asset
            scenario_factor = 1.0
            environmental_factor = 1.0
            operational_factor = 1.0

            for scenario in self._scenario_instances:
                if not scenario.active or not self._scenario_affects(scenario.config, current):
                    continue

                current = scenario.apply(current)
                category = scenario.category.upper()
                if category == "WEATHER":
                    environmental_factor *= 1.0 + scenario.severity
                elif category == "OPERATION":
                    operational_factor *= 1.0 + scenario.severity
                else:
                    scenario_factor *= 1.0 + scenario.severity

            current = self.degradation_model.apply(
                current,
                scenario_factor=scenario_factor,
                environmental_factor=environmental_factor,
                operational_factor=operational_factor,
            )

            failed = self.degradation_model.asset_failed(current.health_score)
            current = current.model_copy(
                update={
                    "failed": failed,
                    "active": current.active and not failed,
                }
            )
            self.clone_manager.update(current)
            updated.append(current)

        return updated

    def _execute_scenarios(self, session: SimulationSession) -> None:
        # Kept as a compatibility hook for callers that used the original engine.
        self._activate_scenarios(session.current_step)

    def _activate_scenarios(self, step: int) -> None:
        for scenario in self._scenario_instances:
            config = scenario.config
            if not config.enabled:
                scenario.stop()
                continue
            if step == config.start_step and not self._scenario_triggered[config.scenario_id]:
                self._scenario_triggered[config.scenario_id] = True
                if self._rng.random() <= config.probability:
                    scenario.start()
                    self.event_bus.publish(
                        Event("SCENARIO", "scenario_engine", {"scenario_id": config.scenario_id, "action": "START"})
                    )
            elif step > config.end_step and scenario.active:
                scenario.stop()
                self.event_bus.publish(
                    Event("SCENARIO", "scenario_engine", {"scenario_id": config.scenario_id, "action": "STOP"})
                )

    @staticmethod
    def _scenario_affects(config: SimulationScenario, asset: RailwayAsset) -> bool:
        if config.target_asset is not None and asset.asset_id != config.target_asset:
            return False
        if config.affected_assets and asset.asset_id not in config.affected_assets:
            return False
        return True

    @staticmethod
    def _build_scenario(config: SimulationScenario):
        if not registry.exists(config.name):
            raise ValueError(f"Scenario '{config.name}' is not registered.")
        return registry.create(config.name, config)

    def _execute_predictions(self, assets: list[RailwayAsset]) -> None:
        for asset in assets:
            self._latest_predictions[asset.asset_id] = self.prediction_engine.predict(asset)
            self.event_bus.publish(
                Event("PREDICTION", "prediction_engine", {"asset_id": asset.asset_id})
            )

    def _build_result(self) -> SimulationResult:
        assert self._session is not None

        assets = self._session.assets
        asset_results: list[AssetResult] = []
        predictions = list(self._latest_predictions.values())

        for asset in assets:
            prediction = self._latest_predictions.get(asset.asset_id) or self.prediction_engine.predict(asset)
            probability = prediction.failure_probability
            asset_results.append(
                AssetResult(
                    asset_id=asset.asset_id,
                    health_score=asset.health_score,
                    degradation=asset.degradation_rate,
                    predicted_risk=RiskPredictor.risk_level(probability),
                    maintenance_required=asset.requires_maintenance,
                    failed=asset.failed,
                )
            )

        healthy = sum(asset.health_score >= 80 for asset in assets)
        degraded = sum(40 <= asset.health_score < 80 for asset in assets)
        failed = sum(asset.health_score < 40 or asset.failed for asset in assets)
        average = sum(asset.health_score for asset in assets) / len(assets) if assets else 0.0
        duration = max(0.0, perf_counter() - self._started_perf) if self._started_perf else 0.0

        aggregate_prediction = None
        if predictions:
            aggregate_prediction = PredictionResult(
                failure_probability=max(p.failure_probability for p in predictions),
                remaining_useful_life_days=min(p.remaining_useful_life_days for p in predictions),
                predicted_health_score=sum(p.predicted_health_score for p in predictions) / len(predictions),
                confidence=sum(p.confidence for p in predictions) / len(predictions),
            )

        return SimulationResult(
            simulation_id=self._session.simulation_id,
            simulation_name=self._session.simulation_name,
            success=self._session.status == "COMPLETED",
            duration_seconds=duration,
            simulation_steps=self._session.current_step,
            scenarios=self._session.scenarios,
            assets=assets,
            asset_results=asset_results,
            prediction=aggregate_prediction,
            benchmark=None,
            total_assets=len(assets),
            healthy_assets=healthy,
            degraded_assets=degraded,
            failed_assets=failed,
            average_health_score=round(average, 3),
            metadata={
                "engine": settings.engine_name,
                "version": settings.engine_version,
                "events_processed": str(self._session.events_processed),
                "replay_frames": str(self.replay_engine.total_frames),
            },
        )

    def status(self) -> dict:
        if self._session is None:
            return {"initialized": False, "running": False, "completed": False}
        return {
            **self._session.summary(),
            "initialized": True,
            "running": self._session.status == "RUNNING",
            "paused": self._session.paused,
            "failed": self._session.status == "FAILED",
        }

    def results(self) -> SimulationResult:
        if self._session is None:
            raise RuntimeError("Simulation has not been created.")
        return self._last_result or self._build_result()

    @property
    def session(self) -> SimulationSession | None:
        return self._session

    def reset(self) -> None:
        self._session = None
        self._last_result = None
        self._scenario_instances.clear()
        self._scenario_triggered.clear()
        self._latest_predictions.clear()
        self.clone_manager.clear()
        self.replay_engine.reset()
        self.event_bus.clear()
        log.info("Simulation engine reset.")
