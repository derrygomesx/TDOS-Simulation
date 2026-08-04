"""
Track Digital Operations Sandbox (TDOS)

comparator.py

Benchmark comparison utilities.
"""

from __future__ import annotations

from tdos.benchmark.metrics import BenchmarkMetrics
from tdos.models.results import BenchmarkResult


class BenchmarkComparator:
    """
    Compares benchmark results from multiple AI models.
    """

    def __init__(self) -> None:

        self.metrics = BenchmarkMetrics()

    # ==========================================================
    # Ranking
    # ==========================================================

    def rank(
        self,
        benchmarks: list[BenchmarkResult],
    ) -> list[BenchmarkResult]:
        """
        Rank benchmark results by performance.
        """

        return sorted(
            benchmarks,
            key=self.score,
            reverse=True,
        )

    # ==========================================================
    # Best Model
    # ==========================================================

    def best(
        self,
        benchmarks: list[BenchmarkResult],
    ) -> BenchmarkResult | None:
        """
        Return the highest-ranked benchmark.
        """

        if not benchmarks:
            return None

        return self.rank(benchmarks)[0]

    # ==========================================================
    # Score
    # ==========================================================

    def score(
        self,
        benchmark: BenchmarkResult,
    ) -> float:
        """
        Compute an overall benchmark score.
        """

        score = (
            benchmark.accuracy * 0.35
            + benchmark.precision * 0.20
            + benchmark.recall * 0.20
            + benchmark.f1_score * 0.20
            + max(0.0, 100 - benchmark.latency_ms) * 0.05
        )

        return round(score, 2)

    # ==========================================================
    # Comparison
    # ==========================================================

    def compare(
        self,
        left: BenchmarkResult,
        right: BenchmarkResult,
    ) -> dict:
        """
        Compare two benchmark results.
        """

        left_score = self.score(left)

        right_score = self.score(right)

        winner = left.model_name if left_score >= right_score else right.model_name

        return {
            "winner": winner,
            "left_score": left_score,
            "right_score": right_score,
            "score_difference": round(
                abs(left_score - right_score),
                2,
            ),
            "left_model": left.model_name,
            "right_model": right.model_name,
        }

    # ==========================================================
    # Leaderboard
    # ==========================================================

    def leaderboard(
        self,
        benchmarks: list[BenchmarkResult],
    ) -> list[dict]:
        """
        Generate a benchmark leaderboard.
        """

        ranked = self.rank(benchmarks)

        board = []

        for position, benchmark in enumerate(
            ranked,
            start=1,
        ):

            board.append(
                {
                    "rank": position,
                    "model": benchmark.model_name,
                    "score": self.score(benchmark),
                    "accuracy": benchmark.accuracy,
                    "latency_ms": benchmark.latency_ms,
                }
            )

        return board
