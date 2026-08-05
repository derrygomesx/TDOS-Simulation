"""
TrackGuard AI
Track Digital Operations Sandbox (TDOS)

test_model_registry.py

Tests for the Model Registry module.

Author  : TrackGuard AI Team
Version : 1.0.0
"""

from database.database import (
    get_session,
    initialize_database,
)

from database.models import ModelRegistryModel

from repositories.model_repository import ModelRepository

from services.model_service import ModelService

from schemas.schemas import ModelRegistry


def test_register_model():
    """
    ModelService should register a model.
    """

    initialize_database()

    session = get_session()

    repository = ModelRepository(session)

    service = ModelService(repository)

    request = ModelRegistry(

        name="YOLOv11",

        version="1.0",

        architecture="YOLO",

        precision=97.5,

        recall=96.8,

        inference_time=11.4,

    )

    model = service.register_model(
        request
    )

    assert model.name == "YOLOv11"

    assert model.version == "1.0"

    assert model.architecture == "YOLO"

    assert model.precision == 97.5

    assert model.recall == 96.8