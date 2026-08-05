"""
TrackGuard AI
Track Digital Operations Sandbox (TDOS)

routes/experiments.py

Experiment REST endpoints.

Author  : TrackGuard AI Team
Version : 1.0.0
"""

from fastapi import APIRouter, HTTPException

from database.database import get_session
from repositories.experiment_repository import ExperimentRepository
from schemas.schemas import Experiment
from services.experiment_service import ExperimentService

router = APIRouter(

    prefix="/experiments",

    tags=["Experiments"],

)


@router.post("")
def create_experiment(
    experiment: Experiment,
):

    session = get_session()

    repository = ExperimentRepository(session)

    service = ExperimentService(repository)

    return service.create_experiment(experiment)


@router.get("")
def get_all_experiments():

    session = get_session()

    repository = ExperimentRepository(session)

    service = ExperimentService(repository)

    return service.get_all_experiments()


@router.get("/{experiment_id}")
def get_experiment(
    experiment_id: str,
):

    session = get_session()

    repository = ExperimentRepository(session)

    service = ExperimentService(repository)

    experiment = service.get_experiment(
        experiment_id
    )

    if experiment is None:

        raise HTTPException(

            status_code=404,

            detail="Experiment not found",

        )

    return experiment


@router.delete("/{experiment_id}")
def delete_experiment(
    experiment_id: str,
):

    session = get_session()

    repository = ExperimentRepository(session)

    service = ExperimentService(repository)

    deleted = service.delete_experiment(
        experiment_id
    )

    if not deleted:

        raise HTTPException(

            status_code=404,

            detail="Experiment not found",

        )

    return {

        "message": "Experiment deleted"

    }