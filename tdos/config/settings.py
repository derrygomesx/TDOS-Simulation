"""
Track Digital Operations Sandbox (TDOS)

settings.py

Central runtime configuration for the TDOS Simulation Engine.
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class TDOSSettings(BaseSettings):
    """
    Global runtime configuration for the TDOS Simulation Engine.

    Values can be overridden using environment variables
    with the TDOS_ prefix.
    """

    # ==========================================================
    # Engine
    # ==========================================================

    engine_name: str = "Track Digital Operations Sandbox"

    engine_version: str = "1.0.0"

    debug_mode: bool = False

    simulation_fps: int = 30

    simulation_speed: float = 1.0

    max_simulation_steps: int = 10000

    random_seed: int = 42

    # ==========================================================
    # Digital Twin
    # ==========================================================

    enable_digital_twin: bool = True

    enable_asset_history: bool = True

    snapshot_interval: int = 10

    # ==========================================================
    # Prediction
    # ==========================================================

    enable_prediction: bool = True

    prediction_horizon: int = 365

    default_confidence: float = 0.95

    # ==========================================================
    # Replay
    # ==========================================================

    enable_recording: bool = True

    replay_fps: int = 30

    max_replay_frames: int = 5000

    # ==========================================================
    # Fleet Simulation
    # ==========================================================

    enable_fleet_simulation: bool = True

    maximum_trains: int = 500

    maximum_assets: int = 100000

    # ==========================================================
    # AI Laboratory
    # ==========================================================

    enable_ai_lab: bool = True

    benchmark_iterations: int = 10

    stress_test_iterations: int = 100

    # ==========================================================
    # Logging
    # ==========================================================

    log_level: str = "INFO"

    enable_console_logging: bool = True

    enable_file_logging: bool = False

    log_file: str = "tdos.log"

    # ==========================================================
    # Performance
    # ==========================================================

    enable_parallel_processing: bool = True

    worker_threads: int = 4

    batch_size: int = 100

    # ==========================================================
    # Storage
    # ==========================================================

    data_directory: str = "tdos/data"

    scenario_directory: str = "tdos/data/scenarios"

    dataset_directory: str = "tdos/data/datasets"

    export_directory: str = "tdos/data/exports"

    # ==========================================================
    # Validation
    # ==========================================================

    strict_validation: bool = True

    allow_unknown_scenarios: bool = False

    # ==========================================================
    # Environment
    # ==========================================================

    model_config = SettingsConfigDict(env_prefix="TDOS_", env_file=".env", extra="ignore")


settings = TDOSSettings()
