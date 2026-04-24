from typing import Optional
from typing import Optional
from library.dddpy.core_condominiums.usecase.condominium_cmd_usecase import CondominiumCmdUseCase
from library.dddpy.core_condominiums.usecase.condominium_query_usecase import CondominiumQueryUseCase
from library.dddpy.core_condominiums.usecase.condominium_factory import condominium_cmd_usecase_factory, condominium_query_usecase_factory
from library.dddpy.core_condominiums.usecase.condominium_cmd_schema import CreateCondominiumSchema, UpdateCondominiumSchema
from library.dddpy.core_condominiums.domain.condominium_exception import CondominiumNotFound, RepeatedCondominiumCode
from library.dddpy.core_condominiums.domain.condominium_success import CondominiumSuccessMessage
from library.dddpy.shared.schemas.response_schema import ResponseSuccessSchema
from library.dddpy.shared.logging.logging import Logger


logger = Logger("CondominiumUseCase")


def _enrich_condominium_with_unit_stats(condo_dict: dict) -> dict:
    """
    Compute and attach unit/building statistics to a condominium dict.

    Adds:
      - built_area:             sum of all unit private_areas
      - condominium_coefficient: sum of all unit condominium_coefficients (should be 100%)
      - units_count:            total active units in the condominium
      - buildings_count:         total active buildings in the condominium
    """
    condo_id = condo_dict.get("id")
    if condo_id is None:
        return condo_dict

    try:
        from library.dddpy.core_units.infrastructure.unit_query_repository import (
            UnitQueryRepositoryImpl,
        )
        unit_repo = UnitQueryRepositoryImpl()
        stats = unit_repo.get_condominium_stats(condo_id)
        # registered_built_area: stored field (official catastro / land registry)
        # total_area: computed from unit private_areas sum
        condo_dict["registered_built_area"] = round(float(condo_dict["built_area"]), 4) if condo_dict.get("built_area") else None
        condo_dict["total_area"] = round(stats["built_area"], 4) if stats["built_area"] else None
        condo_dict["condominium_coefficient"] = round(stats["condominium_coefficient_sum"], 6) if stats["condominium_coefficient_sum"] else None
        condo_dict["total_units"] = stats["units_count"]
        # Remove raw built_area key (replaced by registered_built_area + total_area)
        condo_dict.pop("built_area", None)
        # Count buildings
        try:
            from library.dddpy.core_buildings.infrastructure.building_query_repository import (
                BuildingQueryRepositoryImpl,
            )
            from library.dddpy.shared.mysql.session_manager import session_scope
            from library.dddpy.core_buildings.infrastructure.dbbuildings import DBBuildings
            with session_scope() as session:
                count = session.query(DBBuildings).filter(
                    DBBuildings.condominium_id == condo_id,
                    DBBuildings.status == 1,
                    DBBuildings.deleted_at.is_(None)
                ).count()
            condo_dict["buildings_count"] = count
        except Exception:
            condo_dict["buildings_count"] = 0
    except Exception as e:
        logger.warning(f"Could not compute condominium stats for id={condo_id}: {e}")

    return condo_dict


class CondominiumUseCase:
    def __init__(self):
        logger.add_inside_method("__init__")
        self.condominium_cmd_usecase: CondominiumCmdUseCase = condominium_cmd_usecase_factory()
        self.condominium_query_usecase: CondominiumQueryUseCase = condominium_query_usecase_factory()
        logger.info("CondominiumUseCase initialized")

    def create(self, data: CreateCondominiumSchema):
        logger.add_inside_method("create")
        logger.info(f"Creating condominium with data: {data}")
        existing = self.condominium_query_usecase.get_by_code(data.code)
        if existing:
            logger.warning(f"Condominium code already exists: {data.code}")
            raise RepeatedCondominiumCode()
        new_condominium = self.condominium_cmd_usecase.create(data)
        success = ResponseSuccessSchema(
            success=True,
            message=CondominiumSuccessMessage.CREATED,
            data=new_condominium.to_dict(),
        )
        logger.info(f"{success.message}: {success}")
        return success

    def get_by_id(self, id: int):
        logger.add_inside_method("get_by_id")
        condominium = self.condominium_query_usecase.get_by_id(id)
        if not condominium:
            logger.warning(f"Condominium not found by id={id}")
            raise CondominiumNotFound()
        condo_dict = condominium.to_dict()
        _enrich_condominium_with_unit_stats(condo_dict)
        success = ResponseSuccessSchema(
            success=True,
            message=CondominiumSuccessMessage.RETRIEVED,
            data=condo_dict,
        )
        logger.info(f"{success.message} by id={id}")
        return success

    def get_by_uuid(self, uuid: str):
        logger.add_inside_method("get_by_uuid")
        condominium = self.condominium_query_usecase.get_by_uuid(uuid)
        if not condominium:
            logger.warning(f"Condominium not found by uuid={uuid}")
            raise CondominiumNotFound()
        condo_dict = condominium.to_dict()
        _enrich_condominium_with_unit_stats(condo_dict)
        success = ResponseSuccessSchema(
            success=True,
            message=CondominiumSuccessMessage.RETRIEVED,
            data=condo_dict,
        )
        logger.info(f"{success.message} by uuid={uuid}")
        return success

    def get_by_code(self, code: str):
        logger.add_inside_method("get_by_code")
        condominium = self.condominium_query_usecase.get_by_code(code)
        if not condominium:
            logger.warning(f"Condominium not found by code={code}")
            raise CondominiumNotFound()
        condo_dict = condominium.to_dict()
        _enrich_condominium_with_unit_stats(condo_dict)
        success = ResponseSuccessSchema(
            success=True,
            message=CondominiumSuccessMessage.RETRIEVED,
            data=condo_dict,
        )
        logger.info(f"{success.message} by code={code}")
        return success

    def update(self, id: int, data: UpdateCondominiumSchema):
        logger.add_inside_method("update")
        logger.info(f"Updating condominium id={id} with data: {data}")
        # Verificar que existe
        existing = self.condominium_query_usecase.get_by_id(id)
        if not existing:
            logger.warning(f"Condominium not found for update id={id}")
            raise CondominiumNotFound()
        updated_condominium = self.condominium_cmd_usecase.update(id, data)
        success = ResponseSuccessSchema(
            success=True,
            message=CondominiumSuccessMessage.UPDATED,
            data=updated_condominium.to_dict(),
        )
        logger.info(f"{success.message}: {success}")
        return success

    def delete(self, id: int):
        logger.add_inside_method("delete")
        logger.info(f"Soft deleting condominium id={id}")
        # Verificar que existe
        existing = self.condominium_query_usecase.get_by_id(id)
        if not existing:
            logger.warning(f"Condominium not found for delete id={id}")
            raise CondominiumNotFound()
        deleted = self.condominium_cmd_usecase.delete(id)
        if not deleted:
            logger.warning(f"Failed to delete condominium id={id}")
            raise CondominiumNotFound()
        # Re-fetch to return actual persisted state (ignore soft-delete filter)
        fresh = self.condominium_query_usecase.get_by_id_any_status(id)
        real_deleted_at = fresh.deleted_at if fresh else None
        success = ResponseSuccessSchema(
            success=True,
            message=CondominiumSuccessMessage.DELETED,
            data={"id": id, "deleted_at": real_deleted_at},
        )
        logger.info(f"{success.message} for id={id}")
        return success

    def restore(self, id: int):
        logger.add_inside_method("restore")
        logger.info(f"Restoring condominium id={id}")
        # Verify it exists first (use any-status since entity is soft-deleted)
        existing = self.condominium_query_usecase.get_by_id_any_status(id)
        if not existing:
            logger.warning(f"Condominium not found for restore id={id}")
            raise CondominiumNotFound()
        restored = self.condominium_cmd_usecase.restore(id)
        if not restored:
            logger.warning(f"Failed to restore condominium id={id}")
            raise CondominiumNotFound()
        # Re-fetch to return actual persisted state
        refreshed = self.condominium_query_usecase.get_by_id_any_status(id)
        success = ResponseSuccessSchema(
            success=True,
            message=CondominiumSuccessMessage.RESTORED,
            data=refreshed.to_dict(),
        )
        logger.info(f"{success.message} for id={id}")
        return success

    def get_summary(self, id: int) -> ResponseSuccessSchema:
        """
        Return a consolidated financial + operational summary for a condominium.

        Includes:
          - Condominium identity data (with unit/building stats)
          - AR summary: total_debt, total_pending, overdue_count, overdue_30_days_count
          - overdue_amount: total outstanding balance for overdue AR
        """
        logger.add_inside_method("get_summary")

        # Verify condominium exists
        condominium = self.condominium_query_usecase.get_by_id(id)
        if not condominium:
            logger.warning(f"Condominium not found for summary id={id}")
            raise CondominiumNotFound()

        condo_dict = condominium.to_dict()
        _enrich_condominium_with_unit_stats(condo_dict)

        # AR financial summary
        from library.dddpy.core_accounts_receivable.infrastructure.ar_query_repository import (
            ARQueryRepositoryImpl,
        )
        ar_repo = ARQueryRepositoryImpl()
        ar_summary = ar_repo.get_summary_by_condominium(id)

        return ResponseSuccessSchema(
            success=True,
            message="Condominium summary retrieved",
            data={
                "condominium": condo_dict,
                "financial": ar_summary,
            },
        )

    def list_all(self, skip: int = 0, limit: int = 100, status: Optional[int] = None, city: Optional[str] = None, country: Optional[str] = None, include_deleted: bool = False):
        logger.add_inside_method("list_all")
        condominiums, total = self.condominium_query_usecase.list_all(
            skip=skip, 
            limit=limit, 
            status=status, 
            city=city, 
            country=country,
            include_deleted=include_deleted
        )
        success = ResponseSuccessSchema(
            success=True,
            message=CondominiumSuccessMessage.LISTED,
            data={
                "items": [condominium.to_dict() for condominium in condominiums],
                "total": total,
                "skip": skip,
                "limit": limit,
                "filters": {
                    "status": status,
                    "city": city,
                    "country": country,
                    "include_deleted": include_deleted,
                },
            },
        )
        logger.info(f"{success.message}: {len(condominiums)}/{total} condominiums (skip={skip}, limit={limit})")
        return success
