"""
Announcement mapper — maps between DB model and domain entity.
"""
from library.dddpy.core_announcements.domain.announcement_entity import AnnouncementEntity
from library.dddpy.core_announcements.infrastructure.dbannouncement import DBAnnouncement


class AnnouncementMapper:

    @staticmethod
    def to_domain(db_row: DBAnnouncement) -> AnnouncementEntity:
        return AnnouncementEntity(
            id=db_row.id,
            uuid=db_row.uuid,
            condominium_id=db_row.condominium_id,
            author_user_id=db_row.author_user_id,
            title=db_row.title,
            content=db_row.content,
            category=db_row.category,
            visibility=db_row.visibility,
            is_pinned=db_row.is_pinned or False,
            published_at=db_row.published_at,
            expires_at=db_row.expires_at,
            created_at=db_row.created_at,
            updated_at=db_row.updated_at,
            deleted_at=db_row.deleted_at,
        )

    @staticmethod
    def to_domain_enriched(
        db_row: DBAnnouncement,
        author_name: str = None,
        condominium_name: str = None,
    ) -> AnnouncementEntity:
        entity = AnnouncementMapper.to_domain(db_row)
        entity.author_name = author_name
        entity.condominium_name = condominium_name
        return entity
