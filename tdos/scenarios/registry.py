"""
Track Digital Operations Sandbox (TDOS)

registry.py

Central registry for all simulation scenarios.
"""

from __future__ import annotations

from typing import Dict, Type

from tdos.config.logging import log
from tdos.scenarios.base import BaseScenario


class ScenarioRegistry:
    """
    Registry responsible for managing all
    available TDOS scenario types.
    """

    def __init__(self) -> None:

        self._registry: Dict[str, Type[BaseScenario]] = {}

    # ==========================================================
    # Registration
    # ==========================================================

    def register(
        self,
        scenario_name: str,
        scenario_class: Type[BaseScenario],
    ) -> None:
        """
        Register a scenario implementation.
        """

        name = scenario_name.upper()

        self._registry[name] = scenario_class

        log.info(f"Scenario registered: {name}")

    # ==========================================================
    # Retrieval
    # ==========================================================

    def get(
        self,
        scenario_name: str,
    ) -> Type[BaseScenario]:
        """
        Retrieve a registered scenario class.
        """

        name = scenario_name.upper()

        if name not in self._registry:

            raise KeyError(f"Scenario '{name}' is not registered.")

        return self._registry[name]

    # ==========================================================
    # Utilities
    # ==========================================================

    def exists(
        self,
        scenario_name: str,
    ) -> bool:
        """
        Returns True if the scenario exists.
        """

        return scenario_name.upper() in self._registry

    def unregister(
        self,
        scenario_name: str,
    ) -> bool:
        """
        Remove a registered scenario.
        """

        name = scenario_name.upper()

        if name not in self._registry:
            return False

        del self._registry[name]

        log.info(f"Scenario removed: {name}")

        return True

    def clear(self) -> None:
        """
        Remove all registered scenarios.
        """

        self._registry.clear()

        log.info("Scenario registry cleared.")

    # ==========================================================
    # Statistics
    # ==========================================================

    @property
    def count(self) -> int:
        """
        Number of registered scenarios.
        """

        return len(self._registry)

    def available(self) -> list[str]:
        """
        Returns all registered scenario names.
        """

        return sorted(self._registry.keys())

    # ==========================================================
    # Factory
    # ==========================================================

    def create(
        self,
        scenario_name: str,
        *args,
        **kwargs,
    ) -> BaseScenario:
        """
        Instantiate a scenario.
        """

        scenario_class = self.get(scenario_name)

        return scenario_class(
            *args,
            **kwargs,
        )


# ==========================================================
# Global Registry
# ==========================================================

registry = ScenarioRegistry()
