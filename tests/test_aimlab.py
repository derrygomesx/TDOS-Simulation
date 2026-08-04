"""
Track Digital Operations Sandbox (TDOS)

test_aimlab.py

Tests for the TDOS AI Laboratory.
"""

from tdos.aimlab.evaluator import AIEvaluator
from tdos.aimlab.trainer import AITrainer
from tdos.aimlab.validator import AIValidator
from tdos.models.experiment import AIExperiment

# ==========================================================
# Test Experiment
# ==========================================================


def create_experiment() -> AIExperiment:
    """
    Create a sample AI experiment.
    """

    return AIExperiment(
        experiment_id="EXP-001",
        experiment_name="YOLO Validation",
        experiment_type="Detection",
        model_name="YOLOv11",
        model_version="1.0",
        dataset_name="Railway Dataset",
        status="PENDING",
        accuracy=0.0,
        precision=0.0,
        recall=0.0,
        f1_score=0.0,
        latency_ms=0.0,
        throughput_fps=0.0,
        memory_mb=0.0,
    )


# ==========================================================
# Trainer
# ==========================================================


def test_training_start():

    trainer = AITrainer()

    experiment = trainer.start(create_experiment())

    assert trainer.running is True

    assert experiment.status == "RUNNING"


def test_training_finish():

    trainer = AITrainer()

    trainer.start(create_experiment())

    experiment = trainer.finish(
        accuracy=96.5,
        precision=95.4,
        recall=94.9,
        f1_score=95.1,
        latency_ms=18.2,
        throughput_fps=55.6,
        memory_mb=812.0,
    )

    assert experiment.status == "COMPLETED"

    assert experiment.accuracy == 96.5


def test_training_failure():

    trainer = AITrainer()

    trainer.start(create_experiment())

    experiment = trainer.fail("Dataset missing")

    assert experiment.status == "FAILED"

    assert experiment.notes == "Dataset missing"


def test_trainer_reset():

    trainer = AITrainer()

    trainer.start(create_experiment())

    trainer.reset()

    assert trainer.active is None

    assert trainer.running is False


# ==========================================================
# Validator
# ==========================================================


def test_validator_pass():

    trainer = AITrainer()

    trainer.start(create_experiment())

    experiment = trainer.finish(
        accuracy=96,
        precision=95,
        recall=94,
        f1_score=95,
        latency_ms=20,
        throughput_fps=50,
        memory_mb=750,
    )

    validator = AIValidator()

    result = validator.validate(experiment)

    assert result.passed is True


def test_validator_fail():

    trainer = AITrainer()

    trainer.start(create_experiment())

    experiment = trainer.finish(
        accuracy=40,
        precision=35,
        recall=30,
        f1_score=32,
        latency_ms=250,
        throughput_fps=10,
        memory_mb=900,
    )

    validator = AIValidator()

    result = validator.validate(experiment)

    assert result.passed is False


# ==========================================================
# Evaluator
# ==========================================================


def test_evaluator():

    trainer = AITrainer()

    trainer.start(create_experiment())

    experiment = trainer.finish(
        accuracy=95,
        precision=94,
        recall=94,
        f1_score=94,
        latency_ms=18,
        throughput_fps=60,
        memory_mb=720,
    )

    validator = AIValidator()

    validation = validator.validate(experiment)

    evaluator = AIEvaluator()

    evaluation = evaluator.evaluate(
        experiment,
        validation,
    )

    assert evaluation.passed is True

    assert evaluation.overall_score > 0

    assert evaluation.deployment_level in [
        "PRODUCTION",
        "PILOT",
        "SIMULATION",
        "RESEARCH",
        "REJECTED",
    ]


# ==========================================================
# Deployment Levels
# ==========================================================


def test_deployment_levels():

    evaluator = AIEvaluator()

    assert (
        evaluator._deployment_level(
            97,
            True,
        )
        == "PRODUCTION"
    )

    assert (
        evaluator._deployment_level(
            92,
            True,
        )
        == "PILOT"
    )

    assert (
        evaluator._deployment_level(
            84,
            True,
        )
        == "SIMULATION"
    )

    assert (
        evaluator._deployment_level(
            72,
            True,
        )
        == "RESEARCH"
    )

    assert (
        evaluator._deployment_level(
            99,
            False,
        )
        == "REJECTED"
    )
