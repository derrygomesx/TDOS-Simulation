"""
Track Digital Operations Sandbox (TDOS)

weather.py

Weather-based simulation scenarios.
"""

from __future__ import annotations

from tdos.models.asset import RailwayAsset
from tdos.scenarios.base import BaseScenario
from tdos.scenarios.registry import registry

# ==========================================================
# Base Weather Scenario
# ==========================================================


class WeatherScenario(BaseScenario):
    """
    Base class for all weather scenarios.
    """

    health_penalty: float = 0.0

    degradation_multiplier: float = 1.0

    def apply(
        self,
        asset: RailwayAsset,
    ) -> RailwayAsset:

        severity = self.config.severity

        health_loss = self.health_penalty * severity

        degradation = asset.degradation_rate * self.degradation_multiplier

        return asset.model_copy(
            update={
                "health_score": max(
                    0.0,
                    asset.health_score - health_loss,
                ),
                "degradation_rate": degradation,
            }
        )


# ==========================================================
# Rain
# ==========================================================


class RainScenario(WeatherScenario):

    health_penalty = 0.15

    degradation_multiplier = 1.10


# ==========================================================
# Flood
# ==========================================================


class FloodScenario(WeatherScenario):

    health_penalty = 0.50

    degradation_multiplier = 1.50


# ==========================================================
# Fog
# ==========================================================


class FogScenario(WeatherScenario):

    health_penalty = 0.05

    degradation_multiplier = 1.02


# ==========================================================
# Snow
# ==========================================================


class SnowScenario(WeatherScenario):

    health_penalty = 0.25

    degradation_multiplier = 1.20


# ==========================================================
# Heat
# ==========================================================


class HeatScenario(WeatherScenario):

    health_penalty = 0.20

    degradation_multiplier = 1.15


# ==========================================================
# Dust
# ==========================================================


class DustScenario(WeatherScenario):

    health_penalty = 0.10

    degradation_multiplier = 1.05


# ==========================================================
# Registration
# ==========================================================

registry.register("RAIN", RainScenario)

registry.register("FLOOD", FloodScenario)

registry.register("FOG", FogScenario)

registry.register("SNOW", SnowScenario)

registry.register("HEAT", HeatScenario)

registry.register("DUST", DustScenario)
