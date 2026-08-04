"""
Track Digital Operations Sandbox (TDOS)

test_benchmark.py

Tests for the TDOS Benchmark Engine.
"""

from tdos.benchmark.benchmark_engine import BenchmarkEngine
from tdos.benchmark.comparator import BenchmarkComparator
from tdos.benchmark.metrics import BenchmarkMetrics
from tdos.models.experiment import AIExperiment

# ==========================================================
# Test Experiment
# ==========================================================


def create_experiment() -> AIExperiment:
    """
    Create a benchmark test experiment.
    """

    return AIExperiment(
        experiment_id="EXP-001",
        experiment_name="Benchmark Test",
        experiment_type="Detection",
        model_name="YOLOv11",
        model_version="1.0",
        dataset_name="Railway Dataset",
        status="COMPLETED",
        accuracy=96.40,
        precision=95.30,
        recall=94.80,
        f1_score=95.00,
        latency_ms=18.50,
        throughput_fps=55.20,
        memory_mb=812.40,
    )


# ==========================================================
# Benchmark Engine
# ==========================================================


def test_benchmark_engine():

    engine = BenchmarkEngine()

    benchmark = engine.run(create_experiment())

    assert benchmark.model_name == "YOLOv11"

    assert benchmark.accuracy > 0

    assert benchmark.precision > 0

    assert benchmark.recall > 0

    assert benchmark.f1_score > 0


# ==========================================================
# Benchmark Summary
# ==========================================================


def test_benchmark_summary():

    engine = BenchmarkEngine()

    benchmark = engine.run(create_experiment())

    summary = engine.summary(benchmark)

    assert summary["model"] == "YOLOv11"

    assert "accuracy" in summary

    assert "latency_ms" in summary


# ==========================================================
# Metrics
# ==========================================================


def test_metrics():

    metrics = BenchmarkMetrics()

    results = metrics.compute(create_experiment())

    assert results["accuracy"] == 96.40

    assert results["precision"] == 95.30

    assert results["overall_score"] > 0


# ==========================================================
# Grade
# ==========================================================


def test_metric_grade():

    metrics = BenchmarkMetrics()

    assert metrics.grade(97) == "A+"

    assert metrics.grade(92) == "A"

    assert metrics.grade(87) == "B"

    assert metrics.grade(78) == "C"

    assert metrics.grade(60) == "D"


# ==========================================================
# Rating
# ==========================================================


def test_metric_rating():

    metrics = BenchmarkMetrics()

    assert metrics.rating(97) == "EXCELLENT"

    assert metrics.rating(92) == "VERY GOOD"

    assert metrics.rating(85) == "GOOD"

    assert metrics.rating(72) == "ACCEPTABLE"

    assert metrics.rating(50) == "POOR"


# ==========================================================
# Comparator
# ==========================================================


def test_comparator():

    engine = BenchmarkEngine()

    comparator = BenchmarkComparator()

    left = engine.run(create_experiment())

    experiment = create_experiment().model_copy(
        update={
            "model_name": "RT-DETR",
            "accuracy": 93.50,
            "precision": 92.40,
            "recall": 91.80,
            "f1_score": 92.10,
            "latency_ms": 14.20,
        }
    )

    right = engine.run(experiment)

    comparison = comparator.compare(
        left,
        right,
    )

    assert comparison["winner"] in [
        "YOLOv11",
        "RT-DETR",
    ]


# ==========================================================
# Leaderboard
# ==========================================================


def test_leaderboard():

    engine = BenchmarkEngine()

    comparator = BenchmarkComparator()

    first = engine.run(create_experiment())

    second = engine.run(
        create_experiment().model_copy(
            update={
                "model_name": "RT-DETR",
                "accuracy": 94.10,
            }
        )
    )

    leaderboard = comparator.leaderboard(
        [
            first,
            second,
        ]
    )

    assert len(leaderboard) == 2

    assert leaderboard[0]["rank"] == 1


# ==========================================================
# Best Benchmark
# ==========================================================


def test_best_benchmark():

    engine = BenchmarkEngine()

    comparator = BenchmarkComparator()

    first = engine.run(create_experiment())

    second = engine.run(
        create_experiment().model_copy(
            update={
                "model_name": "RT-DETR",
                "accuracy": 91.0,
            }
        )
    )

    best = comparator.best(
        [
            first,
            second,
        ]
    )

    assert best is not None

    assert best.model_name == "YOLOv11"
