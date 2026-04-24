"""
from typing import Optional
Charge query repository implementation — SQLAlchemy.
"""
from typing import List, Optional, Tuple

from library.dddpy.core_charges.domain.charge_query_repository import (
    ChargeQueryRepository,
)
from library.dddpy.core_charges.domain.charge_entity import ChargeEntity
from library.dddpy.core_charges.infrastructure.dbcharge import DBCharge
from library.dddpy.core_charges.infrastructure.charge_mapper import ChargeMapper
from library.dddpy.core_charge_types.infrastructure.dbcharge_type import DBChargeType
from library.dddpy.core_condominiums.infrastructure.dbcondominiums import DBCondominiums as DBCondominium
from library.dddpy.core_units.infrastructure.dbunits import DBUnits as DBUnit
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("ChargeQueryRepository")


class ChargeQueryRepositoryImpl(ChargeQueryRepository):

    def __init__(self):
        logger.info("ChargeQueryRepositoryImpl initialized")

    def _enrich(self, db_c: DBCharge, db_ct=None, db_condo=None, db_unit=None) -> ChargeEntity:
        """Apply catalog enrichment to a charge entity."""
        entity = ChargeMapper.to_domain(db_c)
        if db_ct:
            entity.charge_type_code = db_ct.code
            entity.charge_type_name = db_ct.name
            entity.charge_type_is_global = bool(db_ct.is_global)
        if db_condo:
            entity.condominium_name = db_condo.name
        if db_unit:
            entity.unit_code = db_unit.code
        return entity

    def _bulk_enrich(self, rows: List[DBCharge]) -> List[ChargeEntity]:
        """Bulk-enrich charge rows with related catalog data."""
        if not rows:
            return []

        charge_type_ids = list({r.charge_type_id for r in rows})
        condo_ids = list({r.condominium_id for r in rows})
        unit_ids = list({r.unit_id for r in rows if r.unit_id})

        with session_scope() as session:
            charge_types = {
                ct.id: ct for ct in
                session.query(DBChargeType).filter(DBChargeType.id.in_(charge_type_ids)).all()
            }
            condos = {
                c.id: c for c in
                session.query(DBCondominium).filter(DBCondominium.id.in_(condo_ids)).all()
            }
            units = {}
            if unit_ids:
                units = {
                    u.id: u for u in
                    session.query(DBUnit).filter(DBUnit.id.in_(unit_ids)).all()
                }

            return [
                self._enrich(
                    row,
                    db_ct=charge_types.get(row.charge_type_id),
                    db_condo=condos.get(row.condominium_id),
                    db_unit=units.get(row.unit_id) if row.unit_id else None,
                )
                for row in rows
            ]

    def get_by_id(self, id: int) -> Optional[ChargeEntity]:
        logger.info(f"Fetching charge by id={id}")
        with session_scope() as session:
            row = session.query(DBCharge).filter(
                DBCharge.id == id,
                DBCharge.deleted_at.is_(None),
            ).first()
            if not row:
                logger.warning(f"Charge not found by id={id}")
                return None

            # Enrich
            ct = session.query(DBChargeType).filter(DBChargeType.id == row.charge_type_id).first()
            condo = session.query(DBCondominium).filter(DBCondominium.id == row.condominium_id).first()
            unit = session.query(DBUnit).filter(DBUnit.id == row.unit_id).first() if row.unit_id else None
            return self._enrich(row, ct, condo, unit)

    def get_by_uuid(self, uuid: str) -> Optional[ChargeEntity]:
        logger.info(f"Fetching charge by uuid={uuid}")
        with session_scope() as session:
            row = session.query(DBCharge).filter(
                DBCharge.uuid == uuid,
                DBCharge.deleted_at.is_(None),
            ).first()
            if not row:
                logger.warning(f"Charge not found by uuid={uuid}")
                return None

            ct = session.query(DBChargeType).filter(DBChargeType.id == row.charge_type_id).first()
            condo = session.query(DBCondominium).filter(DBCondominium.id == row.condominium_id).first()
            unit = session.query(DBUnit).filter(DBUnit.id == row.unit_id).first() if row.unit_id else None
            return self._enrich(row, ct, condo, unit)

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        charge_type_id: Optional[int] = None,
        unit_id: Optional[int] = None,
        status: Optional[str] = None,
        is_recurrent: Optional[bool] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[ChargeEntity], int]:
        logger.info(f"Listing charges skip={skip} limit={limit}")
        with session_scope() as session:
            query = session.query(DBCharge)

            if not include_deleted:
                query = query.filter(DBCharge.deleted_at.is_(None))
            if condominium_id is not None:
                query = query.filter(DBCharge.condominium_id == condominium_id)
            if charge_type_id is not None:
                query = query.filter(DBCharge.charge_type_id == charge_type_id)
            if unit_id is not None:
                query = query.filter(DBCharge.unit_id == unit_id)
            if status is not None:
                query = query.filter(DBCharge.status == status)
            if is_recurrent is not None:
                query = query.filter(DBCharge.is_recurrent == int(is_recurrent))

            total = query.count()
            rows = (
                query
                .order_by(DBCharge.id.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            return self._bulk_enrich(rows), total

    def list_by_condominium(
        self,
        condominium_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        is_recurrent: Optional[bool] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[ChargeEntity], int]:
        return self.list_all(
            skip=skip,
            limit=limit,
            condominium_id=condominium_id,
            status=status,
            is_recurrent=is_recurrent,
            include_deleted=include_deleted,
        )

    def _get_by_id_any_status(self, id: int) -> Optional[ChargeEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        logger.info(f"Fetching charge by id={id} (any status)")
        with session_scope() as session:
            row = session.query(DBCharge).filter(DBCharge.id == id).first()
            if not row:
                logger.warning(f"Charge not found by id={id}")
                return None
            return ChargeMapper.to_domain(row)
