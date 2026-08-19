"""
TrackGuard AI
Track Digital Operations Sandbox (TDOS)

routes/simulation.py

REST API endpoints for TDOS simulation execution.
"""

from fastapi import APIRouter, HTTPException

from database.database import get_session
from schemas.simulation import (
    SimulationActionResponse,
    SimulationCreateRequest,
)
from services.simulation_service import SimulationService

router = APIRouter(
    prefix="/simulations",
    tags=["Simulations"],
)


def _service():
    session = get_session()
    return session, SimulationService(session)


@router.post("")
def create_simulation(request: SimulationCreateRequest):
    session, service = _service()
    try:
        return service.create(request)
    finally:
        session.close()


@router.post("/{simulation_id}/start")
def start_simulation(simulation_id: str):
    session, service = _service()
    try:
        try:
            return service.start(simulation_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
    finally:
        session.close()


@router.post("/{simulation_id}/run")
def run_simulation(simulation_id: str):
    """
    Start a simulation and wait for completion.

    This endpoint is convenient for scripts and simple clients.
    The /start endpoint is the non-blocking lifecycle operation.
    """
    session, service = _service()
    try:
        try:
            service.start(simulation_id)
            return service.wait(simulation_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except RuntimeError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
    finally:
        session.close()


@router.get("/{simulation_id}")
def get_simulation(simulation_id: str):
    session, service = _service()
    try:
        try:
            return service.status(simulation_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
    finally:
        session.close()


@router.get("/{simulation_id}/results")
def get_simulation_results(simulation_id: str):
    session, service = _service()
    try:
        try:
            return service.results(simulation_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except RuntimeError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
    finally:
        session.close()




@router.get("/{simulation_id}/replay")
def get_simulation_replay(simulation_id: str):
    """Return recorded replay frames for the completed simulation."""
    session, service = _service()
    try:
        try:
            return service.replay(simulation_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except RuntimeError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
    finally:
        session.close()


@router.get("/{simulation_id}/rams")
def get_simulation_rams(simulation_id: str):
    """Return RAMS intelligence for the completed simulation."""
    session, service = _service()
    try:
        try:
            return service.rams(simulation_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except RuntimeError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
    finally:
        session.close()


@router.get("/{simulation_id}/decision-support")
def get_simulation_decision_support(simulation_id: str):
    """Return explainable maintenance decisions for the completed simulation."""
    session, service = _service()
    try:
        try:
            return service.decision_support(simulation_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except RuntimeError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
    finally:
        session.close()


@router.post("/{simulation_id}/maintenance-what-if/batch")
def maintenance_what_if_batch(simulation_id: str, payload: dict):
    """Compare multiple non-persistent maintenance intervention scenarios."""
    session, service = _service()
    try:
        scenarios = payload.get("scenarios") if isinstance(payload, dict) else None

        if not isinstance(scenarios, list) or not scenarios:
            raise HTTPException(
                status_code=422,
                detail="At least one maintenance scenario is required.",
            )

        if len(scenarios) > 12:
            raise HTTPException(
                status_code=422,
                detail="A maximum of 12 maintenance scenarios can be compared at once.",
            )

        try:
            return service.maintenance_what_if_batch(
                simulation_id,
                scenarios,
            )
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except RuntimeError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
    finally:
        session.close()


@router.post(
    "/{simulation_id}/pause",
    response_model=SimulationActionResponse,
)
def pause_simulation(simulation_id: str):
    session, service = _service()
    try:
        try:
            return service.pause(simulation_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
    finally:
        session.close()


@router.post(
    "/{simulation_id}/resume",
    response_model=SimulationActionResponse,
)
def resume_simulation(simulation_id: str):
    session, service = _service()
    try:
        try:
            return service.resume(simulation_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
    finally:
        session.close()


@router.post(
    "/{simulation_id}/stop",
    response_model=SimulationActionResponse,
)
def stop_simulation(simulation_id: str):
    session, service = _service()
    try:
        try:
            return service.stop(simulation_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
    finally:
        session.close()


@router.post(
    "/{simulation_id}/reset",
    response_model=SimulationActionResponse,
)
def reset_simulation(simulation_id: str):
    session, service = _service()
    try:
        try:
            return service.reset(simulation_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except RuntimeError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
    finally:
        session.close()
