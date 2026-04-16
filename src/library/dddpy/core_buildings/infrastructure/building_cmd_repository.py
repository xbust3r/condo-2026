from typing import Optional, Dict, Any
from datetime import datetime
import uuid as uuid_lib
from sqlalchemy.exc import IntegrityError

from library.dddpy.core_buildings.domain.building_entity import BuildingEntity
from library.dddpy.core_buildings.domain.building_data import CreateBuildingData, UpdateBuildingData
from library.dddpy.core_buildings.domain.building_cmd_repository import BuildingCmdRepository
from library.dddpy.core_buildings.infrastructure.dbbuildings import DBBuildings
from library.dddpy.core_buildings.infrastructure.building_mapper import BuildingMapper
from library.dddpy.core_buildings.domain.building_exception import RepeatedBuildingCode
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("BuildingCmdRepository")


class BuildingCmdRepositoryImpl(BuildingCmdRepository):

    def __init__(self):
        logger.info("BuildingCmdRepositoryImpl initialized")

    def create(self, data: CreateBuildingData) -> BuildingEntity:
        logger.info(f"Creating building with code={data.code}, condominium_id={data.condominium_id}")
        try:
            with session_scope() as session:
                db_building = DBBuildings(
                    uuid=str(uuid_lib.uuid4()),
                    condominium_id=data.condominium_id,
                    code=data.code,
                    name=data.name,
                    short_name=data.short_name,
                    description=data.description,
                    building_type_id=data.building_type_id,
                    built_area=data.built_area,
                    common_area=data.common_area,
                    coefficient=data.coefficient,
                    floors_count=data.floors_count,
                    basements_count=data.basements_count,
                    units_planned=data.units_planned,
                    sort_order=data.sort_order,
                )
                session.add(db_building)
                session.flush()
                session.refresh(db_building)
                logger.info(f"Building created with id={db_building.id}")
                return BuildingMapper.to_domain(db_building)
        except IntegrityError as e:
            logger.warning(f"IntegrityError: duplicate code={data.code} in condominium={data.condominium_id} — {e}")
            raise RepeatedBuildingCode()
        except Exception as e:
            logger.error(f"Unexpected error creating building: {e}")
            raise

    def update(self, id: int, data: UpdateBuildingData) -> Optional[BuildingEntity]:
        logger.info(f"Updating building id={id}")
        with session_scope() as session:
            db_building = session.query(DBBuildings).filter(DBBuildings.id == id).first()
            if not db_building:
                logger.warning(f"Building not found for update id={id}")
                return None
            if data.name is not None:
                db_building.name = data.name
            if data.short_name is not None:
                db_building.short_name = data.short_name
            if data.description is not None:
                db_building.description = data.description
            if data.building_type_id is not None:
                db_building.building_type_id = data.building_type_id
            if data.built_area is not None:
                db_building.built_area = data.built_area
            if data.common_area is not None:
                db_building.common_area = data.common_area
            if data.coefficient is not None:
                db_building.coefficient = data.coefficient
            if data.floors_count is not None:
                db_building.floors_count = data.floors_count
            if data.basements_count is not None:
                db_building.basements_count = data.basements_count
            if data.units_planned is not None:
                db_building.units_planned = data.units_planned
            if data.sort_order is not None:
                db_building.sort_order = data.sort_order
            if data.status is not None:
                db_building.status = data.status
            session.flush()
            session.refresh(db_building)
            logger.info(f"Building updated id={id}")
            return BuildingMapper.to_domain(db_building)

    def soft_delete(self, id: int) -> bool:
        logger.info(f"Soft deleting building id={id}")
        with session_scope() as session:
            db_building = session.query(DBBuildings).filter(DBBuildings.id == id).first()
            if not db_building:
                logger.warning(f"Building not found for soft delete id={id}")
                return False
            db_building.deleted_at = datetime.utcnow()
            session.flush()
            logger.info(f"Building soft deleted id={id}")
            return True

    def restore(self, id: int) -> bool:
        logger.info(f"Restoring building id={id}")
        with session_scope() as session:
            db_building = session.query(DBBuildings).filter(DBBuildings.id == id).first()
            if not db_building:
                logger.warning(f"Building not found for restore id={id}")
                return False
            db_building.deleted_at = None
            session.flush()
            logger.info(f"Building restored id={id}")
            return True

    def hard_delete(self, id: int) -> bool:
        logger.info(f"Hard deleting building id={id}")
        with session_scope() as session:
            db_building = session.query(DBBuildings).filter(DBBuildings.id == id).first()
            if not db_building:
                logger.warning(f"Building not found for hard delete id={id}")
                return False
            session.delete(db_building)
            session.flush()
            logger.info(f"Building hard deleted id={id}")
            return True

    def update_computed_fields(self, id: int, stats: Dict[str, Any]) -> Optional[BuildingEntity]:
        """
        Update computed stats for a building from unit aggregation.
        Sets built_area, coefficient, floors_count, basements_count, units_planned.
        """
        logger.info(f"Updating computed fields for building id={id}: {stats}")
        with session_scope() as session:
            db_building = session.query(DBBuildings).filter(DBBuildings.id == id).first()
            if not db_building:
                logger.warning(f"Building not found for computed update id={id}")
                return None
            db_building.built_area = stats.get("built_area")
            db_building.coefficient = stats.get("coefficient_sum")
            db_building.floors_count = stats.get("floors_count", 0)
            db_building.basements_count = stats.get("basements_count", 0)
            db_building.units_planned = stats.get("units_count", 0)
            session.flush()
            session.refresh(db_building)
            logger.info(f"Computed fields updated for building id={id}")
            return BuildingMapper.to_domain(db_building)