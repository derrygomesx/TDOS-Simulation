"""
Track Digital Operations Sandbox (TDOS)

metrics.py

Benchmark metric computation.
"""

from __future__ import annotations

from tdos.models.experiment import AIExperiment


class BenchmarkMetrics:
    """
    Computes standardized benchmark metrics
    from an AI experiment.
    """

    # ==========================================================
    # Computation
    # ==========================================================

    def compute(
        self,
        experiment: AIExperiment,
    ) -> dict:
        """
        Compute benchmark metrics.
        """

        score = self.overall_score(experiment)

        return {
            "accuracy": experiment.accuracy,
            "precision": experiment.precision,
            "recall": experiment.recall,
            "f1_score": experiment.f1_score,
            "latency_ms": experiment.latency_ms,
            "throughput_fps": experiment.throughput_fps,
            "memory_mb": experiment.memory_mb,
            "overall_score": score,
        }

    # ==========================================================
    # Overall Score
    # ==========================================================

    @staticmethod
    def overall_score(
        experiment: AIExperiment,
    ) -> float:
        """
        Compute overall benchmark score.
        """

        score = (
            experiment.accuracy * 0.35
            + experiment.precision * 0.20
            + experiment.recall * 0.20
            + experiment.f1_score * 0.20
            + max(0.0, 100 - experiment.latency_ms) * 0.05
        )

        return round(score, 2)

    # ==========================================================
    # Performance Grade
    # ==========================================================

    @staticmethod
    def grade(
        score: float,
    ) -> str:
        """
        Convert benchmark score into a grade.
        """

        if score >= 95:
            return "A+"

        if score >= 90:
            return "A"

        if score >= 85:
            return "B"

        if score >= 75:
            return "C"

        return "D"

    # ==========================================================
    # Rating
    # ==========================================================

    @staticmethod
    def rating(
        score: float,
    ) -> str:
        """
        Human-readable benchmark rating.
        """

        if score >= 95:
            return "EXCELLENT"

        if score >= 90:
            return "VERY GOOD"

        if score >= 80:
            return "GOOD"

        if score >= 70:
            return "ACCEPTABLE"

        return "POOR"
