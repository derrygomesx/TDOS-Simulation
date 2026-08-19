# Track Digital Operations Sandbox (TDOS)

## System Architecture

---

## Overview

Track Digital Operations Sandbox (TDOS) is a modular simulation platform designed for developing, validating, benchmarking, and evaluating railway inspection systems.

The platform enables developers to simulate railway infrastructure degradation, execute inspection scenarios, evaluate AI models, replay simulation timelines, and benchmark prediction algorithms within a controlled virtual environment.

TDOS is designed as a standalone simulation engine that can be integrated into TrackGuard AI or any other railway asset management platform.

---

# High-Level Architecture

```text
                    +----------------------+
                    |     Frontend UI      |
                    +----------+-----------+
                               |
                               |
                    +----------v-----------+
                    |      FastAPI API     |
                    +----------+-----------+
                               |
          ---------------------------------------------
          |            TDOS Interfaces                |
          ---------------------------------------------
                               |
     --------------------------------------------------------
     |            Simulation Engine (Core)                 |
     --------------------------------------------------------
       |        |         |         |          |          |
       |        |         |         |          |          |
 Digital   Scenario   Prediction   Replay    Fleet    AI Lab
  Twin      Engine      Engine     Engine   Manager
       \        |         |          |         /
        \       |         |          |        /
         -------------------------------------
                    Benchmark Engine
```

---

# Project Structure

```text
TDOS

├── config/
├── models/
├── core/
├── digital_twin/
├── scenarios/
├── prediction/
├── replay/
├── fleet/
├── aimlab/
├── benchmark/
├── interfaces/
└── utils/
```

---

# Core Components

## Configuration

Responsible for runtime configuration.

Includes:

- Settings
- Constants
- Logging

---

## Models

Defines every shared data model used throughout TDOS.

Examples include:

- Railway Assets
- Simulation Configurations
- AI Experiments
- Benchmark Results

---

## Core Engine

Acts as the execution controller.

Responsibilities:

- Simulation lifecycle
- Event scheduling
- State management
- Simulation timing
- Event dispatch

---

## Digital Twin

Maintains virtual representations of railway assets.

Capabilities include:

- Asset cloning
- Health tracking
- Degradation simulation
- Twin synchronization

---

## Scenario Engine

Injects events into simulations.

Supported scenario categories include:

- Weather
- Infrastructure failures
- Sensor failures
- Operational events

---

## Prediction Engine

Forecasts future asset conditions.

Modules include:

- Health prediction
- Risk prediction
- Remaining Useful Life (RUL)

---

## Replay Engine

Records every simulation step.

Provides:

- Timeline playback
- Frame retrieval
- Historical replay

---

## Fleet Simulation

Simulates multiple inspection trains.

Responsibilities:

- Fleet management
- Railway network representation
- Train movement

---

## AI Laboratory

Provides a controlled environment for AI development.

Capabilities include:

- Training
- Validation
- Evaluation
- Model Registry
- Deployment Certification

---

## Benchmark Engine

Measures AI performance.

Evaluates:

- Accuracy
- Precision
- Recall
- F1 Score
- Latency
- Throughput

Supports comparison between multiple AI models.

---

## Interfaces

Public APIs exposing TDOS functionality.

Available APIs include:

- Simulation API
- Prediction API
- Replay API
- Benchmark API

---

## Utilities

Shared helper functionality.

Includes:

- Logging
- Validation
- Helper utilities

---

# Execution Flow

```text
Simulation Configuration
            │
            ▼
Simulation Engine
            │
            ▼
Scenario Injection
            │
            ▼
Digital Twin Update
            │
            ▼
Prediction Engine
            │
            ▼
Replay Recording
            │
            ▼
Benchmark Evaluation
            │
            ▼
Simulation Results
```

---

# Design Principles

TDOS follows several software engineering principles:

- Modular architecture
- Separation of responsibilities
- Interface-driven design
- Reusable components
- Extensible subsystem architecture
- Independent simulation modules
- Clean public APIs

---

# Repository Organization

```text
TDOS-Simulation

.github/
docs/
examples/
tests/
tdos/

README.md
requirements.txt
pyproject.toml
```

---

# Future Extensions

The architecture has been designed to support future additions, including:

- Multi-user simulations
- Distributed execution
- Reinforcement Learning environments
- Digital Twin synchronization
- Real-time railway telemetry
- Cloud deployment
- GPU acceleration
- Advanced visualization

---

# Version

Current Version:

**TDOS v1.0**