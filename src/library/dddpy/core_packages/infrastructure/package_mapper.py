"""Package mapper — maps between DB model and domain entity."""
from library.dddpy.core_packages.domain.package_entity import PackageEntity
from library.dddpy.core_packages.infrastructure.dbpackage import DBPackage


class PackageMapper:

    @staticmethod
    def to_domain(row: DBPackage) -> PackageEntity:
        return PackageEntity(
            id=row.id,
            uuid=row.uuid,
            condominium_id=row.condominium_id,
            unit_id=row.unit_id,
            recipient_user_id=row.recipient_user_id,
            carrier=row.carrier,
            tracking_number=row.tracking_number,
            description=row.description,
            status=row.status,
            received_at=row.received_at,
            delivered_at=row.delivered_at,
            pickup_code=row.pickup_code,
            created_at=row.created_at,
            updated_at=row.updated_at,
            deleted_at=row.deleted_at,
        )

    @staticmethod
    def to_domain_enriched(
        row: DBPackage,
        recipient_name: str = None,
        unit_code: str = None,
        building_name: str = None,
        condominium_name: str = None,
    ) -> PackageEntity:
        entity = PackageMapper.to_domain(row)
        entity.recipient_name = recipient_name
        entity.unit_code = unit_code
        entity.building_name = building_name
        entity.condominium_name = condominium_name
        return entity
