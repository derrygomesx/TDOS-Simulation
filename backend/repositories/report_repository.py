"""
TrackGuard AI
Track Digital Operations Sandbox (TDOS)

report_repository.py

Repository for Report Management.

Author  : TrackGuard AI Team
Version : 1.0.0
"""

from sqlalchemy.orm import Session

from database.models import ReportModel


class ReportRepository:
    """
    Handles all database operations
    related to reports.
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
        report: ReportModel,
    ) -> ReportModel:
        """
        Stores a generated report.
        """

        self._session.add(report)

        self._session.commit()

        self._session.refresh(report)

        return report

    # =====================================================
    # GET ALL
    # =====================================================

    def get_all(
        self,
    ) -> list[ReportModel]:
        """
        Returns every report.
        """

        return (

            self._session

            .query(ReportModel)

            .all()

        )

    # =====================================================
    # GET ONE
    # =====================================================

    def get_by_id(
        self,
        report_id: str,
    ) -> ReportModel | None:
        """
        Returns one report.
        """

        return (

            self._session

            .query(ReportModel)

            .filter(
                ReportModel.id == report_id
            )

            .first()

        )

    # =====================================================
    # DELETE
    # =====================================================

    def delete(
        self,
        report: ReportModel,
    ) -> None:
        """
        Deletes one report.
        """

        self._session.delete(report)

        self._session.commit()