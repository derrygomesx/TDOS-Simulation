"""
TrackGuard AI
Track Digital Operations Sandbox (TDOS)

dashboard_repository.py

Repository for Dashboard metrics.

Author  : TrackGuard AI Team
Version : 1.0.0
"""

from sqlalchemy.orm import Session

from database.models import (
    DashboardCacheModel,
    DatasetModel,
    ExperimentModel,
    ModelRegistryModel,
    ReportModel,
    SimulationModel,
)


class DashboardRepository:
    """
    Provides dashboard statistics.
    """

    def __init__(
        self,
        session: Session,
    ):

        self._session = session

    # =====================================================
    # METRICS
    # =====================================================

    def get_dashboard_metrics(
        self,
    ) -> DashboardCacheModel:

        cache = (

            self._session

            .query(DashboardCacheModel)

            .first()

        )

        if cache:

            return cache

        dashboard = DashboardCacheModel(

            id=1,

            active_experiments=self._session.query(
                ExperimentModel
            ).count(),

            active_models=self._session.query(
                ModelRegistryModel
            ).count(),

            datasets=self._session.query(
                DatasetModel
            ).count(),

            reports=self._session.query(
                ReportModel
            ).count(),

            running_simulations=self._session.query(
                SimulationModel
            ).count(),

            system_health="HEALTHY",

        )

        self._session.add(
            dashboard
        )

        self._session.commit()

        self._session.refresh(
            dashboard
        )

        return dashboard