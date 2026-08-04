"""
Track Digital Operations Sandbox (TDOS)

timeline.py

Replay timeline storage.
"""

from __future__ import annotations

from typing import Dict, List

from tdos.replay.recorder import ReplayFrame


class ReplayTimeline:
    """
    Stores replay frames generated during a simulation.

    Provides fast random access and ordered playback.
    """

    def __init__(self) -> None:

        self._frames: Dict[int, ReplayFrame] = {}

    # ======================================================
    # Storage
    # ======================================================

    def add_frame(
        self,
        frame: ReplayFrame,
    ) -> None:
        """
        Store a replay frame.
        """

        self._frames[frame.step] = frame

    # ======================================================
    # Retrieval
    # ======================================================

    def frame(
        self,
        step: int,
    ) -> ReplayFrame | None:
        """
        Retrieve a frame by simulation step.
        """

        return self._frames.get(step)

    def frames(self) -> List[ReplayFrame]:
        """
        Return every replay frame in chronological order.
        """

        return [self._frames[step] for step in sorted(self._frames)]

    def range(
        self,
        start: int,
        end: int,
    ) -> List[ReplayFrame]:
        """
        Return frames within a step range.
        """

        return [self._frames[step] for step in sorted(self._frames) if start <= step <= end]

    # ======================================================
    # Navigation
    # ======================================================

    def first(self) -> ReplayFrame | None:
        """
        Return the first recorded frame.
        """

        if not self._frames:
            return None

        return self._frames[min(self._frames)]

    def last(self) -> ReplayFrame | None:
        """
        Return the final recorded frame.
        """

        if not self._frames:
            return None

        return self._frames[max(self._frames)]

    # ======================================================
    # Utilities
    # ======================================================

    def clear(self) -> None:
        """
        Remove all replay frames.
        """

        self._frames.clear()

    @property
    def count(self) -> int:
        """
        Number of stored replay frames.
        """

        return len(self._frames)

    @property
    def empty(self) -> bool:
        """
        Returns True if no replay frames exist.
        """

        return len(self._frames) == 0

    # ======================================================
    # Export
    # ======================================================

    def summary(self) -> dict:
        """
        Returns replay timeline statistics.
        """

        return {
            "frames": self.count,
            "first_step": min(self._frames) if self._frames else None,
            "last_step": max(self._frames) if self._frames else None,
        }
