"""
from typing import Optional
Incident query repository implementation — read operations with enrichment.
"""
from typing import Optional, List, Tuple
from sqlalchemy import and_, text

from library.dddpy.core_incidents.domain.incident_entity import IncidentEntity
from library.dddpy.core_incidents.domain.incident_query_repository import IncidentQueryRepository
from library.dddpy.core_incidents.infrastructure.dbinicident import DBIncident
from library.dddpy.core_incidents.infrastructure.incident_mapper import IncidentMapper
from library.dddpy.core_units.infrastructure.dbunits import DBUnits
from library.dddpy.core_buildings.infrastructure.dbbuildings import DBBuildings
from library.dddpy.core_condominiums.infrastructure.dbcondominiums import DBCondominium
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("IncidentQueryRepository")


class IncidentQueryRepositoryImpl(IncidentQueryRepository):

    def __init__(self):
        logger.info("IncidentQueryRepositoryImpl initialized")

    def _bulk_enrich(self, rows: List[DBIncident]) -> List[IncidentEntity]:
        """Apply unit + building + condominium + user enrichment to incident rows."""
        if not rows:
            return []

        unit_ids = list({r.unit_id for r in rows if r.unit_id})
        building_ids = list({r.building_id for r in rows if r.building_id})
        condo_ids = list({r.condominium_id for r in rows if r.condominium_id})
        reported_user_ids = list({r.reported_by_user_id for r in rows if r.reported_by_user_id})
        assigned_user_ids = [r.assigned_to_user_id for r in rows if r.assigned_to_user_id]
        all_user_ids = list(set(reported_user_ids + assigned_user_ids))

        with session_scope() as session:
            # 1. Units
            unit_map: dict[int, DBUnits] = {}
            if unit_ids:
                unit_map = {u.id: u for u in session.query(DBUnits).filter(DBUnits.id.in_(unit_ids)).all()}
                # Collect building_ids from units
                for u in unit_map.values():
                    if u.building_id and u.building_id not in building_ids:
                        building_ids.append(u.building_id)

            # 2. Buildings
            building_map: dict[int, DBBuildings] = {}
            if building_ids:
                building_map = {b.id: b for b in session.query(DBBuildings).filter(DBBuildings.id.in_(building_ids)).all()}
                # Collect condo_ids from buildings
                for b in building_map.values():
                    if b.condominium_id and b.condominium_id not in condo_ids:
                        condo_ids.append(b.condominium_id)

            # 3. Condominiums
            condo_map: dict[int, DBCondominium] = {}
            if condo_ids:
                condo_map = {c.id: c for c in session.query(DBCondominium).filter(DBCondominium.id.in_(condo_ids)).all()}

            # 4. User full names via raw SQL on user_profiles
            user_name_map: dict[int, str] = {}
            if all_user_ids:
                placeholders = ", ".join([f":u{i}" for i in range(len(all_user_ids))])
                sql = f"SELECT user_id, first_name, last_name FROM user_profiles WHERE user_id IN ({placeholders})"
                params = {f"u{i}": uid for i, uid in enumerate(all_user_ids)}
                result = session.execute(text(sql), params)
                for row in result:
                    uid, fname, lname = row[0], row[1], row[2]
                    user_name_map[uid] = f"{fname or ''} {lname or ''}".strip()

            result_entities = []
            for row in rows:
                unit = unit_map.get(row.unit_id)
                building = building_map.get(row.building_id) if row.building_id else None
                # If no building_id on incident, try to get it from unit
                if building is None and unit and unit.building_id:
                    building = building_map.get(unit.building_id)
                condo = None
                if building and building.condominium_id:
                    condo = condo_map.get(building.condominium_id)
                elif row.condominium_id:
                    condo = condo_map.get(row.condominium_id)

                entity = IncidentMapper.to_domain_enriched(
                    row,
                    unit_code=unit.code if unit else None,
                    building_name=building.name if building else None,
                    condominium_name=condo.name if condo else None,
                    reported_by_user_full_name=user_name_map.get(row.reported_by_user_id),
                    assigned_to_user_full_name=user_name_map.get(row.assigned_to_user_id) if row.assigned_to_user_id else None,
                )
                result_entities.append(entity)
            return result_entities

    def get_by_id(self, id: int) -> Optional[IncidentEntity]:
        logger.debug(f"Fetching incident by id={id}")
        with session_scope() as session:
            db_incident = (
                session.query(DBIncident)
                .filter(
                    DBIncident.id == id,
                    DBIncident.deleted_at.is_(None),
                )
                .first()
            )
            if not db_incident:
                return None
            enriched = self._bulk_enrich([db_incident])
            return enriched[0] if enriched else None

    def get_by_uuid(self, uuid: str) -> Optional[IncidentEntity]:
        logger.debug(f"Fetching incident by uuid={uuid}")
        with session_scope() as session:
            db_incident = (
                session.query(DBIncident)
                .filter(
                    DBIncident.uuid == uuid,
                    DBIncident.deleted_at.is_(None),
                )
                .first()
            )
            if not db_incident:
                return None
            enriched = self._bulk_enrich([db_incident])
            return enriched[0] if enriched else None

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        building_id: Optional[int] = None,
        unit_id: Optional[int] = None,
        reported_by_user_id: Optional[int] = None,
        assigned_to_user_id: Optional[int] = None,
        category: Optional[str] = None,
        priority: Optional[str] = None,
        status: Optional[str] = None,
        is_escalated: Optional[bool] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[IncidentEntity], int]:
        logger.debug(f"Listing incidents skip={skip} limit={limit}")
        with session_scope() as session:
            query = session.query(DBIncident)

            if not include_deleted:
                query = query.filter(DBIncident.deleted_at.is_(None))
            if condominium_id is not None:
                query = query.filter(DBIncident.condominium_id == condominium_id)
            if building_id is not None:
                query = query.filter(DBIncident.building_id == building_id)
            if unit_id is not None:
                query = query.filter(DBIncident.unit_id == unit_id)
            if reported_by_user_id is not None:
                query = query.filter(DBIncident.reported_by_user_id == reported_by_user_id)
            if assigned_to_user_id is not None:
                query = query.filter(DBIncident.assigned_to_user_id == assigned_to_user_id)
            if category is not None:
                query = query.filter(DBIncident.category == category)
            if priority is not None:
                query = query.filter(DBIncident.priority == priority)
            if status is not None:
                query = query.filter(DBIncident.status == status)
            if is_escalated is not None:
                query = query.filter(DBIncident.is_escalated == is_escalated)

            total = query.count()
            results = (
                query
                .order_by(DBIncident.id.desc())
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
        priority: Optional[str] = None,
        category: Optional[str] = None,
        building_id: Optional[int] = None,
        unit_id: Optional[int] = None,
        assigned_to_user_id: Optional[int] = None,
        is_escalated: Optional[bool] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[IncidentEntity], int]:
        logger.debug(f"Listing incidents for condominium_id={condominium_id}")
        with session_scope() as session:
            query = session.query(DBIncident).filter(
                DBIncident.condominium_id == condominium_id
            )

            if not include_deleted:
                query = query.filter(DBIncident.deleted_at.is_(None))
            if status is not None:
                query = query.filter(DBIncident.status == status)
            if priority is not None:
                query = query.filter(DBIncident.priority == priority)
            if category is not None:
                query = query.filter(DBIncident.category == category)
            if building_id is not None:
                query = query.filter(DBIncident.building_id == building_id)
            if unit_id is not None:
                query = query.filter(DBIncident.unit_id == unit_id)
            if assigned_to_user_id is not None:
                query = query.filter(DBIncident.assigned_to_user_id == assigned_to_user_id)
            if is_escalated is not None:
                query = query.filter(DBIncident.is_escalated == is_escalated)

            total = query.count()
            results = (
                query
                .order_by(DBIncident.id.desc())
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
    ) -> Tuple[List[IncidentEntity], int]:
        logger.debug(f"Listing incidents for reported_by user_id={user_id}")
        with session_scope() as session:
            query = session.query(DBIncident).filter(
                DBIncident.reported_by_user_id == user_id
            )

            if not include_deleted:
                query = query.filter(DBIncident.deleted_at.is_(None))
            if status is not None:
                query = query.filter(DBIncident.status == status)

            total = query.count()
            results = (
                query
                .order_by(DBIncident.id.desc())
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
    ) -> Tuple[List[IncidentEntity], int]:
        logger.debug(f"Listing incidents for unit_id={unit_id}")
        with session_scope() as session:
            query = session.query(DBIncident).filter(
                DBIncident.unit_id == unit_id
            )

            if not include_deleted:
                query = query.filter(DBIncident.deleted_at.is_(None))
            if status is not None:
                query = query.filter(DBIncident.status == status)

            total = query.count()
            results = (
                query
                .order_by(DBIncident.id.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            return self._bulk_enrich(results), total

    def list_by_assigned_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[IncidentEntity], int]:
        logger.debug(f"Listing incidents for assigned_to user_id={user_id}")
        with session_scope() as session:
            query = session.query(DBIncident).filter(
                DBIncident.assigned_to_user_id == user_id
            )

            if not include_deleted:
                query = query.filter(DBIncident.deleted_at.is_(None))
            if status is not None:
                query = query.filter(DBIncident.status == status)

            total = query.count()
            results = (
                query
                .order_by(DBIncident.id.desc())
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
    ) -> Tuple[List[IncidentEntity], int]:
        """List non-closed, non-cancelled incidents."""
        logger.debug(f"Listing active incidents skip={skip} limit={limit}")
        with session_scope() as session:
            query = session.query(DBIncident).filter(
                DBIncident.status.in_(["pending", "open", "in_progress"])
            )

            if condominium_id is not None:
                query = query.filter(DBIncident.condominium_id == condominium_id)

            total = query.count()
            results = (
                query
                .order_by(DBIncident.is_escalated.desc(), DBIncident.id.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            return self._bulk_enrich(results), total

    def _get_by_id_any_status(self, id: int) -> Optional[IncidentEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        logger.debug(f"Fetching incident by id={id} (any status)")
        with session_scope() as session:
            db_incident = (
                session.query(DBIncident)
                .filter(DBIncident.id == id)
                .first()
            )
            if not db_incident:
                return None
            enriched = self._bulk_enrich([db_incident])
            return enriched[0] if enriched else None
