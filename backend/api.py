"""
TDOS API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.config import settings

from routes.dashboard import router as dashboard_router
from routes.datasets import router as dataset_router
from routes.experiments import router as experiment_router
from routes.health import router as health_router
from routes.models import router as model_router
from routes.reports import router as report_router
from routes.simulation import router as simulation_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(experiment_router)
app.include_router(dataset_router)
app.include_router(model_router)
app.include_router(report_router)
app.include_router(dashboard_router)
app.include_router(simulation_router)
