# Track Digital Operations Sandbox (TDOS)

# API Contract

---

## Overview

TDOS exposes a collection of public Python interfaces that provide controlled access to the simulation platform.

External applications should interact only with these interfaces rather than importing internal engine components directly.

Current public APIs:

- SimulationAPI
- PredictionAPI
- ReplayAPI
- BenchmarkAPI

---

# Architecture

```text
Frontend
      │
      ▼
Backend (FastAPI)
      │
      ▼
TDOS Interfaces
      │
      ▼
TDOS Core Modules
```

---

# SimulationAPI

Module:

```text
tdos.interfaces.simulation_api
```

Purpose:

Manage the complete lifecycle of a simulation.

---

### Methods

#### create(config)

Creates a new simulation.

Input:

```python
SimulationConfig
```

Output:

```python
None
```

---

#### start()

Starts simulation execution.

---

#### pause()

Temporarily pauses execution.

---

#### resume()

Resumes execution.

---

#### stop()

Stops the simulation.

---

#### step()

Executes one simulation step.

---

#### run()

Runs the simulation until completion.

---

#### status()

Returns the current simulation state.

Output:

```python
dict
```

Example:

```python
{
    "running": True,
    "paused": False,
    "current_step": 42,
    "completed": False
}
```

---

#### results()

Returns the completed simulation results.

---

#### reset()

Resets the engine.

---

# PredictionAPI

Module:

```text
tdos.interfaces.prediction_api
```

Purpose:

Predict future railway asset conditions.

---

### Methods

#### predict(asset)

Returns complete prediction results.

Input:

```python
RailwayAsset
```

Output:

```python
PredictionResult
```

---

#### predict_health(asset)

Returns predicted health score.

Output:

```python
float
```

---

#### predict_risk(asset)

Returns failure probability.

Output:

```python
float
```

---

#### predict_rul(asset)

Returns Remaining Useful Life.

Output:

```python
int
```

---

#### summary(asset)

Returns prediction summary.

Output:

```python
dict
```

---

# ReplayAPI

Module:

```text
tdos.interfaces.replay_api
```

Purpose:

Manage replay recording and playback.

---

### Methods

#### start()

Starts replay recording.

---

#### record(step, assets)

Stores one replay frame.

Inputs:

```python
step: int

assets: list[RailwayAsset]
```

---

#### stop()

Stops replay recording.

---

#### frame(step)

Returns one replay frame.

---

#### frames()

Returns all replay frames.

---

#### summary()

Returns replay statistics.

---

#### reset()

Clears replay session.

---

# BenchmarkAPI

Module:

```text
tdos.interfaces.benchmark_api
```

Purpose:

Evaluate AI model performance.

---

### Methods

#### run(experiment)

Runs a benchmark.

Input:

```python
AIExperiment
```

Output:

```python
BenchmarkResult
```

---

#### summary(benchmark)

Returns benchmark summary.

---

#### compare(left, right)

Compares two benchmark results.

---

#### leaderboard(results)

Ranks benchmark results.

---

#### best(results)

Returns the highest-ranked benchmark.

---

# Integration Workflow

Typical execution flow:

```text
Create Simulation
        │
        ▼
Run Simulation
        │
        ▼
Generate Predictions
        │
        ▼
Record Replay
        │
        ▼
Run Benchmark
        │
        ▼
Return Results
```

---

# Design Rules

External applications should:

- Use only the interfaces package.
- Avoid importing internal engine modules.
- Treat model objects as immutable after submission.
- Handle exceptions returned by the interfaces.
- Avoid modifying internal TDOS state directly.

---

# Version

Current Contract:

**TDOS API v1.0**