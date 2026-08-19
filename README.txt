TDOS Scenario Comparison Fix

Replace:
  backend/routes/simulation.py
  frontend/src/App.tsx

The backend route exposes:
  POST /simulations/{simulation_id}/maintenance-what-if/batch

The frontend now uses the backend comparison as the source of truth and no longer silently falls back to local projections.

After replacing files:
  1. Restart FastAPI.
  2. Restart Vite.
  3. Run the simulation to completion.
  4. Open Decisions / What-If.
  5. Add scenarios.
  6. Click Compare scenarios.
