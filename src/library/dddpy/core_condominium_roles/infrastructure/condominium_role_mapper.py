"""
Condominium Role Mapper - Transforma entre DB model y Domain entity.

v2 — incluye scope y building_id desde migración 021.
"""
from library.dddpy.core_condominium_roles.infrastructure.dbcondominium_role import DBCondominiumRoles
from library.dddpy.core_condominium_roles.domain.condominium_role_entity import CondominiumRoleEntity


class CondominiumRoleMapper:
    """Mapper para convertir entre DBCondominiumRoles y CondominiumRoleEntity."""

    @staticmethod
    def to_domain(db_role: DBCondominiumRoles) -> CondominiumRoleEntity:
        """Convierte modelo DB a entidad de dominio."""
        return CondominiumRoleEntity(
            id=db_role.id,
            uuid=db_role.uuid,
            condominium_id=db_role.condominium_id,
            user_id=db_role.user_id,
            role=db_role.role,
            status=db_role.status,
            scope=db_role.scope,
            building_id=db_role.building_id,
            start_date=db_role.start_date,
            end_date=db_role.end_date,
            created_at=db_role.created_at,
            updated_at=db_role.updated_at,
            deleted_at=db_role.deleted_at,
        )

    @staticmethod
    def to_infrastructure(entity: CondominiumRoleEntity) -> DBCondominiumRoles:
        """Convierte entidad de dominio a modelo DB."""
        return DBCondominiumRoles(
            id=entity.id,
            uuid=entity.uuid,
            condominium_id=entity.condominium_id,
            user_id=entity.user_id,
            role=entity.role,
            status=entity.status,
            scope=entity.scope,
            building_id=entity.building_id,
            start_date=entity.start_date,
            end_date=entity.end_date,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )
