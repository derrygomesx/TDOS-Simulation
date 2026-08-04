"""
Track Digital Operations Sandbox (TDOS)

replay_api.py

Public API for the TDOS Replay Engine.
"""

from __future__ import annotations

from tdos.models.asset import RailwayAsset
from tdos.replay.replay_engine import ReplayEngine


class ReplayAPI:
    """
    Public interface for the TDOS Replay Engine.
    """

    def __init__(self) -> None:

        self.engine = ReplayEngine()

    # ==========================================================
    # Recording
    # ==========================================================

    def start(self) -> None:
        """
        Start replay recording.
        """

        self.engine.start()

    def record(
        self,
        step: int,
        assets: list[RailwayAsset],
    ) -> None:
        """
        Record one simulation step.
        """

        self.engine.record(
            step=step,
            assets=assets,
        )

    def stop(self) -> None:
        """
        Stop replay recording.
        """

        self.engine.stop()

    # ==========================================================
    # Replay
    # ==========================================================

    def frame(
        self,
        step: int,
    ):
        """
        Retrieve a replay frame.
        """

        return self.engine.frame(step)

    def frames(self):
        """
        Retrieve all replay frames.
        """

        return self.engine.frames()

    # ==========================================================
    # Statistics
    # ==========================================================

    def summary(self) -> dict:
        """
        Replay session summary.
        """

        return {
            "total_frames": self.engine.total_frames,
            "duration_seconds": round(
                self.engine.duration,
                2,
            ),
        }

    # ==========================================================
    # Utilities
    # ==========================================================

    def reset(self) -> None:
        """
        Reset replay session.
        """

        self.engine.reset()
