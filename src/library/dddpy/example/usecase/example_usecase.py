from library.dddpy.example.usecase.example_cmd_usecase import ExampleCmdUseCase
from library.dddpy.example.usecase.example_query_usecase import ExampleQueryUseCase
from library.dddpy.example.usecase.example_factory import example_cmd_usecase_factory, example_query_usecase_factory
from library.dddpy.example.usecase.example_cmd_schema import CreateExampleSchema, UpdateExampleSchema
from library.dddpy.example.domain.example_exception import ExampleNotFound, RepeatedExampleCode
from library.dddpy.example.domain.example_success import ExampleSuccessMessage
from library.dddpy.shared.schemas.response_schema import ResponseSuccessSchema
from library.dddpy.shared.logging.logging import Logger


logger = Logger("ExampleUseCase")


class ExampleUseCase:
    def __init__(self):
        logger.add_inside_method("__init__")
        self.example_cmd_usecase: ExampleCmdUseCase = example_cmd_usecase_factory()
        self.example_query_usecase: ExampleQueryUseCase = example_query_usecase_factory()
        logger.info("ExampleUseCase initialized")

    def create(self, example_data: CreateExampleSchema):
        logger.add_inside_method("create")
        logger.info(f"Creating example with data: {example_data}")
        existing = self.example_query_usecase.get_by_code(example_data.code)
        if existing:
            logger.warning(f"Example code already exists: {example_data.code}")
            raise RepeatedExampleCode()
        new_example = self.example_cmd_usecase.create(example_data)
        success = ResponseSuccessSchema(
            success=True,
            message=ExampleSuccessMessage.CREATED,
            data=new_example.to_dict(),
        )
        logger.info(f"{success.message}: {success}")
        return success

    def get_by_id(self, id: int):
        logger.add_inside_method("get_by_id")
        example = self.example_query_usecase.get_by_id(id)
        if not example:
            logger.warning(f"Example not found by id={id}")
            raise ExampleNotFound()
        success = ResponseSuccessSchema(
            success=True,
            message=ExampleSuccessMessage.RETRIEVED,
            data=example.to_dict(),
        )
        logger.info(f"{success.message} by id={id}")
        return success

    def get_by_code(self, code: str):
        logger.add_inside_method("get_by_code")
        example = self.example_query_usecase.get_by_code(code)
        if not example:
            logger.warning(f"Example not found by code={code}")
            raise ExampleNotFound()
        success = ResponseSuccessSchema(
            success=True,
            message=ExampleSuccessMessage.RETRIEVED,
            data=example.to_dict(),
        )
        logger.info(f"{success.message} by code={code}")
        return success

    def update(self, id: int, example_data: UpdateExampleSchema):
        logger.add_inside_method("update")
        logger.info(f"Updating example id={id} with data: {example_data}")
        updated_example = self.example_cmd_usecase.update(id, example_data)
        if not updated_example:
            logger.warning(f"Example not found for update id={id}")
            raise ExampleNotFound()
        success = ResponseSuccessSchema(
            success=True,
            message=ExampleSuccessMessage.UPDATED,
            data=updated_example.to_dict(),
        )
        logger.info(f"{success.message}: {success}")
        return success

    def delete(self, id: int):
        logger.add_inside_method("delete")
        logger.info(f"Deleting example id={id}")
        deleted = self.example_cmd_usecase.delete(id)
        if not deleted:
            logger.warning(f"Example not found for delete id={id}")
            raise ExampleNotFound()
        success = ResponseSuccessSchema(
            success=True,
            message=ExampleSuccessMessage.DELETED,
            data={},
        )
        logger.info(f"{success.message} for id={id}")
        return success

    def list_all(self):
        logger.add_inside_method("list_all")
        examples = self.example_query_usecase.list_all()
        success = ResponseSuccessSchema(
            success=True,
            message=ExampleSuccessMessage.LISTED,
            data=[example.to_dict() for example in examples],
        )
        logger.info(f"{success.message}: {len(examples)} examples")
        return success
