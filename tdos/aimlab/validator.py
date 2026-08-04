"""
Track Digital Operations Sandbox (TDOS)

validator.py

AI model validation engine.
"""

from __future__ import annotations

from dataclasses import dataclass

from tdos.config.logging import log
from tdos.models.experiment import AIExperiment

# ==========================================================
# Validation Result
# ==========================================================


@dataclass(slots=True, frozen=True)
class ValidationResult:
    """
    Result of AI model validation.
    """

    passed: bool

    score: float

    reason: str


# ==========================================================
# Validator
# ==========================================================


class AIValidator:
    """
    Validates AI model performance against
    configurable acceptance thresholds.
    """

    def __init__(
        self,
        *,
        minimum_accuracy: float = 85.0,
        minimum_precision: float = 80.0,
        minimum_recall: float = 80.0,
        minimum_f1: float = 80.0,
        maximum_latency_ms: float = 100.0,
    ) -> None:

        self.minimum_accuracy = minimum_accuracy

        self.minimum_precision = minimum_precision

        self.minimum_recall = minimum_recall

        self.minimum_f1 = minimum_f1

        self.maximum_latency_ms = maximum_latency_ms

    # ======================================================
    # Validation
    # ======================================================

    def validate(
        self,
        experiment: AIExperiment,
    ) -> ValidationResult:
        """
        Validate an AI experiment.
        """

        failures: list[str] = []

        if experiment.accuracy < self.minimum_accuracy:
            failures.append("Accuracy")

        if experiment.precision < self.minimum_precision:
            failures.append("Precision")

        if experiment.recall < self.minimum_recall:
            failures.append("Recall")

        if experiment.f1_score < self.minimum_f1:
            failures.append("F1 Score")

        if experiment.latency_ms > self.maximum_latency_ms:
            failures.append("Latency")

        score = self._validation_score(experiment)

        if failures:

            reason = "Failed: " + ", ".join(failures)

            log.warning(reason)

            return ValidationResult(
                passed=False,
                score=score,
                reason=reason,
            )

        log.info(f"Validation passed: {experiment.experiment_name}")

        return ValidationResult(
            passed=True,
            score=score,
            reason="Validation successful.",
        )

    # ======================================================
    # Internal
    # ======================================================

    @staticmethod
    def _validation_score(
        experiment: AIExperiment,
    ) -> float:
        """
        Computes an overall validation score.
        """

        score = (
            experiment.accuracy + experiment.precision + experiment.recall + experiment.f1_score
        ) / 4

        return round(score, 2)
