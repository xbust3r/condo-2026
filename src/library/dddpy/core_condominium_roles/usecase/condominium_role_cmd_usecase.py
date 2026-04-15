from typing import Optional
from datetime import date

from library.dddpy.core_condominium_roles.usecase.condominium_role_cmd_schema import (
    CreateCondominiumRoleSchema,
    UpdateCondominiumRoleSchema,
)
from library.dddpy.core_condominium_roles.domain.condominium_role_cmd_repository import CondominiumRoleCmdRepository
from library.dddpy.core_condominium_roles.domain.condominium_role_entity import CondominiumRoleEntity
from library.dddpy.core_condominium_roles.domain.condominium_role_data import CreateCondominiumRoleData, UpdateCondominiumRoleData
from library.dddpy.core_condominium_roles.domain.condominium_role_exception import (
    CondominiumNotFoundForRole,
    UserNotFoundForRole,
    RoleIsSystem,
)
from library.dddpy.shared.logging.logging import Logger


logger = Logger("CondominiumRoleCmdUseCase")


class CondominiumRoleCmdUseCase:

    SYSTEM_ROLES = {"super_admin"}

    def __init__(self, repository: CondominiumRoleCmdRepository):
        self.repository = repository
        logger.info("CondominiumRoleCmdUseCase initialized")

    def _validate_condominium(self, condominium_id: int) -> None:
        """Validate condominium exists and is active."""
        try:
            from library.dddpy.core_condominiums.usecase.condominium_usecase import (
                CondominiumUseCase,
            )
            CondominiumUseCase().get_by_id(condominium_id)
        except Exception:
            raise CondominiumNotFoundForRole()

    def _validate_user(self, user_id: int) -> None:
        """Validate user exists."""
        try:
            from library.dddpy.core_users.usecase.user_usecase import UserUseCase
            UserUseCase().get_by_id(user_id)
        except Exception:
            raise UserNotFoundForRole()

    def create(self, schema: CreateCondominiumRoleSchema) -> CondominiumRoleEntity:
        logger.info(
            f"Delegating condominium role creation for user_id={schema.user_id}, "
            f"condominium_id={schema.condominium_id}, role={schema.role}"
        )
        self._validate_condominium(schema.condominium_id)
        self._validate_user(schema.user_id)

        data = CreateCondominiumRoleData(
            condominium_id=schema.condominium_id,
            user_id=schema.user_id,
            role=schema.role,
            status=schema.status,
            start_date=schema.start_date,
            end_date=schema.end_date,
        )
        return self.repository.create(data)

    def update(self, id: int, schema: UpdateCondominiumRoleSchema) -> Optional[CondominiumRoleEntity]:
        logger.info(f"Delegating condominium role update for id={id}")

        data = UpdateCondominiumRoleData(
            role=schema.role,
            status=schema.status,
            end_date=schema.end_date,
        )
        return self.repository.update(id, data)

    def soft_delete(self, id: int) -> bool:
        logger.info(f"Delegating condominium role soft delete for id={id}")
        return self.repository.soft_delete(id)

    def restore(self, id: int) -> bool:
        logger.info(f"Delegating condominium role restore for id={id}")
        return self.repository.restore(id)

    def hard_delete(self, id: int) -> bool:
        logger.info(f"Delegating condominium role hard delete for id={id}")
        return self.repository.hard_delete(id)
