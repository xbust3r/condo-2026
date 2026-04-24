"""
Resident profile mapper.
"""
from library.dddpy.core_residents.domain.resident_profile_entity import ResidentProfileEntity
from library.dddpy.core_residents.infrastructure.dbresident import DBResidentProfile


class ResidentMapper:

    @staticmethod
    def to_domain(row: DBResidentProfile) -> ResidentProfileEntity:
        return ResidentProfileEntity(
            id=row.id,
            uuid=row.uuid,
            user_id=row.user_id,
            condominium_id=row.condominium_id,
            notify_announcements=row.notify_announcements or True,
            notify_incidents=row.notify_incidents or True,
            notify_packages=row.notify_packages or True,
            notify_visitors=row.notify_visitors or True,
            notify_payments=row.notify_payments or True,
            language=row.language or 'es',
            theme=row.theme or 'light',
            default_building_id=row.default_building_id,
            notes=row.notes,
            created_at=row.created_at,
            updated_at=row.updated_at,
            deleted_at=row.deleted_at,
        )

    @staticmethod
    def to_domain_enriched(
        row: DBResidentProfile,
        user_full_name: str = None,
        condominium_name: str = None,
    ) -> ResidentProfileEntity:
        entity = ResidentMapper.to_domain(row)
        entity.user_full_name = user_full_name
        entity.condominium_name = condominium_name
        return entity
