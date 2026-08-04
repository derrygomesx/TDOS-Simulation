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

from tdos.models.asset import RailwayAsset
from tdos.models.results import SimulationResult
from tdos.models.scenario import SimulationScenario
from tdos.models.simulation import SimulationSession


class SimulationEngine:
    """
    Core TDOS Simulation Engine.

    Responsible for orchestrating the complete
    simulation lifecycle.
    """

    def __init__(self) -> None:

        self._session: SimulationSession | None = None

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

        session = SimulationSession(
            simulation_id=f"SIM-{uuid4().hex[:8].upper()}",
            simulation_name=name,
            assets=assets,
            scenarios=scenarios,
            total_steps=total_steps,
            status="INITIALIZING",
        )

        self._session = session

        log.info(f"Simulation created: {session.simulation_id}")

        return session

    # ==========================================================
    # Run
    # ==========================================================

    def run(self) -> SimulationResult:

        if self._session is None:
            raise RuntimeError("Simulation session not initialized.")

        log.info("Starting simulation...")

        session = self._session.model_copy(
            update={
                "status": "RUNNING",
                "started_at": datetime.now(),
            }
        )

        # -----------------------------------------------
        # Main Simulation Loop
        # -----------------------------------------------

        for step in range(session.total_steps):

            session = session.model_copy(
                update={
                    "current_step": step + 1,
                    "progress": ((step + 1) / session.total_steps) * 100,
                }
            )

            self._process_events(session)

            self._update_assets(session)

            self._execute_scenarios(session)

        session = session.model_copy(
            update={
                "status": "COMPLETED",
                "completed": True,
                "finished_at": datetime.now(),
            }
        )

        self._session = session

        log.success("Simulation completed.")

        return self._build_result()

    # ==========================================================
    # Internal Pipeline
    # ==========================================================

    def _process_events(
        self,
        session: SimulationSession,
    ) -> None:

        log.debug(f"Step {session.current_step}: Processing events.")

    def _update_assets(
        self,
        session: SimulationSession,
    ) -> None:

        log.debug(f"Step {session.current_step}: Updating assets.")

    def _execute_scenarios(
        self,
        session: SimulationSession,
    ) -> None:

        log.debug(f"Step {session.current_step}: Executing scenarios.")

    # ==========================================================
    # Result Builder
    # ==========================================================

    def _build_result(self) -> SimulationResult:

        assert self._session is not None

        assets = self._session.assets

        healthy = sum(1 for asset in assets if asset.health_score >= 80)

        degraded = sum(1 for asset in assets if 40 <= asset.health_score < 80)

        failed = sum(1 for asset in assets if asset.health_score < 40)

        average = sum(a.health_score for a in assets) / len(assets) if assets else 0.0

        return SimulationResult(
            simulation_id=self._session.simulation_id,
            simulation_name=self._session.simulation_name,
            success=True,
            duration_seconds=0.0,
            simulation_steps=self._session.total_steps,
            scenarios=self._session.scenarios,
            assets=assets,
            asset_results=[],
            prediction=None,
            benchmark=None,
            total_assets=len(assets),
            healthy_assets=healthy,
            degraded_assets=degraded,
            failed_assets=failed,
            average_health_score=average,
            metadata={
                "engine": settings.engine_name,
                "version": settings.engine_version,
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

        return self._session.summary()

    def results(self) -> SimulationResult:
        """
        Returns the latest simulation result.
        """

        if self._session is None:

            raise RuntimeError("Simulation has not been created.")

        return self._build_result()

    # ==========================================================
    # Utilities
    # ==========================================================

    @property
    def session(self) -> SimulationSession | None:
        """
        Returns the current simulation session.
        """

        return self._session

    def reset(self) -> None:
        """
        Clears the current simulation.
        """

        self._session = None

        log.info("Simulation engine reset.")
