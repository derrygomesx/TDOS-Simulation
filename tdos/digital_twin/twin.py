"""
Track Digital Operations Sandbox (TDOS)

twin.py

Digital Twin implementation for railway assets.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime

from tdos.models.asset import RailwayAsset


class DigitalTwin:
    """
    Live virtual representation of a railway asset.

    The Digital Twin mirrors the current simulated state of an
    asset and maintains its evolution throughout the simulation.
    """

    def __init__(self, asset: RailwayAsset):

        self.asset_id = asset.asset_id

        self.asset_type = asset.asset_type

        self._initial_state = deepcopy(asset)

        self._current_state = deepcopy(asset)

        self._history: list[RailwayAsset] = []

        self.created_at = datetime.now()

        self.updated_at = self.created_at

    # ======================================================
    # State
    # ======================================================

    @property
    def current(self) -> RailwayAsset:
        """
        Returns the latest asset state.
        """

        return self._current_state

    @property
    def initial(self) -> RailwayAsset:
        """
        Returns the original asset state.
        """

        return self._initial_state

    @property
    def history(self) -> list[RailwayAsset]:
        """
        Returns the state history.
        """

        return list(self._history)

    # ======================================================
    # Update
    # ======================================================

    def update(
        self,
        asset: RailwayAsset,
    ) -> None:
        """
        Updates the Digital Twin with a new asset state.
        """

        self._history.append(deepcopy(self._current_state))

        self._current_state = deepcopy(asset)

        self.updated_at = datetime.now()

    # ======================================================
    # Restore
    # ======================================================

    def restore_initial(self) -> None:
        """
        Restores the twin to its original state.
        """

        self._current_state = deepcopy(self._initial_state)

        self._history.clear()

        self.updated_at = datetime.now()

    # ======================================================
    # Statistics
    # ======================================================

    @property
    def history_length(self) -> int:
        """
        Number of stored historical states.
        """

        return len(self._history)

    @property
    def age_seconds(self) -> float:
        """
        Age of the Digital Twin.
        """

        return (datetime.now() - self.created_at).total_seconds()

    # ======================================================
    # Export
    # ======================================================

    def summary(self) -> dict:
        """
        Returns a compact summary.
        """

        return {
            "asset_id": self.asset_id,
            "asset_type": self.asset_type,
            "health_score": self.current.health_score,
            "history": self.history_length,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
