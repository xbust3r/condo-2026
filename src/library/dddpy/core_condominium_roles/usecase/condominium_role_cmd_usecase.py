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
    DuplicateRoleAssignment,
)
from library.dddpy.shared.logging.logging import Logger


logger = Logger("CondominiumRoleCmdUseCase")


class CondominiumRoleCmdUseCase:

    # RBAC-02: super_admin no es asignable via API — solo seed de DB
    SYSTEM_ROLES = {"super_admin"}

    # RBAC-01: condominium_admin es 1 por condominio (activo)
    ADMIN_ROLE = "condominium_admin"

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

    def _check_condominium_admin_unique(
        self, condominium_id: int, exclude_id: Optional[int] = None
    ) -> None:
        """
        RBAC-01: Verify no other active condominium_admin exists in this condominium.

        Raises DuplicateRoleAssignment if another active admin is found.
        """
        from library.dddpy.core_condominium_roles.infrastructure.condominium_role_query_repository import (
            CondominiumRoleQueryRepositoryImpl,
        )
        repo = CondominiumRoleQueryRepositoryImpl()
        roles, total = repo.list_by_condominium(
            condominium_id=condominium_id,
            role=self.ADMIN_ROLE,
            status="active",
            include_deleted=False,
        )
        for r in roles:
            if exclude_id is None or r.id != exclude_id:
                raise DuplicateRoleAssignment(
                    f"Ya existe un condominium_admin activo en este condominio (id={r.id}). "
                    f"Solo puede haber 1 condominium_admin por condominio."
                )

    def create(self, schema: CreateCondominiumRoleSchema) -> CondominiumRoleEntity:
        logger.info(
            f"Delegating condominium role creation for user_id={schema.user_id}, "
            f"condominium_id={schema.condominium_id}, role={schema.role}"
        )

        # RBAC-02: super_admin no asignable por API
        if schema.role in self.SYSTEM_ROLES:
            logger.warning(f"Attempt to create system role via API: {schema.role}")
            raise RoleIsSystem()

        # RBAC-01: condominium_admin unique por condominio
        if schema.role == self.ADMIN_ROLE:
            self._check_condominium_admin_unique(schema.condominium_id)

        self._validate_condominium(schema.condominium_id)
        self._validate_user(schema.user_id)

        data = CreateCondominiumRoleData(
            condominium_id=schema.condominium_id,
            user_id=schema.user_id,
            role=schema.role,
            status=schema.status,
            scope=schema.scope,
            building_id=schema.building_id,
            unit_id=schema.unit_id,
            start_date=schema.start_date,
            end_date=schema.end_date,
        )
        return self.repository.create(data)

    def update(
        self, id: int, schema: UpdateCondominiumRoleSchema
    ) -> Optional[CondominiumRoleEntity]:
        logger.info(f"Delegating condominium role update for id={id}")

        # Si se está cambiando el rol, validar
        target_role = schema.role

        if target_role:
            # RBAC-02: super_admin no asignable por API
            if target_role in self.SYSTEM_ROLES:
                logger.warning(f"Attempt to assign system role via API: {target_role}")
                raise RoleIsSystem()

            # RBAC-01: condominium_admin unique por condominio
            if target_role == self.ADMIN_ROLE:
                # Necesitamos saber el condominium_id actual para el unique check
                from library.dddpy.core_condominium_roles.infrastructure.condominium_role_query_repository import (
                    CondominiumRoleQueryRepositoryImpl,
                )
                existing = CondominiumRoleQueryRepositoryImpl().get_by_id(id)
                if existing and existing.condominium_id:
                    self._check_condominium_admin_unique(
                        existing.condominium_id, exclude_id=id
                    )

        data = UpdateCondominiumRoleData(
            role=schema.role,
            status=schema.status,
            scope=schema.scope,
            building_id=schema.building_id,
            unit_id=schema.unit_id,
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
