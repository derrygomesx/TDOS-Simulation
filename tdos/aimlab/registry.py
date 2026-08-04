"""
Track Digital Operations Sandbox (TDOS)

registry.py

AI model registry.
"""

from __future__ import annotations

from typing import Dict

from tdos.models.experiment import AIExperiment


class ModelRegistry:
    """
    Registry for AI experiments and trained models.
    """

    def __init__(self) -> None:

        self._models: Dict[str, AIExperiment] = {}

    # ==========================================================
    # Registration
    # ==========================================================

    def register(
        self,
        experiment: AIExperiment,
    ) -> None:
        """
        Register a trained AI model.
        """

        self._models[experiment.model_name] = experiment

    # ==========================================================
    # Retrieval
    # ==========================================================

    def get(
        self,
        model_name: str,
    ) -> AIExperiment | None:
        """
        Retrieve a registered model.
        """

        return self._models.get(model_name)

    def models(
        self,
    ) -> list[AIExperiment]:
        """
        Return all registered models.
        """

        return list(self._models.values())

    # ==========================================================
    # Removal
    # ==========================================================

    def remove(
        self,
        model_name: str,
    ) -> bool:
        """
        Remove a registered model.
        """

        if model_name not in self._models:
            return False

        del self._models[model_name]

        return True

    # ==========================================================
    # Utilities
    # ==========================================================

    def clear(self) -> None:
        """
        Clear registry.
        """

        self._models.clear()

    @property
    def count(self) -> int:
        """
        Number of registered models.
        """

        return len(self._models)

    def summary(self) -> dict:
        """
        Registry summary.
        """

        return {
            "registered_models": self.count,
            "models": sorted(self._models.keys()),
        }
