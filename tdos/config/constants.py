"""
Track Digital Operations Sandbox (TDOS)

constants.py

Global constants used throughout the TDOS Simulation Engine.
"""

from __future__ import annotations

# ==========================================================
# Engine
# ==========================================================

ENGINE_NAME = "Track Digital Operations Sandbox"
ENGINE_VERSION = "1.0.0"
DEFAULT_RANDOM_SEED = 42

DEFAULT_SIMULATION_FPS = 30
DEFAULT_REPLAY_FPS = 30
DEFAULT_TIMESTEP = 1.0

# ==========================================================
# Simulation States
# ==========================================================

STATE_IDLE = "IDLE"
STATE_INITIALIZING = "INITIALIZING"
STATE_RUNNING = "RUNNING"
STATE_PAUSED = "PAUSED"
STATE_REPLAYING = "REPLAYING"
STATE_COMPLETED = "COMPLETED"
STATE_CANCELLED = "CANCELLED"
STATE_FAILED = "FAILED"

SIMULATION_STATES = (
    STATE_IDLE,
    STATE_INITIALIZING,
    STATE_RUNNING,
    STATE_PAUSED,
    STATE_REPLAYING,
    STATE_COMPLETED,
    STATE_CANCELLED,
    STATE_FAILED,
)

# ==========================================================
# Events
# ==========================================================

EVENT_START = "START"
EVENT_STOP = "STOP"
EVENT_PAUSE = "PAUSE"
EVENT_RESUME = "RESUME"
EVENT_SCENARIO = "SCENARIO"
EVENT_ASSET_UPDATE = "ASSET_UPDATE"
EVENT_HEALTH_UPDATE = "HEALTH_UPDATE"
EVENT_PREDICTION = "PREDICTION"
EVENT_REPLAY = "REPLAY"
EVENT_BENCHMARK = "BENCHMARK"
EVENT_ERROR = "ERROR"

# ==========================================================
# Asset Types
# ==========================================================

ASSET_RAIL = "RAIL"
ASSET_SLEEPER = "SLEEPER"
ASSET_FASTENER = "FASTENER"
ASSET_BALLAST = "BALLAST"
ASSET_TURNOUT = "TURNOUT"
ASSET_BRIDGE = "BRIDGE"
ASSET_SIGNAL = "SIGNAL"

ASSET_TYPES = (
    ASSET_RAIL,
    ASSET_SLEEPER,
    ASSET_FASTENER,
    ASSET_BALLAST,
    ASSET_TURNOUT,
    ASSET_BRIDGE,
    ASSET_SIGNAL,
)

# ==========================================================
# Scenario Categories
# ==========================================================

SCENARIO_WEATHER = "WEATHER"
SCENARIO_INFRASTRUCTURE = "INFRASTRUCTURE"
SCENARIO_SENSOR = "SENSOR"
SCENARIO_OPERATION = "OPERATION"

# ==========================================================
# Weather
# ==========================================================

RAIN = "RAIN"
FLOOD = "FLOOD"
FOG = "FOG"
SNOW = "SNOW"
HEAT = "HEAT"
DUST = "DUST"

# ==========================================================
# Infrastructure
# ==========================================================

CRACK_GROWTH = "CRACK_GROWTH"
BALLAST_FAILURE = "BALLAST_FAILURE"
SLEEPER_DAMAGE = "SLEEPER_DAMAGE"
FASTENER_FAILURE = "FASTENER_FAILURE"
TURNOUT_FAILURE = "TURNOUT_FAILURE"
RAIL_MISALIGNMENT = "RAIL_MISALIGNMENT"
BRIDGE_DEFORMATION = "BRIDGE_DEFORMATION"

# ==========================================================
# Sensors
# ==========================================================

GPS_FAILURE = "GPS_FAILURE"
GPS_DRIFT = "GPS_DRIFT"
CAMERA_FAILURE = "CAMERA_FAILURE"
IR_FAILURE = "IR_FAILURE"
ULTRASONIC_FAILURE = "ULTRASONIC_FAILURE"
SENSOR_NOISE = "SENSOR_NOISE"
PACKET_LOSS = "PACKET_LOSS"

# ==========================================================
# Operations
# ==========================================================

MAINTENANCE_DELAY = "MAINTENANCE_DELAY"
INSPECTION_SKIP = "INSPECTION_SKIP"
TRAIN_OVERLOAD = "TRAIN_OVERLOAD"
TRAFFIC_INCREASE = "TRAFFIC_INCREASE"

# ==========================================================
# Health
# ==========================================================

GRADE_A = "A"
GRADE_B = "B"
GRADE_C = "C"
GRADE_D = "D"
GRADE_F = "F"

HEALTH_GRADES = (
    GRADE_A,
    GRADE_B,
    GRADE_C,
    GRADE_D,
    GRADE_F,
)

# ==========================================================
# Risk
# ==========================================================

RISK_LOW = "LOW"
RISK_MEDIUM = "MEDIUM"
RISK_HIGH = "HIGH"
RISK_CRITICAL = "CRITICAL"

RISK_LEVELS = (
    RISK_LOW,
    RISK_MEDIUM,
    RISK_HIGH,
    RISK_CRITICAL,
)

# ==========================================================
# Maintenance
# ==========================================================

PRIORITY_LOW = "LOW"
PRIORITY_MEDIUM = "MEDIUM"
PRIORITY_HIGH = "HIGH"
PRIORITY_IMMEDIATE = "IMMEDIATE"

# ==========================================================
# Replay
# ==========================================================

REPLAY_REALTIME = "REALTIME"
REPLAY_FAST = "FAST"
REPLAY_STEP = "STEP"
REPLAY_CUSTOM = "CUSTOM"

# ==========================================================
# Prediction
# ==========================================================

MODEL_LINEAR = "LINEAR"
MODEL_EXPONENTIAL = "EXPONENTIAL"
MODEL_AI = "AI"

# ==========================================================
# AI Lab
# ==========================================================

TRAINING = "TRAINING"
VALIDATION = "VALIDATION"
TESTING = "TESTING"
DEPLOYMENT = "DEPLOYMENT"

# ==========================================================
# Benchmark
# ==========================================================

PRECISION = "PRECISION"
RECALL = "RECALL"
F1_SCORE = "F1_SCORE"
MAP = "MAP"
LATENCY = "LATENCY"
THROUGHPUT = "THROUGHPUT"
MEMORY = "MEMORY"
CPU = "CPU"
GPU = "GPU"

# ==========================================================
# Limits
# ==========================================================

MAX_HEALTH_SCORE = 100.0
MIN_HEALTH_SCORE = 0.0

MAX_CONFIDENCE = 1.0
MIN_CONFIDENCE = 0.0

# ==========================================================
# Exit Codes
# ==========================================================

SUCCESS = 0
ERROR = 1
