"""
Track Digital Operations Sandbox (TDOS)

certification.py

AI deployment certification.
"""

from __future__ import annotations

from dataclasses import dataclass

from tdos.aimlab.evaluator import EvaluationResult


@dataclass(slots=True, frozen=True)
class CertificationResult:
    """
    AI certification result.
    """

    certified: bool

    certification_level: str

    remarks: str


class CertificationEngine:
    """
    Certifies AI models for deployment.
    """

    def certify(
        self,
        evaluation: EvaluationResult,
    ) -> CertificationResult:
        """
        Generate deployment certification.
        """

        if not evaluation.passed:

            return CertificationResult(
                certified=False,
                certification_level="NONE",
                remarks="Validation failed.",
            )

        level = evaluation.deployment_level

        remarks = {
            "PRODUCTION": "Approved for production deployment.",
            "PILOT": "Approved for pilot deployment.",
            "SIMULATION": "Approved for simulation use only.",
            "RESEARCH": "Research use only.",
        }.get(
            level,
            "Certification unavailable.",
        )

        return CertificationResult(
            certified=True,
            certification_level=level,
            remarks=remarks,
        )
