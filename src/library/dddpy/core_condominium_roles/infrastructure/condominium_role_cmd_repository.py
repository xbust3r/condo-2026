from typing import Optional
from datetime import datetime, date
import uuid as uuid_lib
from sqlalchemy.exc import IntegrityError

from library.dddpy.core_condominium_roles.domain.condominium_role_entity import CondominiumRoleEntity
from library.dddpy.core_condominium_roles.domain.condominium_role_data import CreateCondominiumRoleData, UpdateCondominiumRoleData
from library.dddpy.core_condominium_roles.domain.condominium_role_cmd_repository import CondominiumRoleCmdRepository
from library.dddpy.core_condominium_roles.infrastructure.dbcondominium_role import DBCondominiumRoles
from library.dddpy.core_condominium_roles.infrastructure.condominium_role_mapper import CondominiumRoleMapper
from library.dddpy.core_condominium_roles.domain.condominium_role_exception import (
    DuplicateRoleAssignment,
)
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("CondominiumRoleCmdRepository")


class CondominiumRoleCmdRepositoryImpl(CondominiumRoleCmdRepository):

    def __init__(self):
        logger.info("CondominiumRoleCmdRepositoryImpl initialized")

    def create(self, data: CreateCondominiumRoleData) -> CondominiumRoleEntity:
        logger.info(
            f"Creating condominium role for user_id={data.user_id}, "
            f"condominium_id={data.condominium_id}, role={data.role}"
        )
        try:
            with session_scope() as session:
                db_role = DBCondominiumRoles(
                    uuid=str(uuid_lib.uuid4()),
                    condominium_id=data.condominium_id,
                    user_id=data.user_id,
                    role=data.role,
                    status=data.status,
                    scope=data.scope,
                    building_id=data.building_id,
                    start_date=data.start_date,
                    end_date=data.end_date,
                )
                session.add(db_role)
                session.flush()
                session.refresh(db_role)
                logger.info(f"Condominium role created with id={db_role.id}")
                return CondominiumRoleMapper.to_domain(db_role)
        except IntegrityError as e:
            error_str = str(e).lower()
            if "fk_condominium_roles_condominium" in error_str:
                logger.warning(f"Condominium not found id={data.condominium_id}")
                from library.dddpy.core_condominium_roles.domain.condominium_role_exception import (
                    CondominiumNotFoundForRole,
                )
                raise CondominiumNotFoundForRole()
            if "fk_condominium_roles_user" in error_str:
                logger.warning(f"User not found id={data.user_id}")
                from library.dddpy.core_condominium_roles.domain.condominium_role_exception import (
                    UserNotFoundForRole,
                )
                raise UserNotFoundForRole()
            logger.error(f"Unexpected IntegrityError creating condominium role: {e}")
            raise

    def update(self, id: int, data: UpdateCondominiumRoleData) -> Optional[CondominiumRoleEntity]:
        logger.info(f"Updating condominium role id={id}")
        try:
            with session_scope() as session:
                db_role = session.query(DBCondominiumRoles).filter(DBCondominiumRoles.id == id).first()
                if not db_role:
                    logger.warning(f"Condominium role not found for update id={id}")
                    return None

                if data.role is not None:
                    db_role.role = data.role
                if data.status is not None:
                    db_role.status = data.status
                if data.scope is not None:
                    db_role.scope = data.scope
                if data.building_id is not None:
                    db_role.building_id = data.building_id
                if data.end_date is not None:
                    db_role.end_date = data.end_date

                session.flush()
                session.refresh(db_role)
                logger.info(f"Condominium role updated id={id}")
                return CondominiumRoleMapper.to_domain(db_role)
        except IntegrityError as e:
            logger.error(f"Unexpected IntegrityError updating condominium role id={id}: {e}")
            raise

    def soft_delete(self, id: int) -> bool:
        logger.info(f"Soft deleting condominium role id={id}")
        with session_scope() as session:
            db_role = session.query(DBCondominiumRoles).filter(DBCondominiumRoles.id == id).first()
            if not db_role:
                logger.warning(f"Condominium role not found for soft delete id={id}")
                return False
            db_role.deleted_at = datetime.utcnow()
            session.flush()
            logger.info(f"Condominium role soft deleted id={id}")
            return True

    def restore(self, id: int) -> bool:
        logger.info(f"Restoring condominium role id={id}")
        with session_scope() as session:
            db_role = session.query(DBCondominiumRoles).filter(DBCondominiumRoles.id == id).first()
            if not db_role:
                logger.warning(f"Condominium role not found for restore id={id}")
                return False
            db_role.deleted_at = None
            session.flush()
            logger.info(f"Condominium role restored id={id}")
            return True

    def hard_delete(self, id: int) -> bool:
        logger.info(f"Hard deleting condominium role id={id}")
        with session_scope() as session:
            db_role = session.query(DBCondominiumRoles).filter(DBCondominiumRoles.id == id).first()
            if not db_role:
                logger.warning(f"Condominium role not found for hard delete id={id}")
                return False
            session.delete(db_role)
            session.flush()
            logger.info(f"Condominium role hard deleted id={id}")
            return True

    def soft_delete_by_user(self, user_id: int) -> int:
        """Soft-delete all active roles for a user. Returns count of affected rows."""
        logger.info(f"Cascade soft-delete roles for user_id={user_id}")
        count = 0
        with session_scope() as session:
            rows = (
                session.query(DBCondominiumRoles)
                .filter(
                    DBCondominiumRoles.user_id == user_id,
                    DBCondominiumRoles.deleted_at.is_(None),
                )
                .all()
            )
            for row in rows:
                row.deleted_at = datetime.utcnow()
                count += 1
            session.flush()
            logger.info(f"Cascade: {count} roles soft-deleted for user_id={user_id}")
            return count
