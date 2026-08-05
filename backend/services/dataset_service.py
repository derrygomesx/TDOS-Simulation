"""
TrackGuard AI
Track Digital Operations Sandbox (TDOS)

dataset_service.py

Business logic for Dataset Management.

Author  : TrackGuard AI Team
Version : 1.0.0
"""

from datetime import datetime

from config.enums import DatasetStatus

from database.models import DatasetModel

from repositories.dataset_repository import DatasetRepository

from schemas.schemas import Dataset


class DatasetService:
    """
    Handles Dataset business logic.

    This service sits between the API layer
    and the repository layer.

    Responsibilities

    • Create datasets
    • Retrieve datasets
    • Search datasets
    • Delete datasets
    """

    def __init__(
        self,
        repository: DatasetRepository,
    ) -> None:

        self._repository = repository

    # =====================================================
    # CREATE
    # =====================================================

    def create_dataset(
        self,
        dataset: Dataset,
    ) -> DatasetModel:
        """
        Creates a new dataset.
        """

        model = DatasetModel(

            name=dataset.name,

            version=dataset.version,

            status=DatasetStatus.ACTIVE.value,

            created_at=datetime.utcnow(),

            updated_at=datetime.utcnow(),

        )

        return self._repository.create(model)

    # =====================================================
    # GET ALL
    # =====================================================

    def get_all_datasets(
        self,
    ) -> list[DatasetModel]:
        """
        Returns every dataset.
        """

        return self._repository.get_all()

    # =====================================================
    # GET ONE
    # =====================================================

    def get_dataset(
        self,
        dataset_id: str,
    ) -> DatasetModel | None:
        """
        Returns one dataset.
        """

        return self._repository.get_by_id(
            dataset_id
        )

    # =====================================================
    # SEARCH
    # =====================================================

    def search_datasets(
        self,
        keyword: str,
    ) -> list[DatasetModel]:
        """
        Searches datasets by name.
        """

        return self._repository.search(
            keyword
        )

    # =====================================================
    # DELETE
    # =====================================================

    def delete_dataset(
        self,
        dataset_id: str,
    ) -> bool:
        """
        Deletes one dataset.
        """

        dataset = self._repository.get_by_id(
            dataset_id
        )

        if dataset is None:

            return False

        self._repository.delete(dataset)

        return True