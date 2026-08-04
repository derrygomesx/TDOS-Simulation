"""
Track Digital Operations Sandbox (TDOS)

benchmark_api.py

Public API for the TDOS Benchmark Engine.
"""

from __future__ import annotations

from tdos.benchmark.benchmark_engine import BenchmarkEngine
from tdos.benchmark.comparator import BenchmarkComparator
from tdos.models.experiment import AIExperiment
from tdos.models.results import BenchmarkResult


class BenchmarkAPI:
    """
    Public interface for the TDOS Benchmark Engine.
    """

    def __init__(self) -> None:

        self.engine = BenchmarkEngine()

        self.comparator = BenchmarkComparator()

    # ==========================================================
    # Benchmark
    # ==========================================================

    def run(
        self,
        experiment: AIExperiment,
    ) -> BenchmarkResult:
        """
        Execute a benchmark.
        """

        return self.engine.run(experiment)

    # ==========================================================
    # Summary
    # ==========================================================

    def summary(
        self,
        benchmark: BenchmarkResult,
    ) -> dict:
        """
        Return benchmark summary.
        """

        return self.engine.summary(benchmark)

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

        return self.comparator.compare(
            left,
            right,
        )

    def leaderboard(
        self,
        benchmarks: list[BenchmarkResult],
    ) -> list[dict]:
        """
        Generate benchmark leaderboard.
        """

        return self.comparator.leaderboard(benchmarks)

    def best(
        self,
        benchmarks: list[BenchmarkResult],
    ) -> BenchmarkResult | None:
        """
        Return best benchmark.
        """

        return self.comparator.best(benchmarks)
