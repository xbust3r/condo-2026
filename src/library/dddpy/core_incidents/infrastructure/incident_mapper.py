"""
Incident mapper — maps between DB model and domain entity.
"""
import json
from library.dddpy.core_incidents.infrastructure.dbinicident import DBIncident
from library.dddpy.core_incidents.domain.incident_entity import IncidentEntity


class IncidentMapper:

    @staticmethod
    def _parse_photos(value) -> list:
        """Parse photos JSON field."""
        if value is None:
            return []
        if isinstance(value, list):
            return value
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return []

    @staticmethod
    def to_domain(db_incident: DBIncident) -> IncidentEntity:
        return IncidentEntity(
            id=db_incident.id,
            uuid=db_incident.uuid,
            condominium_id=db_incident.condominium_id,
            building_id=db_incident.building_id,
            unit_id=db_incident.unit_id,
            reported_by_user_id=db_incident.reported_by_user_id,
            assigned_to_user_id=db_incident.assigned_to_user_id,
            category=db_incident.category,
            priority=db_incident.priority,
            status=db_incident.status,
            title=db_incident.title,
            description=db_incident.description,
            photos=IncidentMapper._parse_photos(db_incident.photos),
            internal_notes=db_incident.internal_notes,
            resolution_notes=db_incident.resolution_notes,
            scheduled_date=db_incident.scheduled_date,
            completed_date=db_incident.completed_date,
            is_escalated=db_incident.is_escalated or False,
            created_at=db_incident.created_at,
            updated_at=db_incident.updated_at,
            deleted_at=db_incident.deleted_at,
        )

    @staticmethod
    def to_domain_enriched(
        db_incident: DBIncident,
        unit_code: str = None,
        building_name: str = None,
        condominium_name: str = None,
        reported_by_user_full_name: str = None,
        assigned_to_user_full_name: str = None,
    ) -> IncidentEntity:
        entity = IncidentMapper.to_domain(db_incident)
        entity.unit_code = unit_code
        entity.building_name = building_name
        entity.condominium_name = condominium_name
        entity.reported_by_user_full_name = reported_by_user_full_name
        entity.assigned_to_user_full_name = assigned_to_user_full_name
        return entity
