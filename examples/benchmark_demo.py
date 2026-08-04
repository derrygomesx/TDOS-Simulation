"""
Track Digital Operations Sandbox (TDOS)

benchmark_demo.py

Example demonstrating AI benchmarking.
"""

from tdos.interfaces.benchmark_api import BenchmarkAPI
from tdos.models.experiment import AIExperiment


def main() -> None:

    benchmark_api = BenchmarkAPI()

    experiment = AIExperiment(
        experiment_id="EXP-001",
        experiment_name="YOLO Benchmark",
        experiment_type="Detection",
        model_name="YOLOv11",
        model_version="1.0",
        dataset_name="Railway Inspection Dataset",
        status="COMPLETED",
        accuracy=96.40,
        precision=95.20,
        recall=94.80,
        f1_score=95.00,
        latency_ms=18.50,
        throughput_fps=54.30,
        memory_mb=824.60,
    )

    benchmark = benchmark_api.run(experiment)

    summary = benchmark_api.summary(benchmark)

    print("\nBenchmark Summary\n")

    for key, value in summary.items():

        print(f"{key}: {value}")


if __name__ == "__main__":

    main()
