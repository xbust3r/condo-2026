from fastapi import APIRouter

from library.dddpy.shared.logging.logging import Logger
from library.dddpy.example.usecase.example_usecase import ExampleUseCase
from library.dddpy.example.usecase.example_cmd_schema import CreateExampleSchema, UpdateExampleSchema
from library.dddpy.shared.decorators.api_handler import api_handler


logger = Logger("ACA Routes - Example")

PREFIX = "/example"

example_routes = APIRouter(prefix=PREFIX)

logger.info(f"Registering {PREFIX} routes")


@example_routes.get("/health")
@api_handler
def health_check() -> dict:
    return {"status": "healthy"}


@example_routes.get("")
@api_handler
def list_examples() -> dict:
    logger.add_inside_method("list_examples Route")
    logger.info("Listing all examples")
    response = ExampleUseCase().list_all()
    return response.dict()


@example_routes.get("/{id}")
@api_handler
def get_example(id: int) -> dict:
    logger.add_inside_method("get_example Route")
    logger.info(f"Getting example with ID: {id}")
    response = ExampleUseCase().get_by_id(id)
    return response.dict()


@example_routes.get("/code/{code}")
@api_handler
def get_example_by_code(code: str) -> dict:
    logger.add_inside_method("get_example_by_code Route")
    logger.info(f"Getting example with code: {code}")
    response = ExampleUseCase().get_by_code(code)
    return response.dict()


@example_routes.post("")
@api_handler
def create_example(request: CreateExampleSchema) -> dict:
    logger.add_inside_method("create_example Route")
    logger.info("Creating new example")
    response = ExampleUseCase().create(request)
    return response.dict()


@example_routes.put("/{id}")
@api_handler
def update_example(id: int, request: UpdateExampleSchema) -> dict:
    logger.add_inside_method("update_example Route")
    logger.info(f"Updating example with ID: {id}")
    response = ExampleUseCase().update(id, request)
    return response.dict()


@example_routes.delete("/{id}")
@api_handler
def delete_example(id: int) -> dict:
    logger.add_inside_method("delete_example Route")
    logger.info(f"Deleting example with ID: {id}")
    response = ExampleUseCase().delete(id)
    return response.dict()
