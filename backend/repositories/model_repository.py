"""
TrackGuard AI
Track Digital Operations Sandbox (TDOS)

model_repository.py

Repository for AI Model Registry database operations.

Author  : TrackGuard AI Team
Version : 1.0.0
"""

from sqlalchemy.orm import Session

from database.models import ModelRegistryModel


class ModelRepository:
    """
    Handles all AI Model Registry database operations.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:

        self._session = session

    # =====================================================
    # CREATE
    # =====================================================

    def create(
        self,
        model: ModelRegistryModel,
    ) -> ModelRegistryModel:
        """
        Registers a new AI model.
        """

        self._session.add(model)

        self._session.commit()

        self._session.refresh(model)

        return model

    # =====================================================
    # GET ALL
    # =====================================================

    def get_all(
        self,
    ) -> list[ModelRegistryModel]:
        """
        Returns every registered model.
        """

        return (

            self._session

            .query(ModelRegistryModel)

            .all()

        )

    # =====================================================
    # GET ONE
    # =====================================================

    def get_by_id(
        self,
        model_id: str,
    ) -> ModelRegistryModel | None:
        """
        Returns one model.
        """

        return (

            self._session

            .query(ModelRegistryModel)

            .filter(
                ModelRegistryModel.id == model_id
            )

            .first()

        )

    # =====================================================
    # SEARCH
    # =====================================================

    def search(
        self,
        keyword: str,
    ) -> list[ModelRegistryModel]:
        """
        Searches models by name.
        """

        return (

            self._session

            .query(ModelRegistryModel)

            .filter(
                ModelRegistryModel.name.contains(keyword)
            )

            .all()

        )

    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        model: ModelRegistryModel,
    ) -> ModelRegistryModel:
        """
        Updates a model.
        """

        self._session.commit()

        self._session.refresh(model)

        return model

    # =====================================================
    # DELETE
    # =====================================================

    def delete(
        self,
        model: ModelRegistryModel,
    ) -> None:
        """
        Deletes a model.
        """

        self._session.delete(model)

        self._session.commit()