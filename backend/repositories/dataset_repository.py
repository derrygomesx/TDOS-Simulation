"""
TrackGuard AI
Track Digital Operations Sandbox (TDOS)

dataset_repository.py

Repository for dataset database operations.

Author  : TrackGuard AI Team
Version : 1.0.0
"""

from sqlalchemy.orm import Session

from database.models import DatasetModel


class DatasetRepository:
    """
    Handles all Dataset database operations.
    """

    def __init__(
        self,
        session: Session,
    ):

        self._session = session

    # =====================================================
    # CREATE
    # =====================================================

    def create(
        self,
        dataset: DatasetModel,
    ) -> DatasetModel:

        self._session.add(dataset)

        self._session.commit()

        self._session.refresh(dataset)

        return dataset

    # =====================================================
    # READ
    # =====================================================

    def get_all(
        self,
    ) -> list[DatasetModel]:

        return (

            self._session

            .query(DatasetModel)

            .all()

        )

    def get_by_id(
        self,
        dataset_id: str,
    ) -> DatasetModel | None:

        return (

            self._session

            .query(DatasetModel)

            .filter(
                DatasetModel.id == dataset_id
            )

            .first()

        )

    def search(
        self,
        keyword: str,
    ) -> list[DatasetModel]:

        return (

            self._session

            .query(DatasetModel)

            .filter(
                DatasetModel.name.contains(keyword)
            )

            .all()

        )

    # =====================================================
    # DELETE
    # =====================================================

    def delete(
        self,
        dataset: DatasetModel,
    ) -> None:

        self._session.delete(dataset)

        self._session.commit()