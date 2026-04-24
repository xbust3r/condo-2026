"""
from typing import Optional
ChargeType query repository implementation — SQLAlchemy.
"""
from typing import List, Optional, Tuple

from library.dddpy.core_charge_types.domain.charge_type_query_repository import (
    ChargeTypeQueryRepository,
)
from library.dddpy.core_charge_types.domain.charge_type_entity import ChargeTypeEntity
from library.dddpy.core_charge_types.infrastructure.dbcharge_type import DBChargeType
from library.dddpy.core_charge_types.infrastructure.charge_type_mapper import (
    ChargeTypeMapper,
)
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("ChargeTypeQueryRepository")


class ChargeTypeQueryRepositoryImpl(ChargeTypeQueryRepository):

    def __init__(self):
        logger.info("ChargeTypeQueryRepositoryImpl initialized")

    def get_by_id(self, id: int) -> Optional[ChargeTypeEntity]:
        logger.info(f"Fetching charge type by id={id}")
        with session_scope() as session:
            db_ct = session.query(DBChargeType).filter(
                DBChargeType.id == id,
                DBChargeType.deleted_at.is_(None),
            ).first()
            if not db_ct:
                logger.warning(f"Charge type not found by id={id}")
                return None
            return ChargeTypeMapper.to_domain(db_ct)

    def get_by_uuid(self, uuid: str) -> Optional[ChargeTypeEntity]:
        logger.info(f"Fetching charge type by uuid={uuid}")
        with session_scope() as session:
            db_ct = session.query(DBChargeType).filter(
                DBChargeType.uuid == uuid,
                DBChargeType.deleted_at.is_(None),
            ).first()
            if not db_ct:
                logger.warning(f"Charge type not found by uuid={uuid}")
                return None
            return ChargeTypeMapper.to_domain(db_ct)

    def get_by_code(self, code: str) -> Optional[ChargeTypeEntity]:
        logger.info(f"Fetching charge type by code={code}")
        with session_scope() as session:
            db_ct = session.query(DBChargeType).filter(
                DBChargeType.code == code,
                DBChargeType.deleted_at.is_(None),
            ).first()
            if not db_ct:
                logger.warning(f"Charge type not found by code={code}")
                return None
            return ChargeTypeMapper.to_domain(db_ct)

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[ChargeTypeEntity], int]:
        logger.info(
            f"Listing charge types (skip={skip}, limit={limit}, "
            f"is_active={is_active}, include_deleted={include_deleted})"
        )
        with session_scope() as session:
            query = session.query(DBChargeType)

            if not include_deleted:
                query = query.filter(DBChargeType.deleted_at.is_(None))

            if is_active is not None:
                query = query.filter(DBChargeType.is_active == int(is_active))

            total = query.count()
            db_types = (
                query
                .order_by(DBChargeType.sort_order.asc(), DBChargeType.id.asc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            return [ChargeTypeMapper.to_domain(t) for t in db_types], total

    def _get_by_id_any_status(self, id: int) -> Optional[ChargeTypeEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        logger.info(f"Fetching charge type by id={id} (any status)")
        with session_scope() as session:
            db_ct = session.query(DBChargeType).filter(
                DBChargeType.id == id
            ).first()
            if not db_ct:
                logger.warning(f"Charge type not found by id={id}")
                return None
            return ChargeTypeMapper.to_domain(db_ct)
