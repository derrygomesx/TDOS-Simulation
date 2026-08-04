"""
Track Digital Operations Sandbox (TDOS)

benchmark_engine.py

Central benchmark engine.
"""

from __future__ import annotations

from datetime import datetime

from tdos.benchmark.metrics import BenchmarkMetrics
from tdos.benchmark.report import BenchmarkReport
from tdos.config.logging import log
from tdos.models.experiment import AIExperiment
from tdos.models.results import BenchmarkResult


class BenchmarkEngine:
    """
    Executes standardized AI benchmarks.
    """

    def __init__(self) -> None:

        self.metrics = BenchmarkMetrics()

        self.report = BenchmarkReport()

    # ==========================================================
    # Benchmark
    # ==========================================================

    def run(
        self,
        experiment: AIExperiment,
    ) -> BenchmarkResult:
        """
        Execute benchmark for an AI experiment.
        """

        log.info(f"Running benchmark: {experiment.experiment_name}")

        metrics = self.metrics.compute(experiment)

        benchmark = BenchmarkResult(
            model_name=experiment.model_name,
            accuracy=metrics["accuracy"],
            precision=metrics["precision"],
            recall=metrics["recall"],
            f1_score=metrics["f1_score"],
            latency_ms=metrics["latency_ms"],
            throughput_fps=metrics["throughput_fps"],
        )

        self.report.generate(
            benchmark=benchmark,
            experiment=experiment,
            generated_at=datetime.now(),
        )

        log.info("Benchmark completed.")

        return benchmark

    # ==========================================================
    # Utilities
    # ==========================================================

    def summary(
        self,
        benchmark: BenchmarkResult,
    ) -> dict:
        """
        Returns a compact benchmark summary.
        """

        return {
            "model": benchmark.model_name,
            "accuracy": benchmark.accuracy,
            "precision": benchmark.precision,
            "recall": benchmark.recall,
            "f1_score": benchmark.f1_score,
            "latency_ms": benchmark.latency_ms,
            "throughput_fps": benchmark.throughput_fps,
        }
