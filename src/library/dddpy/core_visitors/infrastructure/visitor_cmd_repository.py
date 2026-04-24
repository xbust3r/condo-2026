"""
from typing import Optional
Visitor command repository implementation — write operations.
"""
from datetime import datetime
import uuid as uuid_lib
from typing import Optional

from library.dddpy.core_visitors.domain.visitor_entity import VisitorEntity
from library.dddpy.core_visitors.domain.visitor_repository import VisitorRepository
from library.dddpy.core_visitors.infrastructure.dbvisitor import DBVisitor
from library.dddpy.core_visitors.infrastructure.visitor_mapper import VisitorMapper
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("VisitorCmdRepository")


class VisitorCmdRepositoryImpl(VisitorRepository):

    def __init__(self):
        logger.info("VisitorCmdRepositoryImpl initialized")

    def create(self, entity: VisitorEntity) -> VisitorEntity:
        logger.info(
            f"Creating visitor name='{entity.visitor_name}', "
            f"condominium_id={entity.condominium_id}, unit_id={entity.unit_id}"
        )
        with session_scope() as session:
            db_visitor = DBVisitor(
                uuid=str(uuid_lib.uuid4()),
                condominium_id=entity.condominium_id,
                building_id=entity.building_id,
                unit_id=entity.unit_id,
                host_user_id=entity.host_user_id,
                visitor_name=entity.visitor_name,
                visitor_document_type=entity.visitor_document_type,
                visitor_document_number=entity.visitor_document_number,
                visitor_phone=entity.visitor_phone,
                expected_date=entity.expected_date,
                expected_time=entity.expected_time,
                actual_checkin_at=entity.actual_checkin_at,
                actual_checkout_at=entity.actual_checkout_at,
                status=entity.status,
                visit_purpose=entity.visit_purpose,
                access_code=entity.access_code,
                notes=entity.notes,
            )
            session.add(db_visitor)
            session.flush()
            session.refresh(db_visitor)
            logger.info(f"Visitor created with id={db_visitor.id}")
            return VisitorMapper.to_domain(db_visitor)

    def update(self, id: int, entity: VisitorEntity) -> Optional[VisitorEntity]:
        logger.info(f"Updating visitor id={id}")
        with session_scope() as session:
            db_visitor = session.query(DBVisitor).filter(DBVisitor.id == id).first()
            if not db_visitor:
                logger.warning(f"Visitor not found for update id={id}")
                return None

            db_visitor.building_id = entity.building_id
            db_visitor.visitor_name = entity.visitor_name
            db_visitor.visitor_document_type = entity.visitor_document_type
            db_visitor.visitor_document_number = entity.visitor_document_number
            db_visitor.visitor_phone = entity.visitor_phone
            db_visitor.expected_date = entity.expected_date
            db_visitor.expected_time = entity.expected_time
            db_visitor.actual_checkin_at = entity.actual_checkin_at
            db_visitor.actual_checkout_at = entity.actual_checkout_at
            db_visitor.status = entity.status
            db_visitor.visit_purpose = entity.visit_purpose
            db_visitor.access_code = entity.access_code
            db_visitor.notes = entity.notes

            session.flush()
            session.refresh(db_visitor)
            logger.info(f"Visitor updated id={id}")
            return VisitorMapper.to_domain(db_visitor)

    def delete(self, id: int) -> bool:
        """Soft delete: sets deleted_at timestamp."""
        logger.info(f"Soft deleting visitor id={id}")
        with session_scope() as session:
            db_visitor = session.query(DBVisitor).filter(DBVisitor.id == id).first()
            if not db_visitor:
                logger.warning(f"Visitor not found for soft delete id={id}")
                return False
            db_visitor.deleted_at = datetime.utcnow()
            session.flush()
            logger.info(f"Visitor soft deleted id={id}")
            return True

    def hard_delete(self, id: int) -> bool:
        """Physical delete."""
        logger.info(f"Hard deleting visitor id={id}")
        with session_scope() as session:
            db_visitor = session.query(DBVisitor).filter(DBVisitor.id == id).first()
            if not db_visitor:
                logger.warning(f"Visitor not found for hard delete id={id}")
                return False
            session.delete(db_visitor)
            session.flush()
            logger.info(f"Visitor hard deleted id={id}")
            return True

    def restore(self, id: int) -> bool:
        """Restore a soft-deleted record: clears deleted_at."""
        logger.info(f"Restoring visitor id={id}")
        with session_scope() as session:
            db_visitor = session.query(DBVisitor).filter(DBVisitor.id == id).first()
            if not db_visitor:
                logger.warning(f"Visitor not found for restore id={id}")
                return False
            db_visitor.deleted_at = None
            session.flush()
            logger.info(f"Visitor restored id={id}")
            return True

    def _get_by_id_any_status(self, id: int) -> Optional[VisitorEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        logger.debug(f"Fetching visitor by id={id} (any status)")
        with session_scope() as session:
            db_visitor = (
                session.query(DBVisitor)
                .filter(DBVisitor.id == id)
                .first()
            )
            if not db_visitor:
                return None
            return VisitorMapper.to_domain(db_visitor)