"""
TrackGuard AI
Track Digital Operations Sandbox (TDOS)

report_service.py

Business logic for Report Management.

Author  : TrackGuard AI Team
Version : 1.0.0
"""

from datetime import datetime

from database.models import ReportModel

from repositories.report_repository import ReportRepository

from reports.report_factory import ReportFactory

from schemas.schemas import Report


class ReportService:
    """
    Handles Report Management business logic.

    Responsibilities

    • Generate reports
    • Store reports
    • Retrieve reports
    • Delete reports
    """

    def __init__(
        self,
        repository: ReportRepository,
    ) -> None:

        self._repository = repository

        self._factory = ReportFactory()

    # =====================================================
    # GENERATE REPORT
    # =====================================================

    def generate_report(
        self,
        report: Report,
        export_type: str,
    ) -> ReportModel:
        """
        Generates and stores a report.
        """

        generator = self._factory.get_generator(
            export_type
        )

        output_path = report.file_path

        generator.generate(

            report_data=report,

            output_path=output_path,

        )

        report_model = ReportModel(

            title=report.title,

            report_type=report.report_type.value,

            file_path=output_path,

            created_at=datetime.utcnow(),

        )

        return self._repository.create(
            report_model
        )

    # =====================================================
    # GET ALL
    # =====================================================

    def get_all_reports(
        self,
    ) -> list[ReportModel]:
        """
        Returns every report.
        """

        return self._repository.get_all()

    # =====================================================
    # GET ONE
    # =====================================================

    def get_report(
        self,
        report_id: str,
    ) -> ReportModel | None:
        """
        Returns one report.
        """

        return self._repository.get_by_id(
            report_id
        )

    # =====================================================
    # DELETE
    # =====================================================

    def delete_report(
        self,
        report_id: str,
    ) -> bool:
        """
        Deletes one report.
        """

        report = self._repository.get_by_id(
            report_id
        )

        if report is None:

            return False

        self._repository.delete(report)

        return True