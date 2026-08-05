"""
TrackGuard AI
Track Digital Operations Sandbox (TDOS)

routes/models.py

REST API routes for AI Model Registry.

Author  : TrackGuard AI Team
Version : 1.0.0
"""

from fastapi import (
    APIRouter,
    HTTPException,
)

from database.database import get_session

from repositories.model_repository import ModelRepository

from schemas.schemas import ModelRegistry

from services.model_service import ModelService


router = APIRouter(

    prefix="/models",

    tags=["Model Registry"],

)


# =====================================================
# CREATE
# =====================================================

@router.post("")
def register_model(
    model: ModelRegistry,
):
    """
    Registers a new AI model.
    """

    session = get_session()

    repository = ModelRepository(session)

    service = ModelService(repository)

    return service.register_model(model)


# =====================================================
# GET ALL
# =====================================================

@router.get("")
def get_all_models():
    """
    Returns every registered AI model.
    """

    session = get_session()

    repository = ModelRepository(session)

    service = ModelService(repository)

    return service.get_all_models()


# =====================================================
# GET ONE
# =====================================================

@router.get("/{model_id}")
def get_model(
    model_id: str,
):
    """
    Returns one registered model.
    """

    session = get_session()

    repository = ModelRepository(session)

    service = ModelService(repository)

    model = service.get_model(model_id)

    if model is None:

        raise HTTPException(

            status_code=404,

            detail="Model not found",

        )

    return model


# =====================================================
# SEARCH
# =====================================================

@router.get("/search/{keyword}")
def search_models(
    keyword: str,
):
    """
    Searches registered models.
    """

    session = get_session()

    repository = ModelRepository(session)

    service = ModelService(repository)

    return service.search_models(keyword)


# =====================================================
# DELETE
# =====================================================

@router.delete("/{model_id}")
def delete_model(
    model_id: str,
):
    """
    Deletes one registered model.
    """

    session = get_session()

    repository = ModelRepository(session)

    service = ModelService(repository)

    deleted = service.delete_model(model_id)

    if not deleted:

        raise HTTPException(

            status_code=404,

            detail="Model not found",

        )

    return {

        "message": "Model deleted"

    }