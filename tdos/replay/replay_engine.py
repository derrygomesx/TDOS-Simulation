"""
Track Digital Operations Sandbox (TDOS)

replay_engine.py

Central replay engine responsible for recording and replaying
simulation timelines.
"""

from __future__ import annotations

from datetime import datetime

from tdos.config.logging import log
from tdos.models.asset import RailwayAsset
from tdos.replay.recorder import ReplayRecorder
from tdos.replay.timeline import ReplayTimeline


class ReplayEngine:
    """
    Coordinates simulation recording and replay.

    Responsibilities
    ----------------
    • Record simulation frames
    • Store timeline history
    • Retrieve recorded frames
    • Reset replay sessions
    """

    def __init__(self) -> None:

        self.timeline = ReplayTimeline()

        self.recorder = ReplayRecorder()

        self.started_at: datetime | None = None

        self.finished_at: datetime | None = None

    # ==========================================================
    # Recording
    # ==========================================================

    def start(self) -> None:
        """
        Starts replay recording.
        """

        self.started_at = datetime.now()

        self.timeline.clear()

        self.recorder.clear()

        log.info("Replay recording started.")

    def record(
        self,
        step: int,
        assets: list[RailwayAsset],
    ) -> None:
        """
        Record one simulation step.
        """

        frame = self.recorder.record(
            step=step,
            assets=assets,
        )

        self.timeline.add_frame(frame)

    def stop(self) -> None:
        """
        Stops replay recording.
        """

        self.finished_at = datetime.now()

        log.info("Replay recording finished.")

    # ==========================================================
    # Replay
    # ==========================================================

    def frame(
        self,
        step: int,
    ):
        """
        Retrieve a frame by simulation step.
        """

        return self.timeline.frame(step)

    def frames(self):
        """
        Return every recorded frame.
        """

        return self.timeline.frames()

    # ==========================================================
    # Statistics
    # ==========================================================

    @property
    def total_frames(self) -> int:
        """
        Number of recorded frames.
        """

        return self.timeline.count

    @property
    def duration(self) -> float:
        """
        Recording duration in seconds.
        """

        if self.started_at is None or self.finished_at is None:
            return 0.0

        return (self.finished_at - self.started_at).total_seconds()

    # ==========================================================
    # Utilities
    # ==========================================================

    def reset(self) -> None:
        """
        Clears replay data.
        """

        self.timeline.clear()

        self.recorder.clear()

        self.started_at = None

        self.finished_at = None

        log.info("Replay engine reset.")
