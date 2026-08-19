"""
Track Digital Operations Sandbox (TDOS)

engine.py

Core simulation engine responsible for executing TDOS simulations.
"""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from tdos.config.logging import log
from tdos.config.settings import settings
from tdos.digital_twin.clone_manager import CloneManager
from tdos.models.asset import RailwayAsset
from tdos.models.results import (
    AssetResult,
    PredictionResult,
    SimulationResult,
)
from tdos.models.scenario import SimulationScenario
from tdos.models.simulation import SimulationSession
from tdos.prediction.prediction_engine import PredictionEngine
from tdos.replay.replay_engine import ReplayEngine
from tdos.rams.models import RAMSResult
from tdos.rams.rams_engine import RAMSEngine


class SimulationEngine:
    """
    Core TDOS Simulation Engine.

    Responsible for orchestrating the complete
    simulation lifecycle and building the
    final analytical result.
    """

    def __init__(self) -> None:
        self._session: SimulationSession | None = None

        # Digital Twin management
        self.clone_manager = CloneManager()

        # Simulation replay
        self.replay_engine = ReplayEngine()

    # ==========================================================
    # Session Management
    # ==========================================================

    def create_session(
        self,
        name: str,
        assets: list[RailwayAsset],
        scenarios: list[SimulationScenario],
        total_steps: int = 1000,
    ) -> SimulationSession:

        # Start every new simulation with a clean
        # Digital Twin registry.
        self.clone_manager.clear()

        # Start every new simulation with a clean
        # replay history.
        self.replay_engine.reset()

        # Create one Digital Twin for every participating asset.
        self.clone_manager.create_twins(assets)

        session = SimulationSession(
            simulation_id=f"SIM-{uuid4().hex[:8].upper()}",
            simulation_name=name,
            assets=assets,
            scenarios=scenarios,
            total_steps=total_steps,
            status="INITIALIZING",
        )

        self._session = session

        log.info(
            f"Simulation created: {session.simulation_id}"
        )

        log.info(
            f"Digital Twins initialized: "
            f"{self.clone_manager.count}"
        )

        return session

    # ==========================================================
    # Run
    # ==========================================================

    def run(self) -> SimulationResult:

        if self._session is None:
            raise RuntimeError(
                "Simulation session not initialized."
            )

        log.info("Starting simulation...")

        session = self._session.model_copy(
            update={
                "status": "RUNNING",
                "started_at": datetime.now(),
            }
        )

        self._session = session

        # ------------------------------------------------------
        # Start replay recording
        # ------------------------------------------------------

        self.replay_engine.start()

        # ------------------------------------------------------
        # Main Simulation Loop
        # ------------------------------------------------------

        for step in range(session.total_steps):

            session = session.model_copy(
                update={
                    "current_step": step + 1,
                    "progress": (
                        (step + 1)
                        / session.total_steps
                    ) * 100,
                }
            )

            # --------------------------------------------------
            # Event processing
            # --------------------------------------------------

            self._process_events(session)

            # --------------------------------------------------
            # Asset state update
            # --------------------------------------------------

            self._update_assets(session)

            # _update_assets() updates self._session because
            # RailwayAsset is frozen.
            session = self._session

            assert session is not None

            # --------------------------------------------------
            # Scenario execution
            # --------------------------------------------------

            self._execute_scenarios(session)

            # --------------------------------------------------
            # Synchronize Digital Twins
            # --------------------------------------------------

            self.clone_manager.synchronize(
                session.assets
            )

            # --------------------------------------------------
            # Record simulation state for replay
            # --------------------------------------------------

            self.replay_engine.record(
                session.current_step,
                session.assets,
            )

        # ------------------------------------------------------
        # Stop replay recording
        # ------------------------------------------------------

        self.replay_engine.stop()

        finished_at = datetime.now()

        session = session.model_copy(
            update={
                "status": "COMPLETED",
                "completed": True,
                "finished_at": finished_at,
            }
        )

        self._session = session

        log.success(
            "Simulation completed."
        )

        return self._build_result()

    # ==========================================================
    # Internal Pipeline
    # ==========================================================

    def _process_events(
        self,
        session: SimulationSession,
    ) -> None:

        log.debug(
            f"Step {session.current_step}: "
            "Processing events."
        )

    def _update_assets(
        self,
        session: SimulationSession,
    ) -> None:
        """
        Applies the configured degradation rate to
        every active asset for one simulation cycle.

        RailwayAsset is frozen, therefore updated assets
        are created using model_copy().
        """

        updated_assets: list[RailwayAsset] = []

        for asset in session.assets:

            # Failed or inactive assets no longer degrade
            # through the normal operational cycle.
            if not asset.active or asset.failed:

                updated_assets.append(asset)

                continue

            # degradation_rate is defined by RailwayAsset
            # as health degradation per simulation cycle.
            new_health = max(
                0.0,
                asset.health_score
                - asset.degradation_rate,
            )

            updated_assets.append(
                asset.model_copy(
                    update={
                        "health_score": new_health,
                        "failed": new_health < 40,
                    }
                )
            )

        updated_session = session.model_copy(
            update={
                "assets": updated_assets,
            }
        )

        self._session = updated_session

        log.debug(
            f"Step {session.current_step}: "
            "Updating assets."
        )

    def _execute_scenarios(
        self,
        session: SimulationSession,
    ) -> None:

        log.debug(
            f"Step {session.current_step}: "
            "Executing scenarios."
        )

    # ==========================================================
    # Result Builder
    # ==========================================================

    def _build_result(self) -> SimulationResult:

        assert self._session is not None

        assets = self._session.assets

        # ------------------------------------------------------
        # Asset Health Summary
        # ------------------------------------------------------

        healthy = sum(
            1
            for asset in assets
            if asset.health_score >= 80
        )

        degraded = sum(
            1
            for asset in assets
            if 40 <= asset.health_score < 80
        )

        failed = sum(
            1
            for asset in assets
            if asset.health_score < 40
        )

        average = (
            sum(
                asset.health_score
                for asset in assets
            )
            / len(assets)
            if assets
            else 0.0
        )

        # ------------------------------------------------------
        # Existing TDOS Prediction Engine
        # ------------------------------------------------------

        prediction_engine = PredictionEngine()

        asset_results: list[AssetResult] = []
        predictions: list[PredictionResult] = []

        for asset in assets:

            prediction = prediction_engine.predict(
                asset
            )

            predictions.append(prediction)

            predicted_risk = (
                prediction_engine
                .risk_predictor
                .risk_level(
                    prediction.failure_probability
                )
            )

            degradation = max(
                0.0,
                asset.health_score
                - prediction.predicted_health_score,
            )

            asset_results.append(
                AssetResult(
                    asset_id=asset.asset_id,
                    health_score=asset.health_score,
                    degradation=round(
                        degradation,
                        3,
                    ),
                    predicted_risk=predicted_risk,
                    maintenance_required=(
                        asset.requires_maintenance
                    ),
                    failed=(
                        asset.health_score < 40
                    ),
                )
            )

        # ------------------------------------------------------
        # Fleet-Level Prediction
        # ------------------------------------------------------

        prediction: PredictionResult | None = None

        if predictions:

            prediction = PredictionResult(

                failure_probability=round(
                    sum(
                        item.failure_probability
                        for item in predictions
                    )
                    / len(predictions),
                    3,
                ),

                remaining_useful_life_days=int(
                    sum(
                        item.remaining_useful_life_days
                        for item in predictions
                    )
                    / len(predictions)
                ),

                predicted_health_score=round(
                    sum(
                        item.predicted_health_score
                        for item in predictions
                    )
                    / len(predictions),
                    2,
                ),

                confidence=round(
                    sum(
                        item.confidence
                        for item in predictions
                    )
                    / len(predictions),
                    3,
                ),
            )

        # ------------------------------------------------------
        # Simulation Duration
        # ------------------------------------------------------

        duration_seconds = 0.0

        if (
            self._session.started_at is not None
            and self._session.finished_at is not None
        ):

            duration_seconds = max(
                0.0,
                (
                    self._session.finished_at
                    - self._session.started_at
                ).total_seconds(),
            )

        # ------------------------------------------------------
        # Final Simulation Result
        # ------------------------------------------------------

        return SimulationResult(

            simulation_id=(
                self._session.simulation_id
            ),

            simulation_name=(
                self._session.simulation_name
            ),

            success=True,

            duration_seconds=duration_seconds,

            simulation_steps=(
                self._session.total_steps
            ),

            scenarios=(
                self._session.scenarios
            ),

            assets=assets,

            asset_results=asset_results,

            prediction=prediction,

            benchmark=None,

            total_assets=len(assets),

            healthy_assets=healthy,

            degraded_assets=degraded,

            failed_assets=failed,

            average_health_score=average,

            metadata={
                "engine": settings.engine_name,
                "version": settings.engine_version,
                "replay_frames": str(
                    self.replay_engine.total_frames
                ),
                "digital_twins": str(
                    self.clone_manager.count
                ),
            },
        )

    # ==========================================================
    # Public Helpers
    # ==========================================================

    def status(self) -> dict:
        """
        Returns the current simulation status.
        """

        if self._session is None:

            return {
                "initialized": False,
                "running": False,
                "completed": False,
            }

        status = self._session.summary()

        status["initialized"] = True
        status["running"] = self._session.status == "RUNNING"
        status["completed"] = self._session.status == "COMPLETED"

        return status

    def rams(self) -> RAMSResult:
        """
        Returns RAMS intelligence derived from the latest simulation result
        and recorded replay history.
        """

        result = self.results()
        return RAMSEngine().analyze(
            result,
            self.replay_engine.frames(),
        )

    def results(self) -> SimulationResult:
        """
        Returns the latest simulation result.
        """

        if self._session is None:

            raise RuntimeError(
                "Simulation has not been created."
            )

        return self._build_result()

    # ==========================================================
    # Utilities
    # ==========================================================

    @property
    def session(
        self,
    ) -> SimulationSession | None:
        """
        Returns the current simulation session.
        """

        return self._session

    def reset(self) -> None:
        """
        Clears the current simulation.
        """

        self._session = None

        self.clone_manager.clear()

        self.replay_engine.reset()

        log.info(
            "Simulation engine reset."
        )