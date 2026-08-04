"""
Track Digital Operations Sandbox (TDOS)

infrastructure.py

Infrastructure-related simulation scenarios.
"""

from __future__ import annotations

from tdos.models.asset import RailwayAsset
from tdos.scenarios.base import BaseScenario
from tdos.scenarios.registry import registry

# ==========================================================
# Base Infrastructure Scenario
# ==========================================================


class InfrastructureScenario(BaseScenario):
    """
    Base class for infrastructure failure scenarios.
    """

    health_penalty: float = 0.0

    degradation_increase: float = 0.0

    def apply(
        self,
        asset: RailwayAsset,
    ) -> RailwayAsset:

        severity = self.config.severity

        new_health = max(0.0, asset.health_score - (self.health_penalty * severity))

        new_degradation = asset.degradation_rate + (self.degradation_increase * severity)

        return asset.model_copy(
            update={
                "health_score": new_health,
                "degradation_rate": new_degradation,
            }
        )


# ==========================================================
# Crack Growth
# ==========================================================


class CrackGrowthScenario(InfrastructureScenario):

    health_penalty = 0.40

    degradation_increase = 0.08


# ==========================================================
# Ballast Failure
# ==========================================================


class BallastFailureScenario(InfrastructureScenario):

    health_penalty = 0.30

    degradation_increase = 0.05


# ==========================================================
# Sleeper Damage
# ==========================================================


class SleeperDamageScenario(InfrastructureScenario):

    health_penalty = 0.35

    degradation_increase = 0.06


# ==========================================================
# Fastener Failure
# ==========================================================


class FastenerFailureScenario(InfrastructureScenario):

    health_penalty = 0.25

    degradation_increase = 0.04


# ==========================================================
# Turnout Failure
# ==========================================================


class TurnoutFailureScenario(InfrastructureScenario):

    health_penalty = 0.45

    degradation_increase = 0.09


# ==========================================================
# Rail Misalignment
# ==========================================================


class RailMisalignmentScenario(InfrastructureScenario):

    health_penalty = 0.38

    degradation_increase = 0.07


# ==========================================================
# Bridge Deformation
# ==========================================================


class BridgeDeformationScenario(InfrastructureScenario):

    health_penalty = 0.50

    degradation_increase = 0.10


# ==========================================================
# Registration
# ==========================================================

registry.register(
    "CRACK_GROWTH",
    CrackGrowthScenario,
)

registry.register(
    "BALLAST_FAILURE",
    BallastFailureScenario,
)

registry.register(
    "SLEEPER_DAMAGE",
    SleeperDamageScenario,
)

registry.register(
    "FASTENER_FAILURE",
    FastenerFailureScenario,
)

registry.register(
    "TURNOUT_FAILURE",
    TurnoutFailureScenario,
)

registry.register(
    "RAIL_MISALIGNMENT",
    RailMisalignmentScenario,
)

registry.register(
    "BRIDGE_DEFORMATION",
    BridgeDeformationScenario,
)
