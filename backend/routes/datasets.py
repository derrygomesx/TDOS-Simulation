"""
TrackGuard AI
Track Digital Operations Sandbox (TDOS)

routes/datasets.py

REST API routes for Dataset Management.

Author  : TrackGuard AI Team
Version : 1.0.0
"""

from fastapi import (
    APIRouter,
    HTTPException,
)

from database.database import get_session

from repositories.dataset_repository import DatasetRepository

from schemas.schemas import Dataset

from services.dataset_service import DatasetService


router = APIRouter(

    prefix="/datasets",

    tags=["Datasets"],

)


# =====================================================
# CREATE
# =====================================================

@router.post("")
def create_dataset(
    dataset: Dataset,
):
    """
    Creates a new dataset.
    """

    session = get_session()

    repository = DatasetRepository(session)

    service = DatasetService(repository)

    return service.create_dataset(dataset)


# =====================================================
# GET ALL
# =====================================================

@router.get("")
def get_all_datasets():
    """
    Returns every dataset.
    """

    session = get_session()

    repository = DatasetRepository(session)

    service = DatasetService(repository)

    return service.get_all_datasets()


# =====================================================
# GET ONE
# =====================================================

@router.get("/{dataset_id}")
def get_dataset(
    dataset_id: str,
):
    """
    Returns one dataset.
    """

    session = get_session()

    repository = DatasetRepository(session)

    service = DatasetService(repository)

    dataset = service.get_dataset(
        dataset_id
    )

    if dataset is None:

        raise HTTPException(

            status_code=404,

            detail="Dataset not found",

        )

    return dataset


# =====================================================
# SEARCH
# =====================================================

@router.get("/search/{keyword}")
def search_dataset(
    keyword: str,
):
    """
    Searches datasets.
    """

    session = get_session()

    repository = DatasetRepository(session)

    service = DatasetService(repository)

    return service.search_datasets(
        keyword
    )


# =====================================================
# DELETE
# =====================================================

@router.delete("/{dataset_id}")
def delete_dataset(
    dataset_id: str,
):
    """
    Deletes one dataset.
    """

    session = get_session()

    repository = DatasetRepository(session)

    service = DatasetService(repository)

    deleted = service.delete_dataset(
        dataset_id
    )

    if not deleted:

        raise HTTPException(

            status_code=404,

            detail="Dataset not found",

        )

    return {

        "message": "Dataset deleted"

    }