"""
Track Digital Operations Sandbox (TDOS)

base.py

Base class for all simulation scenarios.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from tdos.config.logging import log
from tdos.models.asset import RailwayAsset
from tdos.models.scenario import SimulationScenario


class BaseScenario(ABC):
    """
    Abstract base class for all TDOS scenarios.

    Every scenario implementation must inherit from this class.
    """

    def __init__(
        self,
        config: SimulationScenario,
    ) -> None:

        self.config = config

        self.active = False

    # ==========================================================
    # Lifecycle
    # ==========================================================

    def start(self) -> None:
        """
        Starts the scenario.
        """

        self.active = True

        log.info(f"Scenario started: {self.config.name}")

    def stop(self) -> None:
        """
        Stops the scenario.
        """

        self.active = False

        log.info(f"Scenario stopped: {self.config.name}")

    # ==========================================================
    # Execution
    # ==========================================================

    @abstractmethod
    def apply(
        self,
        asset: RailwayAsset,
    ) -> RailwayAsset:
        """
        Applies the scenario to an asset.

        Must return a NEW RailwayAsset.
        """

        raise NotImplementedError

    # ==========================================================
    # Utilities
    # ==========================================================

    def should_execute(
        self,
        current_step: int,
    ) -> bool:
        """
        Determines whether the scenario should execute
        during the current simulation step.
        """

        if not self.config.enabled:
            return False

        if current_step < self.config.start_step:
            return False

        if current_step > self.config.end_step:
            return False

        return True

    def affects(
        self,
        asset: RailwayAsset,
    ) -> bool:
        """
        Determines whether the scenario affects
        the given asset.
        """

        if self.config.target_asset is None:
            return True

        return asset.asset_id == self.config.target_asset

    # ==========================================================
    # Metadata
    # ==========================================================

    @property
    def name(self) -> str:
        """
        Scenario name.
        """

        return self.config.name

    @property
    def category(self) -> str:
        """
        Scenario category.
        """

        return self.config.category

    @property
    def severity(self) -> float:
        """
        Scenario severity.
        """

        return self.config.severity

    # ==========================================================
    # Export
    # ==========================================================

    def summary(self) -> dict:
        """
        Returns a compact scenario summary.
        """

        return {
            "name": self.config.name,
            "category": self.config.category,
            "severity": self.config.severity,
            "enabled": self.config.enabled,
            "active": self.active,
        }
