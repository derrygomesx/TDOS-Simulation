"""
Track Digital Operations Sandbox (TDOS)

simulation_service.py

Application service bridging the FastAPI backend and the TDOS engine.
"""

from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor
from threading import RLock

from database.models import SimulationModel
from schemas.simulation import SimulationCreateRequest
from tdos.core.engine import SimulationEngine
from tdos.decision_support import DecisionSupportEngine


class SimulationService:
    """
    Owns application-level TDOS simulation sessions.

    Each API-created simulation receives its own SimulationEngine instance.
    Long-running simulations execute in a worker thread so the API remains
    responsive and lifecycle endpoints can inspect or request a pause/stop.
    """

    # The API creates a fresh SimulationService for each request. Keep
    # simulation runtime state at class level so a simulation created by
    # POST /simulations can be found by later lifecycle requests such as
    # GET /simulations/{id}, POST /start, /run, /pause, etc.
    _lock = RLock()
    _engines: dict[str, SimulationEngine] = {}
    _futures: dict[str, Future] = {}
    _executor = ThreadPoolExecutor(
        max_workers=4,
        thread_name_prefix="tdos-simulation",
    )

    def __init__(self, session) -> None:
        # Database sessions remain request-scoped. Runtime simulation state
        # is shared above, while DB updates use the current request's session.
        self._session = session

    # ==========================================================
    # CREATE
    # ==========================================================

    def create(self, request: SimulationCreateRequest) -> dict:
        engine = SimulationEngine()

        simulation = engine.create_session(
            name=request.name,
            assets=request.assets,
            scenarios=request.scenarios,
            total_steps=request.total_steps,
        )

        with self._lock:
            self._engines[simulation.simulation_id] = engine

        record = SimulationModel(
            id=simulation.simulation_id,
            experiment_id=request.experiment_id,
            scenario_name=", ".join(
                scenario.name for scenario in request.scenarios
            ) or "BASELINE",
            status=simulation.status,
            progress=simulation.progress,
        )

        self._session.add(record)
        self._session.commit()

        return self._serialize_status(engine)

    # ==========================================================
    # LOOKUP
    # ==========================================================

    def _get_engine(self, simulation_id: str) -> SimulationEngine:
        with self._lock:
            engine = self._engines.get(simulation_id)

        if engine is None:
            raise KeyError(f"Simulation '{simulation_id}' not found.")

        return engine

    # ==========================================================
    # RUN
    # ==========================================================

    def start(self, simulation_id: str) -> dict:
        engine = self._get_engine(simulation_id)
        session = engine.session

        if session is None:
            raise KeyError(f"Simulation '{simulation_id}' not found.")

        if session.completed:
            return self._serialize_status(engine)

        future = self._futures.get(simulation_id)

        if future is not None and not future.done():
            return self._serialize_status(engine)

        self._update_record(
            simulation_id,
            status="RUNNING",
            progress=session.progress,
        )

        future = self._executor.submit(engine.run)

        with self._lock:
            self._futures[simulation_id] = future

        return self._serialize_status(engine)

    def wait(self, simulation_id: str) -> dict:
        """Wait for a started simulation and return its final result."""

        engine = self._get_engine(simulation_id)
        future = self._futures.get(simulation_id)

        if future is not None:
            future.result()

        self._sync_record(engine)
        return self.results(simulation_id)

    # ==========================================================
    # STATUS
    # ==========================================================

    def status(self, simulation_id: str) -> dict:
        engine = self._get_engine(simulation_id)
        self._sync_record(engine)
        return self._serialize_status(engine)

    # ==========================================================
    # RESULTS
    # ==========================================================

    def results(self, simulation_id: str) -> dict:
        engine = self._get_engine(simulation_id)

        if engine.session is None:
            raise KeyError(f"Simulation '{simulation_id}' not found.")

        result = engine.results()
        self._sync_record(engine)

        return result.model_dump(mode="json")

    def rams(self, simulation_id: str) -> dict:
        """Return RAMS intelligence for a completed simulation."""
        engine = self._get_engine(simulation_id)

        if engine.session is None:
            raise KeyError(f"Simulation '{simulation_id}' not found.")

        if not engine.session.completed:
            raise RuntimeError("RAMS analysis is available after simulation completion.")

        return engine.rams().model_dump(mode="json")

    # ==========================================================
    # REPLAY
    # ==========================================================

    def decision_support(self, simulation_id: str) -> dict:
        """Return explainable maintenance decisions for a completed simulation."""
        engine = self._get_engine(simulation_id)
        if engine.session is None:
            raise KeyError(f"Simulation '{simulation_id}' not found.")
        if not engine.session.completed:
            raise RuntimeError("Decision support is available after simulation completion.")
        return DecisionSupportEngine().analyze(engine.rams()).copy()

    def maintenance_what_if(
        self, simulation_id: str, asset_id: str, health_recovery: float = 15.0,
        degradation_reduction_percent: float = 30.0,
    ) -> dict:
        """Evaluate a non-persistent maintenance intervention scenario."""
        engine = self._get_engine(simulation_id)
        if engine.session is None:
            raise KeyError(f"Simulation '{simulation_id}' not found.")
        if not engine.session.completed:
            raise RuntimeError("Maintenance what-if analysis is available after simulation completion.")
        return DecisionSupportEngine().what_if(
            engine.rams(), asset_id, health_recovery, degradation_reduction_percent
        )

    def maintenance_what_if_batch(self, simulation_id: str, scenarios: list[dict]) -> dict:
        """Evaluate multiple non-persistent maintenance intervention scenarios."""
        engine = self._get_engine(simulation_id)
        if engine.session is None:
            raise KeyError(f"Simulation '{simulation_id}' not found.")
        if not engine.session.completed:
            raise RuntimeError("Maintenance what-if analysis is available after simulation completion.")
        if not scenarios:
            raise ValueError("At least one maintenance scenario is required.")
        if len(scenarios) > 12:
            raise ValueError("A maximum of 12 maintenance scenarios can be compared at once.")
        return DecisionSupportEngine().what_if_batch(engine.rams(), scenarios)

    def replay(self, simulation_id: str) -> dict:
        """
        Return the recorded replay timeline for a simulation.

        Each frame is an immutable snapshot captured by ReplayEngine.
        The response is JSON-ready for frontend analytics.
        """
        engine = self._get_engine(simulation_id)

        if engine.session is None:
            raise KeyError(f"Simulation '{simulation_id}' not found.")

        frames = []

        for frame in engine.replay_engine.frames():
            frames.append(
                {
                    "step": frame.step,
                    "timestamp": frame.timestamp.isoformat(),
                    "assets": [
                        asset.model_dump(mode="json")
                        for asset in frame.assets
                    ],
                }
            )

        return {
            "simulation_id": simulation_id,
            "total_frames": len(frames),
            "duration_seconds": engine.replay_engine.duration,
            "frames": frames,
        }

    # ==========================================================
    # CONTROL
    # ==========================================================

    def pause(self, simulation_id: str) -> dict:
        engine = self._get_engine(simulation_id)
        session = engine.session

        if session is None:
            raise KeyError(f"Simulation '{simulation_id}' not found.")

        if session.completed:
            return self._serialize_status(engine)

        engine._session = session.model_copy(
            update={
                "status": "PAUSED",
                "paused": True,
            }
        )

        self._sync_record(engine)
        return self._serialize_status(engine)

    def resume(self, simulation_id: str) -> dict:
        engine = self._get_engine(simulation_id)
        session = engine.session

        if session is None:
            raise KeyError(f"Simulation '{simulation_id}' not found.")

        if session.completed:
            return self._serialize_status(engine)

        engine._session = session.model_copy(
            update={
                "status": "RUNNING",
                "paused": False,
            }
        )

        future = self._futures.get(simulation_id)

        if future is None or future.done():
            future = self._executor.submit(engine.run)
            with self._lock:
                self._futures[simulation_id] = future

        self._sync_record(engine)
        return self._serialize_status(engine)

    def stop(self, simulation_id: str) -> dict:
        engine = self._get_engine(simulation_id)
        session = engine.session

        if session is None:
            raise KeyError(f"Simulation '{simulation_id}' not found.")

        if not session.completed:
            engine._session = session.model_copy(
                update={
                    "status": "CANCELLED",
                    "completed": True,
                    "paused": False,
                }
            )

        self._sync_record(engine)
        return self._serialize_status(engine)

    # ==========================================================
    # RESET
    # ==========================================================

    def reset(self, simulation_id: str) -> dict:
        engine = self._get_engine(simulation_id)

        future = self._futures.get(simulation_id)
        if future is not None and not future.done():
            raise RuntimeError(
                "Cannot reset a simulation while it is running."
            )

        engine.reset()
        self._update_record(
            simulation_id,
            status="IDLE",
            progress=0.0,
        )

        return {
            "simulation_id": simulation_id,
            "status": "IDLE",
            "progress": 0.0,
            "message": "Simulation reset.",
        }

    # ==========================================================
    # INTERNAL
    # ==========================================================

    def _serialize_status(self, engine: SimulationEngine) -> dict:
        status = engine.status()
        return {
            **status,
            "simulation_id": (
                engine.session.simulation_id
                if engine.session is not None
                else None
            ),
        }

    def _update_record(
        self,
        simulation_id: str,
        *,
        status: str,
        progress: float,
    ) -> None:
        record = (
            self._session.query(SimulationModel)
            .filter(SimulationModel.id == simulation_id)
            .first()
        )

        if record is None:
            return

        record.status = status
        record.progress = progress
        self._session.commit()

    def _sync_record(self, engine: SimulationEngine) -> None:
        session = engine.session
        if session is None:
            return

        self._update_record(
            session.simulation_id,
            status=session.status,
            progress=session.progress,
        )

    def shutdown(self) -> None:
        self._executor.shutdown(wait=False, cancel_futures=True)