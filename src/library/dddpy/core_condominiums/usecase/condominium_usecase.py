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
        success = ResponseSuccessSchema(
            success=True,
            message=CondominiumSuccessMessage.RETRIEVED,
            data=condominium.to_dict(),
        )
        logger.info(f"{success.message} by id={id}")
        return success

    def get_by_uuid(self, uuid: str):
        logger.add_inside_method("get_by_uuid")
        condominium = self.condominium_query_usecase.get_by_uuid(uuid)
        if not condominium:
            logger.warning(f"Condominium not found by uuid={uuid}")
            raise CondominiumNotFound()
        success = ResponseSuccessSchema(
            success=True,
            message=CondominiumSuccessMessage.RETRIEVED,
            data=condominium.to_dict(),
        )
        logger.info(f"{success.message} by uuid={uuid}")
        return success

    def get_by_code(self, code: str):
        logger.add_inside_method("get_by_code")
        condominium = self.condominium_query_usecase.get_by_code(code)
        if not condominium:
            logger.warning(f"Condominium not found by code={code}")
            raise CondominiumNotFound()
        success = ResponseSuccessSchema(
            success=True,
            message=CondominiumSuccessMessage.RETRIEVED,
            data=condominium.to_dict(),
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
        success = ResponseSuccessSchema(
            success=True,
            message=CondominiumSuccessMessage.DELETED,
            data={"id": id, "deleted_at": existing.deleted_at},
        )
        logger.info(f"{success.message} for id={id}")
        return success

    def restore(self, id: int):
        logger.add_inside_method("restore")
        logger.info(f"Restoring condominium id={id}")
        restored = self.condominium_cmd_usecase.repository.restore(id)
        if not restored:
            logger.warning(f"Failed to restore condominium id={id}")
            raise CondominiumNotFound()
        condominium = self.condominium_query_usecase.get_by_id(id)
        success = ResponseSuccessSchema(
            success=True,
            message="Condominium restored successfully",
            data=condominium.to_dict(),
        )
        logger.info(f"{success.message} for id={id}")
        return success

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
