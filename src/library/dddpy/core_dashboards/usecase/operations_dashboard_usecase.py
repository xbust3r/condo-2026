"""
Operations Dashboard Use Case — aggregates operational metrics for a condominium.

This is a query-only facade. It consumes data from existing repositories
and returns aggregated metrics. No domain entities or repositories are
created for this module.
"""
from datetime import date, datetime, timedelta
from collections import defaultdict

from library.dddpy.core_incidents.infrastructure.incident_query_repository import (
    IncidentQueryRepositoryImpl,
)
from library.dddpy.core_visitors.infrastructure.visitor_query_repository import (
    VisitorQueryRepositoryImpl,
)
from library.dddpy.core_packages.infrastructure.package_query_repository import (
    PackageQueryRepositoryImpl,
)


class OperationsDashboardUseCase:
    """Aggregates operational metrics for a condominium."""

    def get_dashboard(self, condominium_id: int) -> dict:
        """
        Returns operations dashboard:
        - incidents: open count, by_priority, by_category, avg_resolution_hours
        - visitors: today (registered, checked_in, no_show), this_week total
        - packages: pending_delivery, delivered_this_week
        """
        today = date.today()
        week_start = today - timedelta(days=today.weekday())  # Monday
        week_end = week_start + timedelta(days=6)  # Sunday

        incident_repo = IncidentQueryRepositoryImpl()
        visitor_repo = VisitorQueryRepositoryImpl()
        package_repo = PackageQueryRepositoryImpl()

        # ── 1. Incidents ──────────────────────────────────────────────────────
        # Open incidents (status in pending/open/in_progress)
        OPEN_STATUSES = {"pending", "open", "in_progress"}
        RESOLVED_STATUSES = {"resolved", "closed"}

        all_incidents, _ = incident_repo.list_all(
            condominium_id=condominium_id,
            limit=10000,
        )

        open_incidents = [i for i in all_incidents if i.status in OPEN_STATUSES]

        # By priority
        by_priority = defaultdict(int)
        for inc in open_incidents:
            by_priority[inc.priority] += 1

        # By category
        by_category = defaultdict(int)
        for inc in open_incidents:
            by_category[inc.category] += 1

        # Resolved this month
        this_month_start = today.replace(day=1)
        resolved_this_month = [
            i for i in all_incidents
            if i.status in RESOLVED_STATUSES
            and i.completed_date
            and i.completed_date >= this_month_start
        ]

        # Average resolution time (hours) for resolved incidents
        resolution_hours_list = []
        for inc in all_incidents:
            if inc.status in RESOLVED_STATUSES and inc.completed_date:
                created = inc.created_at
                if isinstance(created, datetime):
                    delta = inc.completed_date - created.date()
                else:
                    delta = inc.completed_date - created
                resolution_hours_list.append(delta.total_seconds() / 3600)

        avg_resolution_hours = (
            round(sum(resolution_hours_list) / len(resolution_hours_list), 1)
            if resolution_hours_list
            else 0.0
        )

        # ── 2. Visitors ──────────────────────────────────────────────────────
        today_str = today.isoformat()
        week_start_str = week_start.isoformat()
        week_end_str = week_end.isoformat()

        visitors_today, _ = visitor_repo.list_all(
            condominium_id=condominium_id,
            expected_date=today_str,
            limit=10000,
        )

        registered_today = len(visitors_today)
        checked_in_today = sum(1 for v in visitors_today if v.status == "checked_in")
        no_show_today = sum(1 for v in visitors_today if v.status == "no_show")
        pending_today = sum(1 for v in visitors_today if v.status == "pending")

        # This week: sum all visitors with expected_date in [week_start, week_end]
        visitors_week, _ = visitor_repo.list_all(
            condominium_id=condominium_id,
            limit=10000,
        )
        visitors_this_week = [
            v for v in visitors_week
            if v.expected_date
            and week_start <= v.expected_date <= week_end
        ]
        this_week_total = len(visitors_this_week)

        # ── 3. Packages ─────────────────────────────────────────────────────
        pending_packages, _ = package_repo.list_pending(
            condominium_id=condominium_id,
            limit=10000,
        )
        pending_delivery = len(pending_packages)

        # Delivered this week
        all_packages_week, _ = package_repo.list_all(
            condominium_id=condominium_id,
            limit=10000,
        )
        delivered_this_week = [
            p for p in all_packages_week
            if p.status == "delivered"
            and p.delivered_at
            and isinstance(p.delivered_at, datetime)
            and week_start <= p.delivered_at.date() <= week_end
        ]
        delivered_this_week_count = len(delivered_this_week)

        return {
            "condominium_id": condominium_id,
            "as_of": datetime.utcnow().isoformat() + "Z",
            "incidents": {
                "open": len(open_incidents),
                "resolved_this_month": len(resolved_this_month),
                "by_priority": dict(by_priority),
                "by_category": dict(by_category),
                "avg_resolution_hours": avg_resolution_hours,
            },
            "visitors": {
                "today": {
                    "registered": registered_today,
                    "checked_in": checked_in_today,
                    "no_show": no_show_today,
                    "pending": pending_today,
                },
                "this_week": this_week_total,
            },
            "packages": {
                "pending_delivery": pending_delivery,
                "delivered_this_week": delivered_this_week_count,
            },
        }
