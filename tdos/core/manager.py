"""
Track Digital Operations Sandbox (TDOS)

manager.py

High-level simulation manager.
"""

from __future__ import annotations

from typing import Dict

from tdos.config.logging import log
from tdos.core.engine import SimulationEngine
from tdos.models.asset import RailwayAsset
from tdos.models.results import SimulationResult
from tdos.models.scenario import SimulationScenario
from tdos.models.simulation import SimulationSession


class SimulationManager:
    """
    High-level controller responsible for creating,
    executing, and managing TDOS simulations.
    """

    def __init__(self) -> None:

        self._engine = SimulationEngine()

        self._sessions: Dict[str, SimulationSession] = {}

    # ==========================================================
    # Create Simulation
    # ==========================================================

    def create_simulation(
        self,
        name: str,
        assets: list[RailwayAsset],
        scenarios: list[SimulationScenario],
        total_steps: int = 1000,
    ) -> SimulationSession:

        session = self._engine.create_session(
            name=name,
            assets=assets,
            scenarios=scenarios,
            total_steps=total_steps,
        )

        self._sessions[session.simulation_id] = session

        log.info(f"Simulation registered: {session.simulation_id}")

        return session

    # ==========================================================
    # Execute
    # ==========================================================

    def run(self) -> SimulationResult:

        log.info("Executing simulation...")

        result = self._engine.run()

        if self._engine.session is not None:
            self._sessions[result.simulation_id] = self._engine.session

        return result

    # ==========================================================
    # Session Access
    # ==========================================================

    def get_session(
        self,
        simulation_id: str,
    ) -> SimulationSession | None:

        return self._sessions.get(simulation_id)

    def list_sessions(self) -> list[SimulationSession]:

        return list(self._sessions.values())

    # ==========================================================
    # Simulation Controls
    # ==========================================================

    def pause(self) -> None:

        session = self._engine.session

        if session is None:
            return

        self._engine._session = session.model_copy(
            update={
                "status": "PAUSED",
                "paused": True,
            }
        )

        log.warning("Simulation paused.")

    def resume(self) -> None:

        session = self._engine.session

        if session is None:
            return

        self._engine._session = session.model_copy(
            update={
                "status": "RUNNING",
                "paused": False,
            }
        )

        log.info("Simulation resumed.")

    def stop(self) -> None:

        session = self._engine.session

        if session is None:
            return

        self._engine._session = session.model_copy(
            update={
                "status": "CANCELLED",
                "completed": True,
            }
        )

        log.error("Simulation cancelled.")

    # ==========================================================
    # Cleanup
    # ==========================================================

    def remove(
        self,
        simulation_id: str,
    ) -> bool:

        if simulation_id not in self._sessions:
            return False

        del self._sessions[simulation_id]

        log.info(f"Simulation removed: {simulation_id}")

        return True

    def clear(self) -> None:

        self._sessions.clear()

        self._engine.reset()

        log.info("Simulation manager cleared.")

    # ==========================================================
    # Statistics
    # ==========================================================

    @property
    def total_simulations(self) -> int:

        return len(self._sessions)

    @property
    def active_simulation(self) -> SimulationSession | None:

        return self._engine.session
