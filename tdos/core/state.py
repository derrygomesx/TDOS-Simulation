"""
Track Digital Operations Sandbox (TDOS)

state.py

Central simulation state model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Set


@dataclass(slots=True)
class SimulationState:
    """
    Represents the live runtime state of a TDOS simulation.

    Every subsystem references this object to obtain
    the current simulation status.
    """

    # ==========================================================
    # Time
    # ==========================================================

    current_step: int = 0

    simulation_time: float = 0.0

    delta_time: float = 1.0

    # ==========================================================
    # Lifecycle
    # ==========================================================

    initialized: bool = False

    running: bool = False

    paused: bool = False

    completed: bool = False

    cancelled: bool = False

    failed: bool = False

    # ==========================================================
    # Statistics
    # ==========================================================

    assets_loaded: int = 0

    active_assets: int = 0

    scenarios_loaded: int = 0

    active_scenarios: int = 0

    processed_events: int = 0

    replay_frames: int = 0

    predictions_generated: int = 0

    benchmark_runs: int = 0

    # ==========================================================
    # Runtime
    # ==========================================================

    random_seed: int = 42

    speed_multiplier: float = 1.0

    # ==========================================================
    # Tracking
    # ==========================================================

    enabled_modules: Set[str] = field(default_factory=set)

    active_events: Set[str] = field(default_factory=set)

    metadata: Dict[str, str] = field(default_factory=dict)

    # ==========================================================
    # Timing
    # ==========================================================

    started_at: datetime | None = None

    finished_at: datetime | None = None

    # ==========================================================
    # Lifecycle Controls
    # ==========================================================

    def start(self) -> None:
        """
        Starts the simulation.
        """

        self.initialized = True
        self.running = True
        self.paused = False
        self.completed = False
        self.cancelled = False
        self.failed = False

        self.started_at = datetime.now()

    def pause(self) -> None:
        """
        Pauses the simulation.
        """

        self.running = False
        self.paused = True

    def resume(self) -> None:
        """
        Resumes the simulation.
        """

        self.running = True
        self.paused = False

    def stop(self) -> None:
        """
        Completes the simulation.
        """

        self.running = False
        self.completed = True

        self.finished_at = datetime.now()

    def cancel(self) -> None:
        """
        Cancels the simulation.
        """

        self.running = False
        self.cancelled = True

        self.finished_at = datetime.now()

    def fail(self) -> None:
        """
        Marks the simulation as failed.
        """

        self.running = False
        self.failed = True

        self.finished_at = datetime.now()

    # ==========================================================
    # Progress
    # ==========================================================

    def advance(self) -> None:
        """
        Advances simulation by one timestep.
        """

        self.current_step += 1

        self.simulation_time += self.delta_time

    # ==========================================================
    # Helpers
    # ==========================================================

    @property
    def is_active(self) -> bool:
        """
        Returns True if the simulation is active.
        """

        return self.running and not self.paused

    @property
    def duration(self) -> float:
        """
        Returns elapsed simulation time.
        """

        return self.simulation_time

    # ==========================================================
    # Export
    # ==========================================================

    def summary(self) -> dict:
        """
        Returns a compact runtime summary.
        """

        return {
            "step": self.current_step,
            "time": self.simulation_time,
            "running": self.running,
            "paused": self.paused,
            "completed": self.completed,
            "assets": self.active_assets,
            "scenarios": self.active_scenarios,
            "events": self.processed_events,
            "predictions": self.predictions_generated,
        }
