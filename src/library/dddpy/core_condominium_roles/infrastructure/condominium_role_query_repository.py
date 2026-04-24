from typing import Optional
from typing import Optional, List, Tuple
from sqlalchemy import and_, text

from library.dddpy.core_condominium_roles.domain.condominium_role_entity import CondominiumRoleEntity
from library.dddpy.core_condominium_roles.domain.condominium_role_query_repository import CondominiumRoleQueryRepository
from library.dddpy.core_condominium_roles.infrastructure.dbcondominium_role import DBCondominiumRoles
from library.dddpy.core_condominium_roles.infrastructure.condominium_role_mapper import CondominiumRoleMapper
from library.dddpy.core_condominiums.infrastructure.dbcondominiums import DBCondominiums
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("CondominiumRoleQueryRepository")


class CondominiumRoleQueryRepositoryImpl(CondominiumRoleQueryRepository):

    def __init__(self):
        logger.info("CondominiumRoleQueryRepositoryImpl initialized")

    def _bulk_enrich(self, rows: List[DBCondominiumRoles]) -> List[CondominiumRoleEntity]:
        """Apply user_full_name + condominium_name enrichment to a list of role rows."""
        if not rows:
            return []

        user_ids = list({r.user_id for r in rows})
        condo_ids = list({r.condominium_id for r in rows})

        with session_scope() as session:
            # Fetch profiles via raw SQL (user_profiles has first_name, last_name keyed by user_id)
            user_names: dict[int, str] = {}
            if user_ids:
                placeholders = ", ".join([f":u{i}" for i in range(len(user_ids))])
                sql = f"SELECT user_id, first_name, last_name FROM user_profiles WHERE user_id IN ({placeholders})"
                params = {f"u{i}": uid for i, uid in enumerate(user_ids)}
                result = session.execute(text(sql), params)
                for row in result:
                    uid, fname, lname = row[0], row[1], row[2]
                    user_names[uid] = f"{fname or ''} {lname or ''}".strip()

            # Fetch condominiums via SQLAlchemy
            condos: dict[int, DBCondominiums] = {}
            if condo_ids:
                condos = {c.id: c for c in session.query(DBCondominiums).filter(DBCondominiums.id.in_(condo_ids)).all()}

            result_entities = []
            for row in rows:
                user_full_name = user_names.get(row.user_id)
                condo = condos.get(row.condominium_id)
                condominium_name = condo.name if condo else None

                entity = CondominiumRoleMapper.to_domain_enriched(
                    row,
                    user_full_name=user_full_name,
                    condominium_name=condominium_name,
                )
                result_entities.append(entity)
            return result_entities

    def get_by_id(self, id: int) -> Optional[CondominiumRoleEntity]:
        logger.debug(f"Fetching condominium role by id={id}")
        with session_scope() as session:
            db_role = (
                session.query(DBCondominiumRoles)
                .filter(
                    DBCondominiumRoles.id == id,
                    DBCondominiumRoles.deleted_at.is_(None),
                )
                .first()
            )
            if not db_role:
                return None
            enriched = self._bulk_enrich([db_role])
            return enriched[0] if enriched else None

    def get_by_uuid(self, uuid: str) -> Optional[CondominiumRoleEntity]:
        logger.debug(f"Fetching condominium role by uuid={uuid}")
        with session_scope() as session:
            db_role = (
                session.query(DBCondominiumRoles)
                .filter(
                    DBCondominiumRoles.uuid == uuid,
                    DBCondominiumRoles.deleted_at.is_(None),
                )
                .first()
            )
            if not db_role:
                return None
            enriched = self._bulk_enrich([db_role])
            return enriched[0] if enriched else None

    def get_active_by_user_and_condominium(
        self, user_id: int, condominium_id: int
    ) -> Optional[CondominiumRoleEntity]:
        logger.debug(
            f"Fetching active role for user_id={user_id} in condominium_id={condominium_id}"
        )
        with session_scope() as session:
            db_role = (
                session.query(DBCondominiumRoles)
                .filter(
                    and_(
                        DBCondominiumRoles.user_id == user_id,
                        DBCondominiumRoles.condominium_id == condominium_id,
                        DBCondominiumRoles.status == "active",
                        DBCondominiumRoles.deleted_at.is_(None),
                    )
                )
                .first()
            )
            if not db_role:
                return None
            enriched = self._bulk_enrich([db_role])
            return enriched[0] if enriched else None

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        user_id: Optional[int] = None,
        role: Optional[str] = None,
        scope: Optional[str] = None,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[CondominiumRoleEntity], int]:
        logger.debug(
            f"Listing condominium roles skip={skip} limit={limit} "
            f"condominium_id={condominium_id} user_id={user_id} scope={scope}"
        )
        with session_scope() as session:
            query = session.query(DBCondominiumRoles)

            if not include_deleted:
                query = query.filter(DBCondominiumRoles.deleted_at.is_(None))
            if condominium_id is not None:
                query = query.filter(DBCondominiumRoles.condominium_id == condominium_id)
            if user_id is not None:
                query = query.filter(DBCondominiumRoles.user_id == user_id)
            if role is not None:
                query = query.filter(DBCondominiumRoles.role == role)
            if scope is not None:
                query = query.filter(DBCondominiumRoles.scope == scope)
            if status is not None:
                query = query.filter(DBCondominiumRoles.status == status)

            total = query.count()
            results = (
                query
                .order_by(DBCondominiumRoles.condominium_id, DBCondominiumRoles.id)
                .offset(skip)
                .limit(limit)
                .all()
            )
            return self._bulk_enrich(results), total

    def list_by_condominium(
        self,
        condominium_id: int,
        skip: int = 0,
        limit: int = 100,
        role: Optional[str] = None,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[CondominiumRoleEntity], int]:
        logger.debug(f"Listing condominium roles for condominium_id={condominium_id}")
        with session_scope() as session:
            query = session.query(DBCondominiumRoles).filter(
                DBCondominiumRoles.condominium_id == condominium_id
            )

            if not include_deleted:
                query = query.filter(DBCondominiumRoles.deleted_at.is_(None))
            if role is not None:
                query = query.filter(DBCondominiumRoles.role == role)
            if status is not None:
                query = query.filter(DBCondominiumRoles.status == status)

            total = query.count()
            results = (
                query
                .order_by(DBCondominiumRoles.id)
                .offset(skip)
                .limit(limit)
                .all()
            )
            return self._bulk_enrich(results), total

    def list_by_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[CondominiumRoleEntity], int]:
        logger.debug(f"Listing condominium roles for user_id={user_id}")
        with session_scope() as session:
            query = session.query(DBCondominiumRoles).filter(
                DBCondominiumRoles.user_id == user_id
            )

            if not include_deleted:
                query = query.filter(DBCondominiumRoles.deleted_at.is_(None))
            if status is not None:
                query = query.filter(DBCondominiumRoles.status == status)

            total = query.count()
            results = (
                query
                .order_by(DBCondominiumRoles.condominium_id, DBCondominiumRoles.id)
                .offset(skip)
                .limit(limit)
                .all()
            )
            return self._bulk_enrich(results), total

    def _get_by_id_any_status(self, id: int) -> Optional[CondominiumRoleEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        logger.debug(f"Fetching condominium role by id={id} (any status)")
        with session_scope() as session:
            db_role = session.query(DBCondominiumRoles).filter(DBCondominiumRoles.id == id).first()
            if not db_role:
                return None
            enriched = self._bulk_enrich([db_role])
            return enriched[0] if enriched else None
