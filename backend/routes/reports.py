"""
TrackGuard AI
Track Digital Operations Sandbox (TDOS)

routes/reports.py

REST API routes for Report Management.

Author  : TrackGuard AI Team
Version : 1.0.0
"""

from fastapi import (
    APIRouter,
    HTTPException,
)

from database.database import get_session

from repositories.report_repository import ReportRepository

from schemas.schemas import Report

from services.report_service import ReportService


router = APIRouter(

    prefix="/reports",

    tags=["Reports"],

)


# =====================================================
# GENERATE REPORT
# =====================================================

@router.post("/{export_type}")
def generate_report(
    report: Report,
    export_type: str,
):
    """
    Generates a report.
    """

    session = get_session()

    repository = ReportRepository(session)

    service = ReportService(repository)

    return service.generate_report(
        report,
        export_type,
    )


# =====================================================
# GET ALL
# =====================================================

@router.get("")
def get_all_reports():
    """
    Returns every report.
    """

    session = get_session()

    repository = ReportRepository(session)

    service = ReportService(repository)

    return service.get_all_reports()


# =====================================================
# GET ONE
# =====================================================

@router.get("/{report_id}")
def get_report(
    report_id: str,
):
    """
    Returns one report.
    """

    session = get_session()

    repository = ReportRepository(session)

    service = ReportService(repository)

    report = service.get_report(
        report_id
    )

    if report is None:

        raise HTTPException(

            status_code=404,

            detail="Report not found",

        )

    return report


# =====================================================
# DELETE
# =====================================================

@router.delete("/{report_id}")
def delete_report(
    report_id: str,
):
    """
    Deletes one report.
    """

    session = get_session()

    repository = ReportRepository(session)

    service = ReportService(repository)

    deleted = service.delete_report(
        report_id
    )

    if not deleted:

        raise HTTPException(

            status_code=404,

            detail="Report not found",

        )

    return {

        "message": "Report deleted"

    }