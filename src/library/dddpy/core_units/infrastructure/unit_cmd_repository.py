from typing import Optional
from datetime import datetime
import uuid as uuid_lib
from sqlalchemy.exc import IntegrityError

from library.dddpy.core_units.domain.unit_entity import UnitEntity
from library.dddpy.core_units.domain.unit_data import CreateUnitData, UpdateUnitData
from library.dddpy.core_units.domain.unit_cmd_repository import UnitCmdRepository
from library.dddpy.core_units.infrastructure.dbunits import DBUnits
from library.dddpy.core_units.infrastructure.unit_mapper import UnitMapper
from library.dddpy.core_units.domain.unit_exception import (
    RepeatedUnitUnitNumber,
    RepeatedUnitCode,
)
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnitCmdRepository")


class UnitCmdRepositoryImpl(UnitCmdRepository):

    def __init__(self):
        logger.info("UnitCmdRepositoryImpl initialized")

    def create(self, data: CreateUnitData) -> UnitEntity:
        logger.info(
            f"Creating unit unit_number={data.unit_number}, building_id={data.building_id}"
        )
        try:
            with session_scope() as session:
                db_unit = DBUnits(
                    uuid=str(uuid_lib.uuid4()),
                    building_id=data.building_id,
                    unit_type_id=data.unit_type_id,
                    unit_number=data.unit_number,
                    code=data.code,
                    name=data.name if data.name is not None else data.unit_number,
                    description=data.description,
                    private_area=data.private_area,
                    coefficient=data.coefficient,
                    floor_number=data.floor_number,
                    floor_label=data.floor_label,
                    occupancy_status=data.occupancy_status,
                    sort_order=data.sort_order,
                    condominium_coefficient=data.condominium_coefficient,
                )
                session.add(db_unit)
                session.flush()
                session.refresh(db_unit)
                logger.info(f"Unit created with id={db_unit.id}")
                return UnitMapper.to_domain(db_unit)
        except IntegrityError as e:
            mysql_code = e.orig.args[0] if hasattr(e, 'orig') and hasattr(e.orig, 'args') else None
            error_str = str(e).lower()
            # 1062 = duplicate key (including unique constraint violations)
            if mysql_code == 1062:
                if 'ux_core_units_building_unit_number' in error_str or (
                    'unit_number' in error_str and 'ux_core_units_building_code' not in error_str
                ):
                    logger.warning(
                        f"Duplicate unit_number={data.unit_number} in building_id={data.building_id}"
                    )
                    raise RepeatedUnitUnitNumber()
                if 'ux_core_units_building_code' in error_str or (
                    'code' in error_str and 'building_id' in error_str
                ):
                    logger.warning(
                        f"Duplicate code={data.code} in building_id={data.building_id}"
                    )
                    raise RepeatedUnitCode()
                # Fall-through for other 1062 (let it bubble)
            # 1048 = column cannot be null (NOT NULL constraint violation)
            if mysql_code == 1048:
                logger.error(f"NOT NULL constraint violation: {e}")
                raise
            logger.error(f"Unexpected IntegrityError creating unit: {e}")
            raise

    def update(self, id: int, data: UpdateUnitData) -> Optional[UnitEntity]:
        logger.info(f"Updating unit id={id}")
        try:
            with session_scope() as session:
                db_unit = session.query(DBUnits).filter(DBUnits.id == id).first()
                if not db_unit:
                    logger.warning(f"Unit not found for update id={id}")
                    return None

                if data.unit_number is not None:
                    db_unit.unit_number = data.unit_number
                if data.code is not None:
                    db_unit.code = data.code
                if data.name is not None:
                    db_unit.name = data.name
                if data.description is not None:
                    db_unit.description = data.description
                if data.unit_type_id is not None:
                    db_unit.unit_type_id = data.unit_type_id
                if data.private_area is not None:
                    db_unit.private_area = data.private_area
                if data.coefficient is not None:
                    db_unit.coefficient = data.coefficient
                if data.floor_number is not None:
                    db_unit.floor_number = data.floor_number
                if data.floor_label is not None:
                    db_unit.floor_label = data.floor_label
                if data.occupancy_status is not None:
                    db_unit.occupancy_status = data.occupancy_status
                if data.sort_order is not None:
                    db_unit.sort_order = data.sort_order
                if data.status is not None:
                    db_unit.status = data.status
                if data.condominium_coefficient is not None:
                    db_unit.condominium_coefficient = data.condominium_coefficient

                session.flush()
                session.refresh(db_unit)
                logger.info(f"Unit updated id={id}")
                return UnitMapper.to_domain(db_unit)
        except IntegrityError as e:
            mysql_code = e.orig.args[0] if hasattr(e, 'orig') and hasattr(e.orig, 'args') else None
            error_str = str(e).lower()
            if mysql_code == 1062:
                if 'ux_core_units_building_unit_number' in error_str or (
                    'unit_number' in error_str and 'ux_core_units_building_code' not in error_str
                ):
                    logger.warning(f"IntegrityError: duplicate unit_number during update id={id}")
                    raise RepeatedUnitUnitNumber()
                if 'ux_core_units_building_code' in error_str or (
                    'code' in error_str and 'building_id' in error_str
                ):
                    logger.warning(f"IntegrityError: duplicate code during update id={id}")
                    raise RepeatedUnitCode()
            logger.error(f"IntegrityError updating unit id={id}: {e}")
            raise

    def soft_delete(self, id: int) -> bool:
        logger.info(f"Soft deleting unit id={id}")
        with session_scope() as session:
            db_unit = session.query(DBUnits).filter(DBUnits.id == id).first()
            if not db_unit:
                logger.warning(f"Unit not found for soft delete id={id}")
                return False
            db_unit.deleted_at = datetime.utcnow()
            session.flush()
            logger.info(f"Unit soft deleted id={id}")
            return True

    def restore(self, id: int) -> bool:
        logger.info(f"Restoring unit id={id}")
        with session_scope() as session:
            db_unit = session.query(DBUnits).filter(DBUnits.id == id).first()
            if not db_unit:
                logger.warning(f"Unit not found for restore id={id}")
                return False
            db_unit.deleted_at = None
            session.flush()
            logger.info(f"Unit restored id={id}")
            return True

    def hard_delete(self, id: int) -> bool:
        logger.info(f"Hard deleting unit id={id}")
        with session_scope() as session:
            db_unit = session.query(DBUnits).filter(DBUnits.id == id).first()
            if not db_unit:
                logger.warning(f"Unit not found for hard delete id={id}")
                return False
            session.delete(db_unit)
            session.flush()
            logger.info(f"Unit hard deleted id={id}")
            return True