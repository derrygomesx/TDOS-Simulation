"""
Track Digital Operations Sandbox (TDOS)

sensors.py

Sensor-related simulation scenarios.
"""

from __future__ import annotations

from tdos.models.asset import RailwayAsset
from tdos.scenarios.base import BaseScenario
from tdos.scenarios.registry import registry

# ==========================================================
# Base Sensor Scenario
# ==========================================================


class SensorScenario(BaseScenario):
    """
    Base class for sensor-related failures.
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
# GPS Failure
# ==========================================================


class GPSFailureScenario(SensorScenario):

    health_penalty = 0.05

    degradation_increase = 0.01


# ==========================================================
# GPS Drift
# ==========================================================


class GPSDriftScenario(SensorScenario):

    health_penalty = 0.03

    degradation_increase = 0.01


# ==========================================================
# Camera Failure
# ==========================================================


class CameraFailureScenario(SensorScenario):

    health_penalty = 0.08

    degradation_increase = 0.02


# ==========================================================
# IR Failure
# ==========================================================


class IRFailureScenario(SensorScenario):

    health_penalty = 0.06

    degradation_increase = 0.02


# ==========================================================
# Ultrasonic Failure
# ==========================================================


class UltrasonicFailureScenario(SensorScenario):

    health_penalty = 0.10

    degradation_increase = 0.03


# ==========================================================
# Sensor Noise
# ==========================================================


class SensorNoiseScenario(SensorScenario):

    health_penalty = 0.04

    degradation_increase = 0.01


# ==========================================================
# Packet Loss
# ==========================================================


class PacketLossScenario(SensorScenario):

    health_penalty = 0.02

    degradation_increase = 0.01


# ==========================================================
# Registration
# ==========================================================

registry.register(
    "GPS_FAILURE",
    GPSFailureScenario,
)

registry.register(
    "GPS_DRIFT",
    GPSDriftScenario,
)

registry.register(
    "CAMERA_FAILURE",
    CameraFailureScenario,
)

registry.register(
    "IR_FAILURE",
    IRFailureScenario,
)

registry.register(
    "ULTRASONIC_FAILURE",
    UltrasonicFailureScenario,
)

registry.register(
    "SENSOR_NOISE",
    SensorNoiseScenario,
)

registry.register(
    "PACKET_LOSS",
    PacketLossScenario,
)
