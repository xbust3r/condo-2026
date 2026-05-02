"""
Factory: Visitor.

Creates test visitor records directly in the DB via SQLAlchemy.
"""
import uuid
from datetime import date, time
from sqlalchemy.orm import Session
from sqlalchemy import func

from library.dddpy.core_visitors.infrastructure.dbvisitor import DBVisitor


class VisitorFactory:
    """Factory for creating test Visitor records."""

    @staticmethod
    def create(
        session: Session,
        condominium_id: int,
        unit_id: int,
        host_user_id: int,
        visitor_name: str = None,
        expected_date: date = None,
        expected_time: time = None,
        status: str = "pending",
        building_id: int = None,
        visit_purpose: str = "visit",
        access_code: str = None,
        notes: str = None,
        **kwargs,
    ) -> DBVisitor:
        db_visitor = DBVisitor(
            uuid=str(uuid.uuid4()),
            condominium_id=condominium_id,
            building_id=building_id,
            unit_id=unit_id,
            host_user_id=host_user_id,
            visitor_name=visitor_name or "Factory Visitor",
            expected_date=expected_date or date.today(),
            expected_time=expected_time or time(14, 0),
            status=status,
            visit_purpose=visit_purpose,
            access_code=access_code or f"V{uuid.uuid4().hex[:6].upper()}",
            notes=notes,
            updated_at=kwargs.get("updated_at", func.now()),
        )
        session.add(db_visitor)
        session.flush()
        session.refresh(db_visitor)
        return db_visitor
