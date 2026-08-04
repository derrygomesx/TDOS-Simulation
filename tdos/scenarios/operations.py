"""
Track Digital Operations Sandbox (TDOS)

operations.py

Operational simulation scenarios.
"""

from __future__ import annotations

from tdos.models.asset import RailwayAsset
from tdos.scenarios.base import BaseScenario
from tdos.scenarios.registry import registry

# ==========================================================
# Base Operational Scenario
# ==========================================================


class OperationalScenario(BaseScenario):
    """
    Base class for operational scenarios.
    """

    health_penalty: float = 0.0

    degradation_multiplier: float = 1.0

    def apply(
        self,
        asset: RailwayAsset,
    ) -> RailwayAsset:

        severity = self.config.severity

        health_loss = self.health_penalty * severity

        new_health = max(
            0.0,
            asset.health_score - health_loss,
        )

        new_degradation = asset.degradation_rate * self.degradation_multiplier

        return asset.model_copy(
            update={
                "health_score": new_health,
                "degradation_rate": new_degradation,
            }
        )


# ==========================================================
# Maintenance Delay
# ==========================================================


class MaintenanceDelayScenario(OperationalScenario):

    health_penalty = 0.20

    degradation_multiplier = 1.25


# ==========================================================
# Inspection Skip
# ==========================================================


class InspectionSkipScenario(OperationalScenario):

    health_penalty = 0.10

    degradation_multiplier = 1.10


# ==========================================================
# Train Overload
# ==========================================================


class TrainOverloadScenario(OperationalScenario):

    health_penalty = 0.35

    degradation_multiplier = 1.40


# ==========================================================
# Traffic Increase
# ==========================================================


class TrafficIncreaseScenario(OperationalScenario):

    health_penalty = 0.15

    degradation_multiplier = 1.15


# ==========================================================
# Registration
# ==========================================================

registry.register(
    "MAINTENANCE_DELAY",
    MaintenanceDelayScenario,
)

registry.register(
    "INSPECTION_SKIP",
    InspectionSkipScenario,
)

registry.register(
    "TRAIN_OVERLOAD",
    TrainOverloadScenario,
)

registry.register(
    "TRAFFIC_INCREASE",
    TrafficIncreaseScenario,
)
