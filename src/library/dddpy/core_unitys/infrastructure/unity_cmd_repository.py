from typing import Optional
from datetime import datetime
import uuid as uuid_lib
from sqlalchemy.exc import IntegrityError

from library.dddpy.core_unitys.domain.unity_entity import UnityEntity
from library.dddpy.core_unitys.domain.unity_data import CreateUnityData, UpdateUnityData
from library.dddpy.core_unitys.domain.unity_cmd_repository import UnityCmdRepository
from library.dddpy.core_unitys.infrastructure.dbunitys import DBUnitys
from library.dddpy.core_unitys.infrastructure.unity_mapper import UnityMapper
from library.dddpy.core_unitys.domain.unity_exception import (
    RepeatedUnityUnitNumber,
    RepeatedUnityCode,
)
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("UnityCmdRepository")


class UnityCmdRepositoryImpl(UnityCmdRepository):

    def __init__(self):
        logger.info("UnityCmdRepositoryImpl initialized")

    def create(self, data: CreateUnityData) -> UnityEntity:
        logger.info(
            f"Creating unity unit_number={data.unit_number}, building_id={data.building_id}"
        )
        try:
            with session_scope() as session:
                db_unity = DBUnitys(
                    uuid=str(uuid_lib.uuid4()),
                    building_id=data.building_id,
                    unity_type_id=data.unity_type_id,
                    unit_number=data.unit_number,
                    code=data.code,
                    name=data.name,
                    description=data.description,
                    private_area=data.private_area,
                    coefficient=data.coefficient,
                    floor_number=data.floor_number,
                    floor_label=data.floor_label,
                    occupancy_status=data.occupancy_status,
                    sort_order=data.sort_order,
                )
                session.add(db_unity)
                session.flush()
                session.refresh(db_unity)
                logger.info(f"Unity created with id={db_unity.id}")
                return UnityMapper.to_domain(db_unity)
        except IntegrityError as e:
            error_str = str(e).lower()
            if "unit_number" in error_str or "ux_core_unitys_building_unit_number" in error_str:
                logger.warning(
                    f"Duplicate unit_number={data.unit_number} in building_id={data.building_id}"
                )
                raise RepeatedUnityUnitNumber()
            if "code" in error_str or "ux_core_unitys_building_code" in error_str:
                logger.warning(
                    f"Duplicate code={data.code} in building_id={data.building_id}"
                )
                raise RepeatedUnityCode()
            logger.error(f"Unexpected IntegrityError creating unity: {e}")
            raise

    def update(self, id: int, data: UpdateUnityData) -> Optional[UnityEntity]:
        logger.info(f"Updating unity id={id}")
        try:
            with session_scope() as session:
                db_unity = session.query(DBUnitys).filter(DBUnitys.id == id).first()
                if not db_unity:
                    logger.warning(f"Unity not found for update id={id}")
                    return None

                if data.unit_number is not None:
                    db_unity.unit_number = data.unit_number
                if data.code is not None:
                    db_unity.code = data.code
                if data.name is not None:
                    db_unity.name = data.name
                if data.description is not None:
                    db_unity.description = data.description
                if data.unity_type_id is not None:
                    db_unity.unity_type_id = data.unity_type_id
                if data.private_area is not None:
                    db_unity.private_area = data.private_area
                if data.coefficient is not None:
                    db_unity.coefficient = data.coefficient
                if data.floor_number is not None:
                    db_unity.floor_number = data.floor_number
                if data.floor_label is not None:
                    db_unity.floor_label = data.floor_label
                if data.occupancy_status is not None:
                    db_unity.occupancy_status = data.occupancy_status
                if data.sort_order is not None:
                    db_unity.sort_order = data.sort_order
                if data.status is not None:
                    db_unity.status = data.status

                session.flush()
                session.refresh(db_unity)
                logger.info(f"Unity updated id={id}")
                return UnityMapper.to_domain(db_unity)
        except IntegrityError as e:
            error_str = str(e).lower()
            if "unit_number" in error_str or "ux_core_unitys_building_unit_number" in error_str:
                logger.warning(f"IntegrityError: duplicate unit_number during update id={id}")
                raise RepeatedUnityUnitNumber()
            if "code" in error_str or "ux_core_unitys_building_code" in error_str:
                logger.warning(f"IntegrityError: duplicate code during update id={id}")
                raise RepeatedUnityCode()
            logger.error(f"Unexpected IntegrityError updating unity id={id}: {e}")
            raise

    def soft_delete(self, id: int) -> bool:
        logger.info(f"Soft deleting unity id={id}")
        with session_scope() as session:
            db_unity = session.query(DBUnitys).filter(DBUnitys.id == id).first()
            if not db_unity:
                logger.warning(f"Unity not found for soft delete id={id}")
                return False
            db_unity.deleted_at = datetime.utcnow()
            session.flush()
            logger.info(f"Unity soft deleted id={id}")
            return True

    def restore(self, id: int) -> bool:
        logger.info(f"Restoring unity id={id}")
        with session_scope() as session:
            db_unity = session.query(DBUnitys).filter(DBUnitys.id == id).first()
            if not db_unity:
                logger.warning(f"Unity not found for restore id={id}")
                return False
            db_unity.deleted_at = None
            session.flush()
            logger.info(f"Unity restored id={id}")
            return True

    def hard_delete(self, id: int) -> bool:
        logger.info(f"Hard deleting unity id={id}")
        with session_scope() as session:
            db_unity = session.query(DBUnitys).filter(DBUnitys.id == id).first()
            if not db_unity:
                logger.warning(f"Unity not found for hard delete id={id}")
                return False
            session.delete(db_unity)
            session.flush()
            logger.info(f"Unity hard deleted id={id}")
            return True
