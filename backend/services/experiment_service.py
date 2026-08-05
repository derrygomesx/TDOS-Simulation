"""
TrackGuard AI
Track Digital Operations Sandbox (TDOS)

experiment_service.py

Business logic for experiment management.

Author  : TrackGuard AI Team
Version : 1.0.0
"""

from datetime import datetime

from config.enums import ExperimentStatus
from database.models import ExperimentModel
from repositories.experiment_repository import ExperimentRepository
from schemas.schemas import Experiment


class ExperimentService:
    """
    Handles experiment business logic.
    """

    def __init__(
        self,
        repository: ExperimentRepository,
    ):

        self._repository = repository

    # =====================================================
    # CREATE
    # =====================================================

    def create_experiment(
        self,
        experiment: Experiment,
    ) -> ExperimentModel:

        model = ExperimentModel(

            name=experiment.name,

            description=experiment.description,

            status=ExperimentStatus.CREATED.value,

            created_at=datetime.utcnow(),

            updated_at=datetime.utcnow(),

        )

        return self._repository.create(model)

    # =====================================================
    # READ
    # =====================================================

    def get_experiment(
        self,
        experiment_id: str,
    ):

        return self._repository.get_by_id(experiment_id)

    def get_all_experiments(self):

        return self._repository.get_all()

    # =====================================================
    # DELETE
    # =====================================================

    def delete_experiment(
        self,
        experiment_id: str,
    ) -> bool:

        experiment = self._repository.get_by_id(experiment_id)

        if experiment is None:

            return False

        self._repository.delete(experiment)

        return True