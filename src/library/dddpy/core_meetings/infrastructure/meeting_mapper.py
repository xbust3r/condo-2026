"""
Meeting mapper — maps between DB model and domain entity.
"""
from library.dddpy.core_meetings.domain.meeting_entity import MeetingEntity
from library.dddpy.core_meetings.infrastructure.dbmeeting import DBMeeting


class MeetingMapper:

    @staticmethod
    def to_domain(db_row: DBMeeting) -> MeetingEntity:
        return MeetingEntity(
            id=db_row.id,
            uuid=db_row.uuid,
            condominium_id=db_row.condominium_id,
            meeting_type=db_row.meeting_type,
            title=db_row.title,
            description=db_row.description,
            meeting_date=db_row.meeting_date,
            location=db_row.location,
            status=db_row.status,
            approved_at=db_row.approved_at,
            created_by_user_id=db_row.created_by_user_id,
            created_at=db_row.created_at,
            updated_at=db_row.updated_at,
            deleted_at=db_row.deleted_at,
        )

    @staticmethod
    def to_domain_enriched(
        db_row: DBMeeting,
        condominium_name: str = None,
        created_by_name: str = None,
    ) -> MeetingEntity:
        entity = MeetingMapper.to_domain(db_row)
        entity.condominium_name = condominium_name
        entity.created_by_name = created_by_name
        return entity
