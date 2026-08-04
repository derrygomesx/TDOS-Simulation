"""
Track Digital Operations Sandbox (TDOS)

validators.py

Common validation utilities.
"""

from __future__ import annotations

import re


class Validator:
    """
    Collection of reusable validation methods.
    """

    # ==========================================================
    # Numeric Validation
    # ==========================================================

    @staticmethod
    def score(
        value: float,
        *,
        minimum: float = 0.0,
        maximum: float = 100.0,
    ) -> bool:
        """
        Validate a score.
        """

        return minimum <= value <= maximum

    @staticmethod
    def probability(
        value: float,
    ) -> bool:
        """
        Validate a probability.
        """

        return 0.0 <= value <= 1.0

    @staticmethod
    def positive(
        value: float,
    ) -> bool:
        """
        Validate positive values.
        """

        return value >= 0.0

    @staticmethod
    def percentage(
        value: float,
    ) -> bool:
        """
        Validate percentages.
        """

        return 0.0 <= value <= 100.0

    # ==========================================================
    # String Validation
    # ==========================================================

    @staticmethod
    def not_empty(
        value: str,
    ) -> bool:
        """
        Validate non-empty strings.
        """

        return bool(value and value.strip())

    @staticmethod
    def identifier(
        value: str,
    ) -> bool:
        """
        Validate identifiers.

        Example:
            AST-001
            TR-004
            EXP-2026-001
        """

        pattern = r"^[A-Za-z0-9_-]+$"

        return bool(
            re.fullmatch(
                pattern,
                value,
            )
        )

    # ==========================================================
    # Collections
    # ==========================================================

    @staticmethod
    def non_empty_list(
        values: list,
    ) -> bool:
        """
        Validate non-empty list.
        """

        return len(values) > 0

    # ==========================================================
    # Railway Assets
    # ==========================================================

    @classmethod
    def asset_health(
        cls,
        health: float,
    ) -> bool:
        """
        Validate railway asset health.
        """

        return cls.score(health)

    @classmethod
    def degradation_rate(
        cls,
        rate: float,
    ) -> bool:
        """
        Validate degradation rate.
        """

        return cls.positive(rate)

    # ==========================================================
    # Simulation
    # ==========================================================

    @staticmethod
    def simulation_step(
        step: int,
    ) -> bool:
        """
        Validate simulation step.
        """

        return step >= 0

    @staticmethod
    def duration(
        seconds: float,
    ) -> bool:
        """
        Validate duration.
        """

        return seconds >= 0

    # ==========================================================
    # Benchmark
    # ==========================================================

    @classmethod
    def latency(
        cls,
        latency_ms: float,
    ) -> bool:
        """
        Validate inference latency.
        """

        return cls.positive(latency_ms)

    @classmethod
    def throughput(
        cls,
        fps: float,
    ) -> bool:
        """
        Validate throughput.
        """

        return cls.positive(fps)

    # ==========================================================
    # AI
    # ==========================================================

    @classmethod
    def accuracy(
        cls,
        accuracy: float,
    ) -> bool:
        """
        Validate model accuracy.
        """

        return cls.score(accuracy)

    @classmethod
    def confidence(
        cls,
        confidence: float,
    ) -> bool:
        """
        Validate confidence score.
        """

        return cls.probability(confidence)
