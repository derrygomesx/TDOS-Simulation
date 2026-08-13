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
