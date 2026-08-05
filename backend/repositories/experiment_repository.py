"""
TrackGuard AI
Track Digital Operations Sandbox (TDOS)

experiment_repository.py

Repository for Experiment database operations.

Author  : TrackGuard AI Team
Version : 1.0.0
"""

from sqlalchemy.orm import Session

from database.models import ExperimentModel


class ExperimentRepository:
    """
    Handles all Experiment database operations.
    """

    def __init__(self, session: Session):

        self._session = session

    # =====================================================
    # CREATE
    # =====================================================

    def create(
        self,
        experiment: ExperimentModel,
    ) -> ExperimentModel:

        self._session.add(experiment)

        self._session.commit()

        self._session.refresh(experiment)

        return experiment

    # =====================================================
    # READ
    # =====================================================

    def get_by_id(
        self,
        experiment_id: str,
    ) -> ExperimentModel | None:

        return (

            self._session.query(ExperimentModel)

            .filter(

                ExperimentModel.id == experiment_id

            )

            .first()

        )

    def get_all(self) -> list[ExperimentModel]:

        return (

            self._session.query(

                ExperimentModel

            )

            .all()

        )

    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        experiment: ExperimentModel,
    ) -> ExperimentModel:

        self._session.commit()

        self._session.refresh(experiment)

        return experiment

    # =====================================================
    # DELETE
    # =====================================================

    def delete(
        self,
        experiment: ExperimentModel,
    ) -> None:

        self._session.delete(experiment)

        self._session.commit()