"""
from typing import Optional
Visitor query repository implementation — read operations with enrichment.
"""
from typing import Optional, List, Tuple
from sqlalchemy import and_

from library.dddpy.core_visitors.domain.visitor_entity import VisitorEntity
from library.dddpy.core_visitors.domain.visitor_query_repository import VisitorQueryRepository
from library.dddpy.core_visitors.infrastructure.dbvisitor import DBVisitor
from library.dddpy.core_visitors.infrastructure.visitor_mapper import VisitorMapper
from library.dddpy.core_units.infrastructure.dbunits import DBUnits
from library.dddpy.core_buildings.infrastructure.dbbuildings import DBBuildings
from library.dddpy.core_condominiums.infrastructure.dbcondominiums import DBCondominiums
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger
from sqlalchemy import text


logger = Logger("VisitorQueryRepository")


class VisitorQueryRepositoryImpl(VisitorQueryRepository):

    def __init__(self):
        logger.info("VisitorQueryRepositoryImpl initialized")

    def _bulk_enrich(self, rows: List[DBVisitor]) -> List[VisitorEntity]:
        """Apply unit + building + condominium + user enrichment to visitor rows."""
        if not rows:
            return []

        unit_ids = list({r.unit_id for r in rows if r.unit_id})
        building_ids = list({r.building_id for r in rows if r.building_id})
        condo_ids = list({r.condominium_id for r in rows if r.condominium_id})
        host_user_ids = list({r.host_user_id for r in rows if r.host_user_id})

        with session_scope() as session:
            # 1. Units
            unit_map: dict = {}
            if unit_ids:
                unit_map = {u.id: u for u in session.query(DBUnits).filter(DBUnits.id.in_(unit_ids)).all()}
                # Collect building_ids from units
                for u in unit_map.values():
                    if u.building_id and u.building_id not in building_ids:
                        building_ids.append(u.building_id)

            # 2. Buildings
            building_map: dict = {}
            if building_ids:
                building_map = {b.id: b for b in session.query(DBBuildings).filter(DBBuildings.id.in_(building_ids)).all()}
                # Collect condo_ids from buildings
                for b in building_map.values():
                    if b.condominium_id and b.condominium_id not in condo_ids:
                        condo_ids.append(b.condominium_id)

            # 3. Condominiums
            condo_map: dict = {}
            if condo_ids:
                condo_map = {c.id: c for c in session.query(DBCondominiums).filter(DBCondominiums.id.in_(condo_ids)).all()}

            # 4. User full names via raw SQL on user_profiles
            user_name_map: dict = {}
            if host_user_ids:
                placeholders = ", ".join([f":u{i}" for i in range(len(host_user_ids))])
                sql = f"SELECT user_id, first_name, last_name FROM user_profiles WHERE user_id IN ({placeholders})"
                params = {f"u{i}": uid for i, uid in enumerate(host_user_ids)}
                result = session.execute(text(sql), params)
                for row in result:
                    uid, fname, lname = row[0], row[1], row[2]
                    user_name_map[uid] = f"{fname or ''} {lname or ''}".strip()

            result_entities = []
            for row in rows:
                unit = unit_map.get(row.unit_id)
                building = building_map.get(row.building_id) if row.building_id else None
                if building is None and unit and unit.building_id:
                    building = building_map.get(unit.building_id)
                condo = None
                if building and building.condominium_id:
                    condo = condo_map.get(building.condominium_id)
                elif row.condominium_id:
                    condo = condo_map.get(row.condominium_id)

                entity = VisitorMapper.to_domain_enriched(
                    row,
                    host_user_full_name=user_name_map.get(row.host_user_id),
                    unit_code=unit.code if unit else None,
                    building_name=building.name if building else None,
                    condominium_name=condo.name if condo else None,
                )
                result_entities.append(entity)
            return result_entities

    def get_by_id(self, id: int) -> Optional[VisitorEntity]:
        logger.debug(f"Fetching visitor by id={id}")
        with session_scope() as session:
            db_visitor = (
                session.query(DBVisitor)
                .filter(
                    DBVisitor.id == id,
                    DBVisitor.deleted_at.is_(None),
                )
                .first()
            )
            if not db_visitor:
                return None
            enriched = self._bulk_enrich([db_visitor])
            return enriched[0] if enriched else None

    def get_by_uuid(self, uuid: str) -> Optional[VisitorEntity]:
        logger.debug(f"Fetching visitor by uuid={uuid}")
        with session_scope() as session:
            db_visitor = (
                session.query(DBVisitor)
                .filter(
                    DBVisitor.uuid == uuid,
                    DBVisitor.deleted_at.is_(None),
                )
                .first()
            )
            if not db_visitor:
                return None
            enriched = self._bulk_enrich([db_visitor])
            return enriched[0] if enriched else None

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        building_id: Optional[int] = None,
        unit_id: Optional[int] = None,
        host_user_id: Optional[int] = None,
        status: Optional[str] = None,
        expected_date: Optional[str] = None,
        visit_purpose: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[VisitorEntity], int]:
        logger.debug(f"Listing visitors skip={skip} limit={limit}")
        with session_scope() as session:
            query = session.query(DBVisitor)

            if not include_deleted:
                query = query.filter(DBVisitor.deleted_at.is_(None))
            if condominium_id is not None:
                query = query.filter(DBVisitor.condominium_id == condominium_id)
            if building_id is not None:
                query = query.filter(DBVisitor.building_id == building_id)
            if unit_id is not None:
                query = query.filter(DBVisitor.unit_id == unit_id)
            if host_user_id is not None:
                query = query.filter(DBVisitor.host_user_id == host_user_id)
            if status is not None:
                query = query.filter(DBVisitor.status == status)
            if expected_date is not None:
                query = query.filter(DBVisitor.expected_date == expected_date)
            if visit_purpose is not None:
                query = query.filter(DBVisitor.visit_purpose == visit_purpose)

            total = query.count()
            results = (
                query
                .order_by(DBVisitor.id.desc())
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
        status: Optional[str] = None,
        expected_date: Optional[str] = None,
        visit_purpose: Optional[str] = None,
        building_id: Optional[int] = None,
        unit_id: Optional[int] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[VisitorEntity], int]:
        logger.debug(f"Listing visitors for condominium_id={condominium_id}")
        with session_scope() as session:
            query = session.query(DBVisitor).filter(
                DBVisitor.condominium_id == condominium_id
            )

            if not include_deleted:
                query = query.filter(DBVisitor.deleted_at.is_(None))
            if status is not None:
                query = query.filter(DBVisitor.status == status)
            if expected_date is not None:
                query = query.filter(DBVisitor.expected_date == expected_date)
            if visit_purpose is not None:
                query = query.filter(DBVisitor.visit_purpose == visit_purpose)
            if building_id is not None:
                query = query.filter(DBVisitor.building_id == building_id)
            if unit_id is not None:
                query = query.filter(DBVisitor.unit_id == unit_id)

            total = query.count()
            results = (
                query
                .order_by(DBVisitor.id.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            return self._bulk_enrich(results), total

    def list_by_unit(
        self,
        unit_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[VisitorEntity], int]:
        logger.debug(f"Listing visitors for unit_id={unit_id}")
        with session_scope() as session:
            query = session.query(DBVisitor).filter(
                DBVisitor.unit_id == unit_id
            )

            if not include_deleted:
                query = query.filter(DBVisitor.deleted_at.is_(None))
            if status is not None:
                query = query.filter(DBVisitor.status == status)

            total = query.count()
            results = (
                query
                .order_by(DBVisitor.id.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            return self._bulk_enrich(results), total

    def list_by_host(
        self,
        host_user_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[VisitorEntity], int]:
        logger.debug(f"Listing visitors for host_user_id={host_user_id}")
        with session_scope() as session:
            query = session.query(DBVisitor).filter(
                DBVisitor.host_user_id == host_user_id
            )

            if not include_deleted:
                query = query.filter(DBVisitor.deleted_at.is_(None))
            if status is not None:
                query = query.filter(DBVisitor.status == status)

            total = query.count()
            results = (
                query
                .order_by(DBVisitor.id.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            return self._bulk_enrich(results), total

    def list_by_date(
        self,
        condominium_id: int,
        expected_date: str,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[VisitorEntity], int]:
        logger.debug(f"Listing visitors for condominium_id={condominium_id} on date={expected_date}")
        with session_scope() as session:
            query = session.query(DBVisitor).filter(
                DBVisitor.condominium_id == condominium_id,
                DBVisitor.expected_date == expected_date,
            )

            if not include_deleted:
                query = query.filter(DBVisitor.deleted_at.is_(None))
            if status is not None:
                query = query.filter(DBVisitor.status == status)

            total = query.count()
            results = (
                query
                .order_by(DBVisitor.expected_time.asc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            return self._bulk_enrich(results), total

    def list_active(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
    ) -> Tuple[List[VisitorEntity], int]:
        """List visitors that are pending or checked_in (active visits)."""
        logger.debug(f"Listing active visitors skip={skip} limit={limit}")
        with session_scope() as session:
            query = session.query(DBVisitor).filter(
                DBVisitor.status.in_(["pending", "checked_in"])
            )

            if condominium_id is not None:
                query = query.filter(DBVisitor.condominium_id == condominium_id)

            total = query.count()
            results = (
                query
                .order_by(DBVisitor.expected_date.asc(), DBVisitor.expected_time.asc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            return self._bulk_enrich(results), total

    def get_by_access_code(
        self,
        access_code: str,
        condominium_id: Optional[int] = None,
    ) -> Optional[VisitorEntity]:
        logger.debug(f"Fetching visitor by access_code={access_code}")
        with session_scope() as session:
            query = session.query(DBVisitor).filter(
                DBVisitor.access_code == access_code,
                DBVisitor.deleted_at.is_(None),
            )
            if condominium_id is not None:
                query = query.filter(DBVisitor.condominium_id == condominium_id)

            db_visitor = query.first()
            if not db_visitor:
                return None
            enriched = self._bulk_enrich([db_visitor])
            return enriched[0] if enriched else None

    def _get_by_id_any_status(self, id: int) -> Optional[VisitorEntity]:
        """Re-fetch entity ignoring soft-delete filter."""
        logger.debug(f"Fetching visitor by id={id} (any status)")
        with session_scope() as session:
            db_visitor = (
                session.query(DBVisitor)
                .filter(DBVisitor.id == id)
                .first()
            )
            if not db_visitor:
                return None
            enriched = self._bulk_enrich([db_visitor])
            return enriched[0] if enriched else None