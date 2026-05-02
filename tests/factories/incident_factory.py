"""
Factory: Incident.

Creates test incident records directly in the DB via SQLAlchemy.
"""
import uuid
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func

from library.dddpy.core_incidents.infrastructure.dbinicident import DBIncident


class IncidentFactory:
    """Factory for creating test Incident records."""

    @staticmethod
    def create(
        session: Session,
        condominium_id: int,
        unit_id: int,
        reported_by_user_id: int,
        title: str = None,
        category: str = "other",
        priority: str = "medium",
        status: str = "pending",
        building_id: int = None,
        assigned_to_user_id: int = None,
        description: str = None,
        scheduled_date: date = None,
        **kwargs,
    ) -> DBIncident:
        db_incident = DBIncident(
            uuid=str(uuid.uuid4()),
            condominium_id=condominium_id,
            building_id=building_id,
            unit_id=unit_id,
            reported_by_user_id=reported_by_user_id,
            assigned_to_user_id=assigned_to_user_id,
            category=category,
            priority=priority,
            status=status,
            title=title or "Factory-created incident",
            description=description or "Test incident description",
            scheduled_date=scheduled_date,
            updated_at=kwargs.get("updated_at", func.now()),
        )
        session.add(db_incident)
        session.flush()
        session.refresh(db_incident)
        return db_incident
