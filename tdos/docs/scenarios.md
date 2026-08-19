# Track Digital Operations Sandbox (TDOS)

# Simulation Scenarios

---

# Overview

TDOS provides configurable simulation scenarios that reproduce realistic railway operating conditions. These scenarios allow developers to evaluate inspection algorithms, prediction models, digital twins, and AI systems under controlled environments.

Scenarios are grouped into four categories:

- Weather
- Infrastructure
- Sensors
- Operations

Multiple scenarios can be combined within a single simulation to create complex testing environments.

---

# Scenario Architecture

```text
Simulation Engine
        │
        ▼
Scenario Manager
        │
        ├──────── Weather
        ├──────── Infrastructure
        ├──────── Sensors
        └──────── Operations
```

---

# Weather Scenarios

Weather scenarios simulate environmental conditions that influence railway infrastructure and sensor performance.

---

## Rain

Purpose

- Wet rail surfaces
- Reduced visibility
- Increased corrosion rate

Expected Effects

- Faster infrastructure degradation
- Lower camera confidence
- Reduced traction conditions

---

## Fog

Purpose

Simulates low-visibility conditions.

Expected Effects

- Reduced camera detection accuracy
- Increased perception uncertainty
- Lower inspection confidence

---

## Heat

Purpose

Simulates high ambient temperatures.

Expected Effects

- Rail thermal expansion
- Increased deformation probability
- Accelerated material aging

---

## Snow

Purpose

Simulates cold-weather operations.

Expected Effects

- Reduced sensor reliability
- Ice accumulation
- Lower operational efficiency

---

## Flood

Purpose

Simulates water accumulation around railway infrastructure.

Expected Effects

- Ballast instability
- Drainage failure
- Infrastructure degradation

---

## Dust

Purpose

Simulates dusty operating environments.

Expected Effects

- Camera contamination
- Sensor obstruction
- Reduced image quality

---

# Infrastructure Scenarios

Infrastructure scenarios simulate failures within railway assets.

---

## Crack Growth

Simulates progressive rail crack propagation.

Effects

- Health reduction
- Increased failure probability
- Reduced Remaining Useful Life

---

## Ballast Failure

Simulates ballast deterioration.

Effects

- Reduced track stability
- Increased vibration
- Lower geometry quality

---

## Sleeper Damage

Simulates damaged or degraded sleepers.

Effects

- Alignment degradation
- Structural instability

---

## Fastener Failure

Simulates broken or loose fasteners.

Effects

- Reduced track integrity
- Higher maintenance priority

---

## Rail Misalignment

Simulates lateral or vertical alignment errors.

Effects

- Increased operational risk
- Reduced health score

---

# Sensor Scenarios

Sensor scenarios introduce failures into inspection equipment.

---

## GPS Drift

Effects

- Position errors
- Route deviation
- Localization uncertainty

---

## GPS Failure

Effects

- Complete GPS outage
- Position unavailable

---

## Camera Failure

Effects

- Vision inspection unavailable

---

## IR Failure

Effects

- Thermal inspection unavailable

---

## Ultrasonic Failure

Effects

- Internal crack detection unavailable

---

## Sensor Noise

Effects

- Increased measurement uncertainty
- Reduced confidence

---

## Packet Loss

Effects

- Missing telemetry
- Incomplete replay timeline
- Reduced synchronization accuracy

---

# Operational Scenarios

Operational scenarios affect railway operations rather than infrastructure.

---

## Train Overload

Effects

- Accelerated degradation
- Increased stress on assets

---

## Maintenance Delay

Effects

- Deferred repairs
- Lower health over time

---

## Inspection Skip

Effects

- Missing inspection cycles
- Reduced monitoring confidence

---

## Traffic Increase

Effects

- Higher asset utilization
- Increased wear
- Reduced Remaining Useful Life

---

# Combining Scenarios

TDOS supports simultaneous execution of multiple scenarios.

Example:

```text
Rain
      +
Fog
      +
GPS Drift
      +
Crack Growth
```

This combination produces a challenging inspection environment suitable for testing AI robustness.

---

# Scenario Lifecycle

```text
Simulation Start
        │
        ▼
Load Scenario
        │
        ▼
Initialize Parameters
        │
        ▼
Apply Effects
        │
        ▼
Update Digital Twin
        │
        ▼
Generate Predictions
        │
        ▼
Record Replay
        │
        ▼
Benchmark Results
```

---

# Design Principles

Every scenario should:

- Be deterministic when seeded
- Be independently executable
- Support parameter customization
- Integrate with the Digital Twin
- Update Prediction Engine inputs
- Be compatible with Replay Engine recording

---

# Future Scenario Extensions

Planned scenario categories include:

- Landslides
- Bridge failures
- Tunnel degradation
- Switch and crossing failures
- Power supply interruptions
- Communication failures
- Multi-train traffic conflicts
- Earthquake simulations
- Cybersecurity attack scenarios

---

# Version

Current Scenario Library:

**TDOS Scenarios v1.0**