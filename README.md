# TDOS — Step 3 RAMS Intelligence

This update adds a complete RAMS (Reliability, Availability, Maintainability & Safety) layer on top of the existing TDOS simulation/replay system.

## Files to replace/add

### Add
- `tdos/rams/__init__.py`
- `tdos/rams/models.py`
- `tdos/rams/rams_engine.py`
- `tests/test_rams.py`

### Replace
- `tdos/core/engine.py`
- `backend/services/simulation_service.py`
- `backend/routes/simulation.py`
- `src/App.tsx`
- `src/styles.css`

## API

After a simulation is completed:

`GET /simulations/{simulation_id}/rams`

Returns:
- Fleet RAMS score and grade
- Reliability score
- Availability score
- Maintainability score
- Safety score
- Critical asset count
- Maintenance priority counts
- Per-asset RAMS analysis

## RAMS basis

Weights:
- Reliability: 30%
- Availability: 25%
- Maintainability: 20%
- Safety: 25%

Availability is calculated from actual replay snapshots.
Reliability uses TDOS predicted failure probability.
Safety combines predicted failure risk, health degradation and asset-type criticality.
Maintainability is explicitly a maintenance-readiness proxy because the current TDOS model does not simulate repair duration/MTTR or work-order execution.

## Validation performed

- `tests/test_rams.py`: 2 passed
- `backend/tests/test_simulation_api.py`: 1 passed
- App.tsx TypeScript/TSX syntax transpilation: 0 diagnostics
- RAMS API smoke test: HTTP 200 with live simulation data

## Frontend

The update adds a new `RAMS` navigation tab with:
- Fleet RAMS score
- R/A/M/S breakdown
- Critical assets
- Maintenance queue
- Fleet availability
- Asset ranking
- Engineering methodology panel
