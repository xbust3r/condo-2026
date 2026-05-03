"""
Amenity mapper — maps between DB model and domain entity.

Now supports scope + building_id enrichment.
"""
from typing import Optional

from library.dddpy.core_amenities.domain.amenity_entity import AmenityEntity
from library.dddpy.core_amenities.infrastructure.dbamenity import DBAmenity


class AmenityMapper:

    @staticmethod
    def to_domain(db_row: DBAmenity) -> AmenityEntity:
        return AmenityEntity(
            id=db_row.id,
            uuid=db_row.uuid,
            condominium_id=db_row.condominium_id,
            name=db_row.name,
            description=db_row.description,
            location=db_row.location,
            max_capacity=db_row.max_capacity or 1,
            booking_duration_min=db_row.booking_duration_min or 60,
            requires_approval=db_row.requires_approval or False,
            scope=db_row.scope or 'CONDOMINIUM',
            building_id=db_row.building_id,
            booking_price=float(db_row.booking_price or 0),
            security_deposit_amount=float(db_row.security_deposit_amount or 0),
            is_reservable=bool(db_row.is_reservable or False),
            status=db_row.status or 'active',
            created_at=db_row.created_at,
            updated_at=db_row.updated_at,
            deleted_at=db_row.deleted_at,
        )

    @staticmethod
    def to_domain_enriched(
        db_row: DBAmenity,
        condominium_name: Optional[str] = None,
        building_name: Optional[str] = None,
    ) -> AmenityEntity:
        entity = AmenityMapper.to_domain(db_row)
        entity.condominium_name = condominium_name
        entity.building_name = building_name
        return entity
