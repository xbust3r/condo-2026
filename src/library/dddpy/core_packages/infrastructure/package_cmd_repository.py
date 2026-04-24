"""Package Command Repository Implementation."""
from datetime import datetime
from typing import Optional

from library.dddpy.core_packages.domain.package_cmd_repository import PackageCmdRepository
from library.dddpy.core_packages.domain.package_entity import PackageEntity
from library.dddpy.core_packages.infrastructure.dbpackage import DBPackage
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("PackageCmdRepository")


class PackageCmdRepositoryImpl(PackageCmdRepository):

    def __init__(self):
        logger.info("PackageCmdRepositoryImpl initialized")

    def create(self, entity: PackageEntity) -> int:
        logger.info(
            f"Creating package condominium_id={entity.condominium_id}, "
            f"unit_id={entity.unit_id}, recipient_user_id={entity.recipient_user_id}"
        )
        with session_scope() as session:
            db_p = DBPackage(
                uuid=entity.uuid,
                condominium_id=entity.condominium_id,
                unit_id=entity.unit_id,
                recipient_user_id=entity.recipient_user_id,
                carrier=entity.carrier,
                tracking_number=entity.tracking_number,
                description=entity.description,
                status=entity.status,
                received_at=entity.received_at,
                delivered_at=entity.delivered_at,
                pickup_code=entity.pickup_code,
            )
            session.add(db_p)
            session.flush()
            session.refresh(db_p)
            logger.info(f"Package created id={db_p.id}")
            return db_p.id

    def update(self, entity: PackageEntity) -> bool:
        logger.info(f"Updating package id={entity.id}")
        with session_scope() as session:
            db_p = session.query(DBPackage).filter(
                DBPackage.id == entity.id,
                DBPackage.deleted_at.is_(None),
            ).first()
            if not db_p:
                return False
            if entity.carrier is not None:
                db_p.carrier = entity.carrier
            if entity.tracking_number is not None:
                db_p.tracking_number = entity.tracking_number
            if entity.description is not None:
                db_p.description = entity.description
            if entity.status is not None:
                db_p.status = entity.status
            if entity.received_at is not None:
                db_p.received_at = entity.received_at
            if entity.delivered_at is not None:
                db_p.delivered_at = entity.delivered_at
            if entity.pickup_code is not None:
                db_p.pickup_code = entity.pickup_code
            db_p.updated_at = datetime.utcnow()
            session.flush()
            logger.info(f"Package updated id={entity.id}")
            return True

    def soft_delete(self, id: int) -> bool:
        logger.info(f"Soft-deleting package id={id}")
        with session_scope() as session:
            db_p = session.query(DBPackage).filter(
                DBPackage.id == id,
                DBPackage.deleted_at.is_(None),
            ).first()
            if not db_p:
                return False
            db_p.deleted_at = datetime.utcnow()
            session.flush()
            logger.info(f"Package soft-deleted id={id}")
            return True

    def hard_delete(self, id: int) -> bool:
        logger.info(f"Hard-deleting package id={id}")
        with session_scope() as session:
            db_p = session.query(DBPackage).filter(
                DBPackage.id == id,
            ).first()
            if not db_p:
                return False
            session.delete(db_p)
            session.flush()
            logger.info(f"Package hard-deleted id={id}")
            return True
