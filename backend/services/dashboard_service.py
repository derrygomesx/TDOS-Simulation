"""
TrackGuard AI
Track Digital Operations Sandbox (TDOS)

dashboard_service.py

Business logic for Dashboard.

Author  : TrackGuard AI Team
Version : 1.0.0
"""

from repositories.dashboard_repository import DashboardRepository

from schemas.schemas import DashboardMetrics


class DashboardService:
    """
    Dashboard business logic.
    """

    def __init__(
        self,
        repository: DashboardRepository,
    ) -> None:

        self._repository = repository

    # =====================================================
    # DASHBOARD
    # =====================================================

    def get_dashboard(
        self,
    ) -> DashboardMetrics:
        """
        Returns dashboard metrics.
        """

        metrics = self._repository.get_dashboard_metrics()

        return DashboardMetrics(

            active_experiments=metrics.active_experiments,

            active_models=metrics.active_models,

            datasets=metrics.datasets,

            reports=metrics.reports,

            running_simulations=metrics.running_simulations,

            system_health=metrics.system_health,

        )