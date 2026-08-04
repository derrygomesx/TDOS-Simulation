"""
Track Digital Operations Sandbox (TDOS)

helpers.py

General helper utilities used throughout TDOS.
"""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4


class Helpers:
    """
    Collection of reusable helper methods.
    """

    # ==========================================================
    # Time
    # ==========================================================

    @staticmethod
    def now() -> datetime:
        """
        Returns the current UTC datetime.
        """

        return datetime.now()

    @staticmethod
    def timestamp() -> str:
        """
        Returns an ISO-8601 timestamp.
        """

        return datetime.now().isoformat()

    # ==========================================================
    # UUID
    # ==========================================================

    @staticmethod
    def uuid() -> str:
        """
        Generate a UUID string.
        """

        return str(uuid4())

    # ==========================================================
    # Numeric Helpers
    # ==========================================================

    @staticmethod
    def clamp(
        value: float,
        minimum: float,
        maximum: float,
    ) -> float:
        """
        Clamp a value between a minimum and maximum.
        """

        return max(
            minimum,
            min(value, maximum),
        )

    @staticmethod
    def percentage(
        value: float,
        total: float,
    ) -> float:
        """
        Calculate a percentage.
        """

        if total == 0:
            return 0.0

        return round(
            (value / total) * 100,
            2,
        )

    # ==========================================================
    # Dictionary Helpers
    # ==========================================================

    @staticmethod
    def merge(
        left: dict,
        right: dict,
    ) -> dict:
        """
        Merge two dictionaries.
        """

        return {
            **left,
            **right,
        }

    # ==========================================================
    # Serialization
    # ==========================================================

    @staticmethod
    def serialize(
        obj,
    ):
        """
        Convert supported objects into dictionaries.
        """

        if hasattr(obj, "model_dump"):

            return obj.model_dump()

        if hasattr(obj, "__dict__"):

            return vars(obj)

        return obj

    # ==========================================================
    # Formatting
    # ==========================================================

    @staticmethod
    def round2(
        value: float,
    ) -> float:
        """
        Round to two decimal places.
        """

        return round(value, 2)

    @staticmethod
    def round3(
        value: float,
    ) -> float:
        """
        Round to three decimal places.
        """

        return round(value, 3)

    # ==========================================================
    # Collections
    # ==========================================================

    @staticmethod
    def unique(
        values: list,
    ) -> list:
        """
        Remove duplicate values while preserving order.
        """

        return list(dict.fromkeys(values))

    @staticmethod
    def chunk(
        values: list,
        size: int,
    ) -> list[list]:
        """
        Split a list into chunks.
        """

        return [
            values[i : i + size]
            for i in range(
                0,
                len(values),
                size,
            )
        ]
