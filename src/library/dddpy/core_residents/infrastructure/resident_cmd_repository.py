"""
Resident profile command repository implementation.
"""
import uuid as uuid_lib
from datetime import datetime
from typing import Optional

from library.dddpy.core_residents.domain.resident_cmd_repository import ResidentProfileCmdRepository
from library.dddpy.core_residents.domain.resident_profile_entity import ResidentProfileEntity
from library.dddpy.core_residents.infrastructure.dbresident import DBResidentProfile
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("ResidentProfileCmdRepository")


class ResidentProfileCmdRepositoryImpl(ResidentProfileCmdRepository):

    def create_or_update(self, entity: ResidentProfileEntity) -> int:
        logger.info(f"Upserting resident profile user_id={entity.user_id}, condo={entity.condominium_id}")
        with session_scope() as session:
            existing = session.query(DBResidentProfile).filter(
                DBResidentProfile.user_id == entity.user_id,
                DBResidentProfile.condominium_id == entity.condominium_id,
                DBResidentProfile.deleted_at.is_(None),
            ).first()

            if existing:
                existing.notify_announcements = entity.notify_announcements
                existing.notify_incidents = entity.notify_incidents
                existing.notify_packages = entity.notify_packages
                existing.notify_visitors = entity.notify_visitors
                existing.notify_payments = entity.notify_payments
                existing.language = entity.language
                existing.theme = entity.theme
                existing.default_building_id = entity.default_building_id
                existing.notes = entity.notes
                existing.updated_at = datetime.utcnow()
                session.flush()
                logger.info(f"Resident profile updated id={existing.id}")
                return existing.id
            else:
                db_p = DBResidentProfile(
                    uuid=str(uuid_lib.uuid4()),
                    user_id=entity.user_id,
                    condominium_id=entity.condominium_id,
                    notify_announcements=entity.notify_announcements,
                    notify_incidents=entity.notify_incidents,
                    notify_packages=entity.notify_packages,
                    notify_visitors=entity.notify_visitors,
                    notify_payments=entity.notify_payments,
                    language=entity.language,
                    theme=entity.theme,
                    default_building_id=entity.default_building_id,
                    notes=entity.notes,
                )
                session.add(db_p)
                session.flush()
                session.refresh(db_p)
                logger.info(f"Resident profile created id={db_p.id}")
                return db_p.id

    def update_preferences(
        self,
        user_id: int,
        condominium_id: int,
        preferences: dict,
    ) -> bool:
        logger.info(f"Updating preferences user_id={user_id}, condo={condominium_id}")
        with session_scope() as session:
            db_p = session.query(DBResidentProfile).filter(
                DBResidentProfile.user_id == user_id,
                DBResidentProfile.condominium_id == condominium_id,
                DBResidentProfile.deleted_at.is_(None),
            ).first()
            if not db_p:
                return False
            for key, value in preferences.items():
                if hasattr(db_p, key):
                    setattr(db_p, key, value)
            db_p.updated_at = datetime.utcnow()
            session.flush()
            return True

    def soft_delete(self, id: int) -> bool:
        logger.info(f"Soft-deleting resident profile id={id}")
        with session_scope() as session:
            db_p = session.query(DBResidentProfile).filter(
                DBResidentProfile.id == id,
                DBResidentProfile.deleted_at.is_(None),
            ).first()
            if not db_p:
                return False
            db_p.deleted_at = datetime.utcnow()
            session.flush()
            return True
