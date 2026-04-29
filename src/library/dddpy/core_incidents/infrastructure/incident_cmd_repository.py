from typing import Optional

"""Incident command repository implementation — write operations."""
from datetime import datetime
import uuid as uuid_lib
import json

from library.dddpy.core_incidents.domain.incident_entity import IncidentEntity
from library.dddpy.core_incidents.domain.incident_repository import IncidentRepository
from library.dddpy.core_incidents.infrastructure.dbinicident import DBIncident
from library.dddpy.core_incidents.infrastructure.incident_mapper import IncidentMapper
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("IncidentCmdRepository")


class IncidentCmdRepositoryImpl(IncidentRepository):

    def __init__(self):
        logger.info("IncidentCmdRepositoryImpl initialized")

    def create(self, entity: IncidentEntity) -> IncidentEntity:
        logger.info(
            f"Creating incident title='{entity.title}', "
            f"condominium_id={entity.condominium_id}, unit_id={entity.unit_id}"
        )
        with session_scope() as session:
            db_incident = DBIncident(
                uuid=str(uuid_lib.uuid4()),
                condominium_id=entity.condominium_id,
                building_id=entity.building_id,
                unit_id=entity.unit_id,
                reported_by_user_id=entity.reported_by_user_id,
                assigned_to_user_id=entity.assigned_to_user_id,
                category=entity.category,
                priority=entity.priority,
                status=entity.status,
                title=entity.title,
                description=entity.description,
                photos=json.dumps(entity.photos) if entity.photos else None,
                internal_notes=entity.internal_notes,
                resolution_notes=entity.resolution_notes,
                scheduled_date=entity.scheduled_date,
                completed_date=entity.completed_date,
                is_escalated=entity.is_escalated,
            )
            session.add(db_incident)
            session.flush()
            session.refresh(db_incident)
            logger.info(f"Incident created with id={db_incident.id}")
            return IncidentMapper.to_domain(db_incident)

    def update(self, id: int, entity: IncidentEntity) -> IncidentEntity:
        logger.info(f"Updating incident id={id}")
        with session_scope() as session:
            db_incident = session.query(DBIncident).filter(DBIncident.id == id).first()
            if not db_incident:
                logger.warning(f"Incident not found for update id={id}")
                return None

            db_incident.building_id = entity.building_id
            db_incident.unit_id = entity.unit_id
            db_incident.assigned_to_user_id = entity.assigned_to_user_id
            db_incident.category = entity.category
            db_incident.priority = entity.priority
            db_incident.status = entity.status
            db_incident.title = entity.title
            db_incident.description = entity.description
            db_incident.photos = json.dumps(entity.photos) if entity.photos else None
            db_incident.internal_notes = entity.internal_notes
            db_incident.resolution_notes = entity.resolution_notes
            db_incident.scheduled_date = entity.scheduled_date
            db_incident.completed_date = entity.completed_date
            db_incident.is_escalated = entity.is_escalated

            session.flush()
            session.refresh(db_incident)
            logger.info(f"Incident updated id={id}")
            return IncidentMapper.to_domain(db_incident)

    def delete(self, id: int) -> bool:
        """Soft delete: sets deleted_at timestamp."""
        logger.info(f"Soft deleting incident id={id}")
        with session_scope() as session:
            db_incident = session.query(DBIncident).filter(DBIncident.id == id).first()
            if not db_incident:
                logger.warning(f"Incident not found for soft delete id={id}")
                return False
            db_incident.deleted_at = datetime.utcnow()
            session.flush()
            logger.info(f"Incident soft deleted id={id}")
            return True

    def hard_delete(self, id: int) -> bool:
        """Physical delete."""
        logger.info(f"Hard deleting incident id={id}")
        with session_scope() as session:
            db_incident = session.query(DBIncident).filter(DBIncident.id == id).first()
            if not db_incident:
                logger.warning(f"Incident not found for hard delete id={id}")
                return False
            session.delete(db_incident)
            session.flush()
            logger.info(f"Incident hard deleted id={id}")
            return True

    def restore(self, id: int) -> bool:
        """Restore a soft-deleted record: clears deleted_at."""
        logger.info(f"Restoring incident id={id}")
        with session_scope() as session:
            db_incident = session.query(DBIncident).filter(DBIncident.id == id).first()
            if not db_incident:
                logger.warning(f"Incident not found for restore id={id}")
                return False
            db_incident.deleted_at = None
            session.flush()
            logger.info(f"Incident restored id={id}")
            return True

    def _get_by_id_any_status(self, id: int) -> Optional[IncidentEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        logger.debug(f"Fetching incident by id={id} (any status)")
        with session_scope() as session:
            db_incident = (
                session.query(DBIncident)
                .filter(DBIncident.id == id)
                .first()
            )
            if not db_incident:
                return None
            return IncidentMapper.to_domain(db_incident)
