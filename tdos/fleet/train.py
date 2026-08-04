"""
Track Digital Operations Sandbox (TDOS)

train.py

Simulation train model.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Train:
    """
    Represents a railway inspection train.
    """

    # ==========================================================
    # Identity
    # ==========================================================

    train_id: str

    train_name: str

    # ==========================================================
    # Position
    # ==========================================================

    current_position: float = 0.0

    destination: float = 0.0

    # ==========================================================
    # Motion
    # ==========================================================

    speed: float = 0.0

    max_speed: float = 120.0

    # ==========================================================
    # State
    # ==========================================================

    active: bool = True

    paused: bool = False

    completed: bool = False

    # ==========================================================
    # Statistics
    # ==========================================================

    distance_travelled: float = 0.0

    simulation_steps: int = 0

    metadata: dict[str, str] = field(default_factory=dict)

    # ==========================================================
    # Movement
    # ==========================================================

    def update(self) -> None:
        """
        Advance the train by one simulation step.
        """

        if not self.active:
            return

        if self.paused:
            return

        if self.completed:
            return

        movement = min(
            self.speed,
            self.remaining_distance,
        )

        self.current_position += movement

        self.distance_travelled += movement

        self.simulation_steps += 1

        if self.current_position >= self.destination:

            self.current_position = self.destination

            self.completed = True

            self.active = False

    # ==========================================================
    # Controls
    # ==========================================================

    def start(self) -> None:
        """
        Start train movement.
        """

        self.active = True

        self.paused = False

    def pause(self) -> None:
        """
        Pause train movement.
        """

        self.paused = True

    def resume(self) -> None:
        """
        Resume train movement.
        """

        self.paused = False

    def stop(self) -> None:
        """
        Stop the train.
        """

        self.active = False

    # ==========================================================
    # Utilities
    # ==========================================================

    @property
    def remaining_distance(self) -> float:
        """
        Remaining distance to destination.
        """

        return max(
            0.0,
            self.destination - self.current_position,
        )

    @property
    def progress(self) -> float:
        """
        Route completion percentage.
        """

        if self.destination == 0:
            return 0.0

        return round(
            (self.current_position / self.destination) * 100,
            2,
        )

    @property
    def arrived(self) -> bool:
        """
        Returns True if destination reached.
        """

        return self.completed

    # ==========================================================
    # Export
    # ==========================================================

    def summary(self) -> dict:
        """
        Returns train summary.
        """

        return {
            "train_id": self.train_id,
            "train_name": self.train_name,
            "position": self.current_position,
            "destination": self.destination,
            "speed": self.speed,
            "progress": self.progress,
            "active": self.active,
            "completed": self.completed,
        }
