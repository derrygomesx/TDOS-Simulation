"""
Track Digital Operations Sandbox (TDOS)

evaluator.py

AI model evaluation engine.
"""

from __future__ import annotations

from dataclasses import dataclass

from tdos.config.logging import log
from tdos.aimlab.validator import ValidationResult
from tdos.models.experiment import AIExperiment

# ==========================================================
# Evaluation Result
# ==========================================================


@dataclass(slots=True, frozen=True)
class EvaluationResult:
    """
    Final evaluation of an AI model.
    """

    overall_score: float

    deployment_level: str

    recommendation: str

    passed: bool


# ==========================================================
# Evaluator
# ==========================================================


class AIEvaluator:
    """
    Produces the final AI evaluation after validation.
    """

    # ======================================================
    # Evaluation
    # ======================================================

    def evaluate(
        self,
        experiment: AIExperiment,
        validation: ValidationResult,
    ) -> EvaluationResult:
        """
        Evaluate an AI experiment.
        """

        score = self._overall_score(experiment)

        level = self._deployment_level(
            score,
            validation.passed,
        )

        recommendation = self._recommendation(level)

        log.info(f"Evaluation completed: " f"{experiment.experiment_name}")

        return EvaluationResult(
            overall_score=score,
            deployment_level=level,
            recommendation=recommendation,
            passed=validation.passed,
        )

    # ======================================================
    # Internal
    # ======================================================

    @staticmethod
    def _overall_score(
        experiment: AIExperiment,
    ) -> float:
        """
        Computes the overall AI score.
        """

        score = (
            (experiment.accuracy * 0.35)
            + (experiment.precision * 0.20)
            + (experiment.recall * 0.20)
            + (experiment.f1_score * 0.20)
            + (max(0.0, 100 - experiment.latency_ms) * 0.05)
        )

        return round(score, 2)

    @staticmethod
    def _deployment_level(
        score: float,
        passed: bool,
    ) -> str:
        """
        Determines deployment readiness.
        """

        if not passed:
            return "REJECTED"

        if score >= 95:
            return "PRODUCTION"

        if score >= 90:
            return "PILOT"

        if score >= 80:
            return "SIMULATION"

        return "RESEARCH"

    @staticmethod
    def _recommendation(
        level: str,
    ) -> str:
        """
        Generates deployment recommendation.
        """

        recommendations = {
            "PRODUCTION": "Approved for production deployment.",
            "PILOT": "Recommended for pilot deployment.",
            "SIMULATION": "Suitable for simulation and validation.",
            "RESEARCH": "Requires additional model improvements.",
            "REJECTED": "Model failed validation and should not be deployed.",
        }

        return recommendations[level]
