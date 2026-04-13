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
            size=db_condominium.size,
            percentage=db_condominium.percentage,
            status=db_condominium.status,
            created_at=db_condominium.created_at,
            updated_at=db_condominium.updated_at,
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
            size=condominium.size,
            percentage=condominium.percentage,
            status=condominium.status,
            created_at=condominium.created_at,
            updated_at=condominium.updated_at,
        )