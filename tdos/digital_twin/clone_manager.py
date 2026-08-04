"""
Track Digital Operations Sandbox (TDOS)

clone_manager.py

Manages all Digital Twins within the simulation.
"""

from __future__ import annotations

from typing import Dict

from tdos.config.logging import log
from tdos.digital_twin.twin import DigitalTwin
from tdos.models.asset import RailwayAsset


class CloneManager:
    """
    Central manager for all Digital Twins.

    Responsible for creating, updating, retrieving,
    synchronizing, and removing Digital Twins.
    """

    def __init__(self) -> None:

        self._twins: Dict[str, DigitalTwin] = {}

    # ==========================================================
    # Twin Management
    # ==========================================================

    def create_twin(
        self,
        asset: RailwayAsset,
    ) -> DigitalTwin:
        """
        Creates a Digital Twin for an asset.
        """

        twin = DigitalTwin(asset)

        self._twins[asset.asset_id] = twin

        log.info(f"Digital Twin created: {asset.asset_id}")

        return twin

    def create_twins(
        self,
        assets: list[RailwayAsset],
    ) -> None:
        """
        Creates Digital Twins for multiple assets.
        """

        for asset in assets:
            self.create_twin(asset)

    # ==========================================================
    # Retrieval
    # ==========================================================

    def get(
        self,
        asset_id: str,
    ) -> DigitalTwin | None:
        """
        Retrieves a Digital Twin.
        """

        return self._twins.get(asset_id)

    def all(self) -> list[DigitalTwin]:
        """
        Returns all Digital Twins.
        """

        return list(self._twins.values())

    # ==========================================================
    # Updates
    # ==========================================================

    def update(
        self,
        asset: RailwayAsset,
    ) -> None:
        """
        Updates an existing Digital Twin.
        """

        twin = self.get(asset.asset_id)

        if twin is None:

            twin = self.create_twin(asset)

        else:

            twin.update(asset)

    def synchronize(
        self,
        assets: list[RailwayAsset],
    ) -> None:
        """
        Synchronizes all Digital Twins with the latest
        asset states.
        """

        for asset in assets:
            self.update(asset)

    # ==========================================================
    # Removal
    # ==========================================================

    def remove(
        self,
        asset_id: str,
    ) -> bool:
        """
        Removes a Digital Twin.
        """

        if asset_id not in self._twins:
            return False

        del self._twins[asset_id]

        log.info(f"Digital Twin removed: {asset_id}")

        return True

    def clear(self) -> None:
        """
        Removes every Digital Twin.
        """

        self._twins.clear()

        log.info("All Digital Twins cleared.")

    # ==========================================================
    # Statistics
    # ==========================================================

    @property
    def count(self) -> int:
        """
        Number of Digital Twins.
        """

        return len(self._twins)

    @property
    def empty(self) -> bool:
        """
        Returns True if no Digital Twins exist.
        """

        return len(self._twins) == 0

    # ==========================================================
    # Export
    # ==========================================================

    def summary(self) -> dict:
        """
        Returns Clone Manager statistics.
        """

        return {
            "digital_twins": self.count,
            "asset_ids": sorted(self._twins.keys()),
        }
