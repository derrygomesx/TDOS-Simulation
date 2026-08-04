"""
Track Digital Operations Sandbox (TDOS)

fleet_manager.py

Fleet management for simulation trains.
"""

from __future__ import annotations

from typing import Dict

from tdos.config.logging import log
from tdos.fleet.train import Train


class FleetManager:
    """
    Manages all trains participating in a TDOS simulation.
    """

    def __init__(self) -> None:

        self._fleet: Dict[str, Train] = {}

    # ==========================================================
    # Fleet Management
    # ==========================================================

    def add_train(
        self,
        train: Train,
    ) -> None:
        """
        Register a train.
        """

        self._fleet[train.train_id] = train

        log.info(f"Train added: {train.train_id}")

    def remove_train(
        self,
        train_id: str,
    ) -> bool:
        """
        Remove a train.
        """

        if train_id not in self._fleet:
            return False

        del self._fleet[train_id]

        log.info(f"Train removed: {train_id}")

        return True

    # ==========================================================
    # Retrieval
    # ==========================================================

    def get_train(
        self,
        train_id: str,
    ) -> Train | None:
        """
        Retrieve a train.
        """

        return self._fleet.get(train_id)

    def trains(self) -> list[Train]:
        """
        Return all registered trains.
        """

        return list(self._fleet.values())

    # ==========================================================
    # Simulation
    # ==========================================================

    def update(self) -> None:
        """
        Update every train for one simulation step.
        """

        for train in self._fleet.values():

            train.update()

    # ==========================================================
    # Statistics
    # ==========================================================

    @property
    def total_trains(self) -> int:
        """
        Number of trains.
        """

        return len(self._fleet)

    @property
    def active_trains(self) -> int:
        """
        Number of active trains.
        """

        return sum(train.active for train in self._fleet.values())

    # ==========================================================
    # Utilities
    # ==========================================================

    def clear(self) -> None:
        """
        Remove all trains.
        """

        self._fleet.clear()

        log.info("Fleet cleared.")

    # ==========================================================
    # Export
    # ==========================================================

    def summary(self) -> dict:
        """
        Fleet summary.
        """

        return {
            "total_trains": self.total_trains,
            "active_trains": self.active_trains,
            "train_ids": sorted(self._fleet.keys()),
        }
