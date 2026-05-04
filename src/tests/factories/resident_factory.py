"""
Factory: ResidentEntity (core_resident_profiles table).

Creates test resident profile records directly in the DB.
Residents link a user to a condominium/unit.
"""
import uuid
from sqlalchemy.orm import Session

from library.dddpy.core_residents.infrastructure.dbresident import DBResidentProfile


class ResidentFactory:
    """Factory for creating test Resident records."""

    @staticmethod
    def create(
        session: Session,
        user_id: int,
        condominium_id: int,
        notify_announcements: bool = True,
        notify_incidents: bool = True,
        notify_packages: bool = True,
        notify_visitors: bool = True,
        notify_payments: bool = True,
        language: str = "es",
        theme: str = "light",
        **kwargs,
    ) -> DBResidentProfile:
        """
        Create and persist a ResidentProfile record.

        Usage:
            resident = ResidentFactory.create(
                session,
                user_id=user.id,
                condominium_id=condo.id
            )
        """
        db_resident = DBResidentProfile(
            uuid=str(uuid.uuid4()),
            user_id=user_id,
            condominium_id=condominium_id,
            notify_announcements=notify_announcements,
            notify_incidents=notify_incidents,
            notify_packages=notify_packages,
            notify_visitors=notify_visitors,
            notify_payments=notify_payments,
            language=language,
            theme=theme,
            default_building_id=kwargs.get("default_building_id"),
            notes=kwargs.get("notes"),
        )
        session.add(db_resident)
        session.flush()
        session.refresh(db_resident)
        return db_resident
