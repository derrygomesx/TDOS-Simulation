"""
Track Digital Operations Sandbox (TDOS)

trainer.py

AI model training manager.
"""

from __future__ import annotations

from datetime import datetime

from tdos.config.logging import log
from tdos.models.experiment import AIExperiment


class AITrainer:
    """
    Coordinates AI model training inside TDOS.

    Responsibilities
    ----------------
    • Start training sessions
    • Track experiment status
    • Store training metrics
    """

    def __init__(self) -> None:

        self._active_experiment: AIExperiment | None = None

    # ==========================================================
    # Training
    # ==========================================================

    def start(
        self,
        experiment: AIExperiment,
    ) -> AIExperiment:
        """
        Starts an AI training experiment.
        """

        experiment = experiment.model_copy(
            update={
                "status": "RUNNING",
                "started_at": datetime.now(),
            }
        )

        self._active_experiment = experiment

        log.info(f"Training started: {experiment.experiment_name}")

        return experiment

    def finish(
        self,
        *,
        accuracy: float,
        precision: float,
        recall: float,
        f1_score: float,
        latency_ms: float,
        throughput_fps: float,
        memory_mb: float,
    ) -> AIExperiment:
        """
        Completes the active experiment.
        """

        if self._active_experiment is None:

            raise RuntimeError("No active experiment.")

        started = self._active_experiment.started_at

        duration = 0.0

        if started is not None:

            duration = (datetime.now() - started).total_seconds()

        experiment = self._active_experiment.model_copy(
            update={
                "status": "COMPLETED",
                "completed_at": datetime.now(),
                "duration_seconds": duration,
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1_score": f1_score,
                "latency_ms": latency_ms,
                "throughput_fps": throughput_fps,
                "memory_mb": memory_mb,
            }
        )

        self._active_experiment = experiment

        log.info(f"Training completed: {experiment.experiment_name}")

        return experiment

    # ==========================================================
    # Failure
    # ==========================================================

    def fail(
        self,
        reason: str,
    ) -> AIExperiment:
        """
        Marks the experiment as failed.
        """

        if self._active_experiment is None:

            raise RuntimeError("No active experiment.")

        experiment = self._active_experiment.model_copy(
            update={
                "status": "FAILED",
                "notes": reason,
                "completed_at": datetime.now(),
            }
        )

        self._active_experiment = experiment

        log.error(f"Training failed: {reason}")

        return experiment

    # ==========================================================
    # Utilities
    # ==========================================================

    @property
    def active(self) -> AIExperiment | None:
        """
        Returns the currently active experiment.
        """

        return self._active_experiment

    @property
    def running(self) -> bool:
        """
        Returns True if training is active.
        """

        return self._active_experiment is not None and self._active_experiment.status == "RUNNING"

    def reset(self) -> None:
        """
        Clears the active experiment.
        """

        self._active_experiment = None

        log.info("AI Trainer reset.")
