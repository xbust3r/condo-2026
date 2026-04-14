"""
UnityType Mapper — transforms between DB model and Domain entity.
"""
from library.dddpy.core_unities_types.infrastructure.dbunitytype import DBUnityType
from library.dddpy.core_unities_types.domain.unity_type_entity import UnityTypeEntity


class UnityTypeMapper:
    """Mapper para convertir entre DBUnityType y UnityTypeEntity."""

    @staticmethod
    def to_domain(db_type: DBUnityType) -> UnityTypeEntity:
        return UnityTypeEntity(
            id=db_type.id,
            uuid=db_type.uuid,
            code=db_type.code,
            name=db_type.name,
            description=db_type.description,
            condominium_id=db_type.condominium_id,
            is_system=bool(db_type.is_system),
            sort_order=db_type.sort_order,
            usage_class=db_type.usage_class,
            status=db_type.status,
            created_at=db_type.created_at,
            updated_at=db_type.updated_at,
            deleted_at=db_type.deleted_at,
        )

    @staticmethod
    def to_infrastructure(entity: UnityTypeEntity) -> DBUnityType:
        return DBUnityType(
            id=entity.id,
            uuid=entity.uuid,
            code=entity.code,
            name=entity.name,
            description=entity.description,
            condominium_id=entity.condominium_id,
            is_system=int(entity.is_system),
            sort_order=entity.sort_order,
            usage_class=entity.usage_class,
            status=entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )
