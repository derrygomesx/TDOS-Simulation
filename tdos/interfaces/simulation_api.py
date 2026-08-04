"""
Track Digital Operations Sandbox (TDOS)

simulation_api.py

Public API for the TDOS Simulation Engine.
"""

from __future__ import annotations

from tdos.core.engine import SimulationEngine
from tdos.models.asset import RailwayAsset
from tdos.models.results import SimulationResult
from tdos.models.scenario import SimulationScenario
from tdos.models.simulation import SimulationSession


class SimulationAPI:
    """
    Public interface for interacting with the
    TDOS Simulation Engine.
    """

    def __init__(self) -> None:

        self.engine = SimulationEngine()

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
        """
        Create a new simulation session.
        """

        return self.engine.create_session(
            name=name,
            assets=assets,
            scenarios=scenarios,
            total_steps=total_steps,
        )

    # ==========================================================
    # Execution
    # ==========================================================

    def run(self) -> SimulationResult:
        """
        Execute the simulation.
        """

        return self.engine.run()

    # ==========================================================
    # Status
    # ==========================================================

    def status(self) -> dict:
        """
        Return simulation status.
        """

        return self.engine.status()

    # ==========================================================
    # Results
    # ==========================================================

    def results(self) -> SimulationResult:
        """
        Return simulation results.
        """

        return self.engine.results()

    # ==========================================================
    # Utilities
    # ==========================================================

    @property
    def session(self) -> SimulationSession | None:
        """
        Return the active simulation session.
        """

        return self.engine.session

    def reset(self) -> None:
        """
        Reset the simulation engine.
        """

        self.engine.reset()
