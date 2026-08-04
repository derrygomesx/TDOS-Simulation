"""
Track Digital Operations Sandbox (TDOS)

recorder.py

Replay frame recorder.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime

from tdos.models.asset import RailwayAsset

# ==========================================================
# Replay Frame
# ==========================================================


@dataclass(slots=True, frozen=True)
class ReplayFrame:
    """
    Immutable snapshot of the simulation at one timestep.
    """

    step: int

    timestamp: datetime

    assets: list[RailwayAsset] = field(default_factory=list)


# ==========================================================
# Replay Recorder
# ==========================================================


class ReplayRecorder:
    """
    Creates replay frames from the current simulation state.
    """

    def __init__(self) -> None:

        self._recorded_frames = 0

    # ======================================================
    # Recording
    # ======================================================

    def record(
        self,
        step: int,
        assets: list[RailwayAsset],
    ) -> ReplayFrame:
        """
        Capture a simulation frame.
        """

        frame = ReplayFrame(
            step=step,
            timestamp=datetime.now(),
            assets=deepcopy(assets),
        )

        self._recorded_frames += 1

        return frame

    # ======================================================
    # Utilities
    # ======================================================

    @property
    def frame_count(self) -> int:
        """
        Number of frames recorded.
        """

        return self._recorded_frames

    def clear(self) -> None:
        """
        Reset recorder statistics.
        """

        self._recorded_frames = 0
