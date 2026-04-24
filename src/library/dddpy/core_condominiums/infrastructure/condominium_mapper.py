"""
Condominium Mapper - Transforma entre DB y Domain.
"""
from library.dddpy.core_condominiums.infrastructure.dbcondominiums import DBCondominiums
from library.dddpy.core_condominiums.domain.condominium_entity import CondominiumEntity


class CondominiumMapper:
    """Mapper para convertir entre DBCondominiums y CondominiumEntity."""

    @staticmethod
    def to_domain(db_condominium: DBCondominiums) -> CondominiumEntity:
        """Convierte modelo DB a entidad de dominio."""
        return CondominiumEntity(
            id=db_condominium.id,
            uuid=db_condominium.uuid,
            code=db_condominium.code,
            name=db_condominium.name,
            description=db_condominium.description,
            land_area=db_condominium.land_area,
            built_area=db_condominium.built_area,
            area_unit=db_condominium.area_unit,
            legal_name=db_condominium.legal_name,
            document_number=db_condominium.document_number,
            address=db_condominium.address,
            city=db_condominium.city,
            country=db_condominium.country,
            contact_email=db_condominium.contact_email,
            contact_phone=db_condominium.contact_phone,
            status=db_condominium.status,
            theme_id=db_condominium.theme_id,
            created_at=db_condominium.created_at,
            updated_at=db_condominium.updated_at,
            deleted_at=db_condominium.deleted_at,
        )

    @staticmethod
    def to_infrastructure(condominium: CondominiumEntity) -> DBCondominiums:
        """Convierte entidad de dominio a modelo DB."""
        return DBCondominiums(
            id=condominium.id,
            uuid=condominium.uuid,
            code=condominium.code,
            name=condominium.name,
            description=condominium.description,
            land_area=condominium.land_area,
            built_area=condominium.built_area,
            area_unit=condominium.area_unit,
            legal_name=condominium.legal_name,
            document_number=condominium.document_number,
            address=condominium.address,
            city=condominium.city,
            country=condominium.country,
            contact_email=condominium.contact_email,
            contact_phone=condominium.contact_phone,
            status=condominium.status,
            theme_id=condominium.theme_id,
            created_at=condominium.created_at,
            updated_at=condominium.updated_at,
            deleted_at=condominium.deleted_at,
        )
