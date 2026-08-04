"""
Track Digital Operations Sandbox (TDOS)

railway_network.py

Railway network model.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# ==========================================================
# Track Segment
# ==========================================================


@dataclass(slots=True)
class TrackSegment:
    """
    Represents one railway track segment.
    """

    segment_id: str

    start_km: float

    end_km: float

    bidirectional: bool = True

    active: bool = True

    @property
    def length(self) -> float:
        """
        Length of the track segment.
        """

        return abs(self.end_km - self.start_km)


# ==========================================================
# Railway Network
# ==========================================================


class RailwayNetwork:
    """
    Represents the railway infrastructure used during
    simulation.
    """

    def __init__(self) -> None:

        self._segments: dict[str, TrackSegment] = {}

    # ======================================================
    # Segment Management
    # ======================================================

    def add_segment(
        self,
        segment: TrackSegment,
    ) -> None:
        """
        Add a track segment.
        """

        self._segments[segment.segment_id] = segment

    def remove_segment(
        self,
        segment_id: str,
    ) -> bool:
        """
        Remove a track segment.
        """

        if segment_id not in self._segments:
            return False

        del self._segments[segment_id]

        return True

    # ======================================================
    # Retrieval
    # ======================================================

    def get_segment(
        self,
        segment_id: str,
    ) -> TrackSegment | None:
        """
        Retrieve a track segment.
        """

        return self._segments.get(segment_id)

    def segments(self) -> list[TrackSegment]:
        """
        Return every track segment.
        """

        return list(self._segments.values())

    # ======================================================
    # Network Statistics
    # ======================================================

    @property
    def total_segments(self) -> int:
        """
        Number of track segments.
        """

        return len(self._segments)

    @property
    def total_length(self) -> float:
        """
        Total railway length.
        """

        return sum(segment.length for segment in self._segments.values())

    # ======================================================
    # Validation
    # ======================================================

    def contains(
        self,
        kilometer: float,
    ) -> bool:
        """
        Returns True if the kilometer position
        exists in the network.
        """

        return any(
            segment.start_km <= kilometer <= segment.end_km for segment in self._segments.values()
        )

    # ======================================================
    # Utilities
    # ======================================================

    def clear(self) -> None:
        """
        Remove every track segment.
        """

        self._segments.clear()

    # ======================================================
    # Export
    # ======================================================

    def summary(self) -> dict:
        """
        Returns network statistics.
        """

        return {
            "segments": self.total_segments,
            "total_length_km": round(
                self.total_length,
                2,
            ),
        }
