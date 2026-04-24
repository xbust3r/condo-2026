"""Package Query Repository Implementation — with bulk enrichment."""
from typing import Optional, List, Tuple

from sqlalchemy import text

from library.dddpy.core_packages.domain.package_entity import PackageEntity
from library.dddpy.core_packages.domain.package_query_repository import PackageQueryRepository
from library.dddpy.core_packages.infrastructure.dbpackage import DBPackage
from library.dddpy.core_packages.infrastructure.package_mapper import PackageMapper
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("PackageQueryRepository")


class PackageQueryRepositoryImpl(PackageQueryRepository):

    def __init__(self):
        logger.info("PackageQueryRepositoryImpl initialized")

    def _bulk_enrich(self, rows: List[DBPackage]) -> List[PackageEntity]:
        """Apply recipient_name, unit_code, building_name, condominium_name enrichment."""
        if not rows:
            return []

        unit_ids = list({r.unit_id for r in rows if r.unit_id})
        recipient_ids = list({r.recipient_user_id for r in rows if r.recipient_user_id})

        with session_scope() as session:
            from library.dddpy.core_units.infrastructure.dbunits import DBUnits
            from library.dddpy.core_buildings.infrastructure.dbbuilding import DBBuildings
            from library.dddpy.core_condominiums.infrastructure.dbcondominium import DBCondominium

            # 1. Units (unit_code + building_id)
            unit_map = {}
            if unit_ids:
                units = session.query(DBUnits).filter(DBUnits.id.in_(unit_ids)).all()
                unit_map = {u.id: u for u in units}

            # 2. Buildings (building_name + condominium_id)
            building_ids = list({u.building_id for u in unit_map.values() if u.building_id})
            building_map = {}
            if building_ids:
                buildings = session.query(DBBuildings).filter(DBBuildings.id.in_(building_ids)).all()
                building_map = {b.id: b for b in buildings}

            # 3. Condominiums
            condo_ids = list({b.condominium_id for b in building_map.values() if b.condominium_id})
            condo_map = {}
            if condo_ids:
                condos = session.query(DBCondominium).filter(DBCondominium.id.in_(condo_ids)).all()
                condo_map = {c.id: c for c in condos}

            # 4. Recipient names (users + user_profiles)
            user_name_map = {}
            if recipient_ids:
                placeholders = ", ".join([f":u{i}" for i in range(len(recipient_ids))])
                sql = f"""
                    SELECT u.id, COALESCE(CONCAT(p.first_name, ' ', p.last_name), u.email) AS full_name
                    FROM users u
                    LEFT JOIN user_profiles p ON p.user_id = u.id AND p.deleted_at IS NULL
                    WHERE u.id IN ({placeholders})
                """
                params = {f"u{i}": uid for i, uid in enumerate(recipient_ids)}
                result = session.execute(text(sql), params)
                user_name_map = {row[0]: row[1] for row in result}

            result_entities = []
            for row in rows:
                unit = unit_map.get(row.unit_id)
                building = None
                if unit and unit.building_id:
                    building = building_map.get(unit.building_id)
                condo = None
                if building and building.condominium_id:
                    condo = condo_map.get(building.condominium_id)

                entity = PackageMapper.to_domain_enriched(
                    row,
                    recipient_name=user_name_map.get(row.recipient_user_id),
                    unit_code=unit.code if unit else None,
                    building_name=building.name if building else None,
                    condominium_name=condo.name if condo else None,
                )
                result_entities.append(entity)
            return result_entities

    def get_by_id(self, id: int) -> Optional[PackageEntity]:
        logger.debug(f"Fetching package by id={id}")
        with session_scope() as session:
            row = session.query(DBPackage).filter(
                DBPackage.id == id,
                DBPackage.deleted_at.is_(None),
            ).first()
            if not row:
                return None
            enriched = self._bulk_enrich([row])
            return enriched[0] if enriched else None

    def get_by_uuid(self, uuid: str) -> Optional[PackageEntity]:
        logger.debug(f"Fetching package by uuid={uuid}")
        with session_scope() as session:
            row = session.query(DBPackage).filter(
                DBPackage.uuid == uuid,
                DBPackage.deleted_at.is_(None),
            ).first()
            if not row:
                return None
            enriched = self._bulk_enrich([row])
            return enriched[0] if enriched else None

    def list_all(
        self,
        condominium_id: Optional[int] = None,
        unit_id: Optional[int] = None,
        recipient_user_id: Optional[int] = None,
        status: Optional[str] = None,
        include_deleted: bool = False,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[PackageEntity], int]:
        logger.debug(f"Listing packages skip={skip} limit={limit}")
        with session_scope() as session:
            query = session.query(DBPackage)
            if not include_deleted:
                query = query.filter(DBPackage.deleted_at.is_(None))
            if condominium_id is not None:
                query = query.filter(DBPackage.condominium_id == condominium_id)
            if unit_id is not None:
                query = query.filter(DBPackage.unit_id == unit_id)
            if recipient_user_id is not None:
                query = query.filter(DBPackage.recipient_user_id == recipient_user_id)
            if status is not None:
                query = query.filter(DBPackage.status == status)

            total = query.count()
            rows = query.order_by(DBPackage.created_at.desc()).offset(skip).limit(limit).all()
            return self._bulk_enrich(rows), total

    def list_pending(
        self,
        condominium_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[PackageEntity], int]:
        logger.debug(f"Listing pending packages for condominium_id={condominium_id}")
        with session_scope() as session:
            query = session.query(DBPackage).filter(
                DBPackage.condominium_id == condominium_id,
                DBPackage.status.in_(['pending', 'with_concierge']),
                DBPackage.deleted_at.is_(None),
            )
            total = query.count()
            rows = query.order_by(DBPackage.received_at.desc()).offset(skip).limit(limit).all()
            return self._bulk_enrich(rows), total

    def list_by_unit(
        self,
        unit_id: int,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[PackageEntity], int]:
        logger.debug(f"Listing packages for unit_id={unit_id}")
        with session_scope() as session:
            query = session.query(DBPackage).filter(
                DBPackage.unit_id == unit_id,
                DBPackage.deleted_at.is_(None),
            )
            if status is not None:
                query = query.filter(DBPackage.status == status)
            total = query.count()
            rows = query.order_by(DBPackage.created_at.desc()).offset(skip).limit(limit).all()
            return self._bulk_enrich(rows), total
