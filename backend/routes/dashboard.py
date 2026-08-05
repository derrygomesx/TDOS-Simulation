"""
TrackGuard AI
Track Digital Operations Sandbox (TDOS)

routes/dashboard.py

REST API routes for Dashboard.

Author  : TrackGuard AI Team
Version : 1.0.0
"""

from fastapi import APIRouter

from database.database import get_session

from repositories.dashboard_repository import DashboardRepository

from services.dashboard_service import DashboardService


router = APIRouter(

    prefix="/dashboard",

    tags=["Dashboard"],

)


# =====================================================
# DASHBOARD METRICS
# =====================================================

@router.get("")
def get_dashboard():
    """
    Returns dashboard metrics.
    """

    session = get_session()

    repository = DashboardRepository(session)

    service = DashboardService(repository)

    return service.get_dashboard()