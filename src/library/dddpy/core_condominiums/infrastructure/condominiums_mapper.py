# Mapper for Condominium
from library.dddpy.core_condominiums.domain.condominiums import Condominium
from library.dddpy.core_condominiums.infrastructure.condominiums import DBCondominiums


class CondominiumMapper:
    
    @staticmethod
    def to_domain(db_condominium: DBCondominiums) -> Condominium:
        return Condominium(
            id=db_condominium.id,
            name=db_condominium.name,
            code=db_condominium.code,
            description=db_condominium.description,
            size=float(db_condominium.size) if db_condominium.size else None,
            percentage=float(db_condominium.percentage) if db_condominium.percentage else None,
            status=db_condominium.status,
            created_at=db_condominium.created_at,
            updated_at=db_condominium.updated_at,
        )

    @staticmethod
    def to_db(condominium: Condominium) -> DBCondominiums:
        return DBCondominiums(
            id=condominium.id,
            name=condominium.name,
            code=condominium.code,
            description=condominium.description,
            size=condominium.size,
            percentage=condominium.percentage,
            status=condominium.status,
            created_at=condominium.created_at,
            updated_at=condominium.updated_at,
        )
