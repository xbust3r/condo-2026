from typing import Optional, List

from library.dddpy.core_condominiums.domain.condominium_query_repository import CondominiumQueryRepository
from library.dddpy.core_condominiums.domain.condominium_entity import CondominiumEntity
from library.dddpy.core_condominiums.infrastructure.dbcondominiums import DBCondominiums
from library.dddpy.core_condominiums.infrastructure.condominium_mapper import CondominiumMapper
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("CondominiumQueryRepository")


class CondominiumQueryRepositoryImpl(CondominiumQueryRepository):

    def __init__(self):
        logger.info("CondominiumQueryRepositoryImpl initialized")

    def get_by_id(self, id: int) -> Optional[CondominiumEntity]:
        logger.info(f"Fetching condominium by id={id}")
        with session_scope() as session:
            db_condominium = session.query(DBCondominiums).filter(
                DBCondominiums.id == id,
                DBCondominiums.deleted_at.is_(None)
            ).first()
            if not db_condominium:
                logger.warning(f"Condominium not found by id={id}")
                return None
            return CondominiumMapper.to_domain(db_condominium)

    def get_by_uuid(self, uuid: str) -> Optional[CondominiumEntity]:
        logger.info(f"Fetching condominium by uuid={uuid}")
        with session_scope() as session:
            db_condominium = session.query(DBCondominiums).filter(
                DBCondominiums.uuid == uuid,
                DBCondominiums.deleted_at.is_(None)
            ).first()
            if not db_condominium:
                logger.warning(f"Condominium not found by uuid={uuid}")
                return None
            return CondominiumMapper.to_domain(db_condominium)

    def get_by_code(self, code: str) -> Optional[CondominiumEntity]:
        logger.info(f"Fetching condominium by code={code}")
        with session_scope() as session:
            db_condominium = session.query(DBCondominiums).filter(
                DBCondominiums.code == code,
                DBCondominiums.deleted_at.is_(None)
            ).first()
            if not db_condominium:
                logger.warning(f"Condominium not found by code={code}")
                return None
            return CondominiumMapper.to_domain(db_condominium)

    def get_by_name(self, name: str) -> Optional[CondominiumEntity]:
        logger.info(f"Fetching condominium by name={name}")
        with session_scope() as session:
            db_condominium = session.query(DBCondominiums).filter(
                DBCondominiums.name == name,
                DBCondominiums.deleted_at.is_(None)
            ).first()
            if not db_condominium:
                logger.warning(f"Condominium not found by name={name}")
                return None
            return CondominiumMapper.to_domain(db_condominium)

    def list_all(self, skip: int = 0, limit: int = 100, status: Optional[int] = None, city: Optional[str] = None, country: Optional[str] = None, include_deleted: bool = False) -> tuple[List[CondominiumEntity], int]:
        logger.info(f"Fetching condominiums (skip={skip}, limit={limit}, status={status}, city={city}, country={country}, include_deleted={include_deleted})")
        with session_scope() as session:
            query = session.query(DBCondominiums)
            
            # Exclude deleted by default
            if not include_deleted:
                query = query.filter(DBCondominiums.deleted_at.is_(None))
            
            # Apply filters
            if status is not None:
                query = query.filter(DBCondominiums.status == status)
            if city:
                query = query.filter(DBCondominiums.city.ilike(f"%{city}%"))
            if country:
                query = query.filter(DBCondominiums.country.ilike(f"%{country}%"))
            
            total = query.count()
            db_condominiums = query.offset(skip).limit(limit).all()
            return [CondominiumMapper.to_domain(c) for c in db_condominiums], total

    # ── Internal helpers for post-mutation re-fetch ──────────────────────────

    def _get_by_id_any_status(self, id: int) -> Optional[CondominiumEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        logger.info(f"Fetching condominium by id={id} (any status)")
        with session_scope() as session:
            db_condominium = session.query(DBCondominiums).filter(
                DBCondominiums.id == id
            ).first()
            if not db_condominium:
                logger.warning(f"Condominium not found by id={id}")
                return None
            return CondominiumMapper.to_domain(db_condominium)
