"""
Track Digital Operations Sandbox (TDOS)

report.py

Benchmark report generator.
"""

from __future__ import annotations

from datetime import datetime

from tdos.models.experiment import AIExperiment
from tdos.models.results import BenchmarkResult


class BenchmarkReport:
    """
    Generates benchmark reports for AI experiments.
    """

    # ==========================================================
    # Report Generation
    # ==========================================================

    def generate(
        self,
        *,
        benchmark: BenchmarkResult,
        experiment: AIExperiment,
        generated_at: datetime,
    ) -> dict:
        """
        Generate a structured benchmark report.
        """

        report = {
            "generated_at": generated_at.isoformat(),
            "experiment": {
                "id": experiment.experiment_id,
                "name": experiment.experiment_name,
                "type": experiment.experiment_type,
                "status": experiment.status,
                "model": experiment.model_name,
                "model_version": experiment.model_version,
                "dataset": experiment.dataset_name,
            },
            "benchmark": {
                "accuracy": benchmark.accuracy,
                "precision": benchmark.precision,
                "recall": benchmark.recall,
                "f1_score": benchmark.f1_score,
                "latency_ms": benchmark.latency_ms,
                "throughput_fps": benchmark.throughput_fps,
            },
            "summary": self._summary(benchmark),
        }

        return report

    # ==========================================================
    # Summary
    # ==========================================================

    @staticmethod
    def _summary(
        benchmark: BenchmarkResult,
    ) -> str:
        """
        Generate a concise benchmark summary.
        """

        return (
            f"Model '{benchmark.model_name}' "
            f"achieved "
            f"{benchmark.accuracy:.2f}% accuracy, "
            f"{benchmark.precision:.2f}% precision, "
            f"{benchmark.recall:.2f}% recall, "
            f"{benchmark.f1_score:.2f}% F1 score, "
            f"with {benchmark.latency_ms:.2f} ms latency "
            f"and {benchmark.throughput_fps:.2f} FPS throughput."
        )
