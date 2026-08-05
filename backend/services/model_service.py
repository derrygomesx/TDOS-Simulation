"""
TrackGuard AI
Track Digital Operations Sandbox (TDOS)

model_service.py

Business logic for AI Model Registry.

Author  : TrackGuard AI Team
Version : 1.0.0
"""

from datetime import datetime

from config.enums import ModelStatus

from database.models import ModelRegistryModel

from repositories.model_repository import ModelRepository

from schemas.schemas import ModelRegistry


class ModelService:
    """
    Handles AI Model Registry business logic.

    Responsibilities

    • Register models
    • Retrieve models
    • Search models
    • Update models
    • Delete models
    """

    def __init__(
        self,
        repository: ModelRepository,
    ) -> None:

        self._repository = repository

    # =====================================================
    # CREATE
    # =====================================================

    def register_model(
        self,
        model: ModelRegistry,
    ) -> ModelRegistryModel:
        """
        Registers a new AI model.
        """

        model_db = ModelRegistryModel(

            name=model.name,

            version=model.version,

            architecture=model.architecture,

            precision=model.precision,

            recall=model.recall,

            inference_time=model.inference_time,

            status=ModelStatus.TRAINING.value,

            created_at=datetime.utcnow(),

            updated_at=datetime.utcnow(),

        )

        return self._repository.create(
            model_db
        )

    # =====================================================
    # GET ALL
    # =====================================================

    def get_all_models(
        self,
    ) -> list[ModelRegistryModel]:
        """
        Returns every registered model.
        """

        return self._repository.get_all()

    # =====================================================
    # GET ONE
    # =====================================================

    def get_model(
        self,
        model_id: str,
    ) -> ModelRegistryModel | None:
        """
        Returns one registered model.
        """

        return self._repository.get_by_id(
            model_id
        )

    # =====================================================
    # SEARCH
    # =====================================================

    def search_models(
        self,
        keyword: str,
    ) -> list[ModelRegistryModel]:
        """
        Searches registered models.
        """

        return self._repository.search(
            keyword
        )

    # =====================================================
    # UPDATE
    # =====================================================

    def update_model(
        self,
        model: ModelRegistryModel,
    ) -> ModelRegistryModel:
        """
        Updates a registered model.
        """

        model.updated_at = datetime.utcnow()

        return self._repository.update(
            model
        )

    # =====================================================
    # DELETE
    # =====================================================

    def delete_model(
        self,
        model_id: str,
    ) -> bool:
        """
        Deletes one registered model.
        """

        model = self._repository.get_by_id(
            model_id
        )

        if model is None:

            return False

        self._repository.delete(
            model
        )

        return True