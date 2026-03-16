from chalice import Blueprint, Response

from chalicelib.dddpy.shared.logging.logging import Logger
from chalicelib.dddpy.example.usecase.example_usecase import ExampleUseCase
from chalicelib.dddpy.example.usecase.example_cmd_schema import CreateExampleSchema, UpdateExampleSchema
from chalicelib.dddpy.shared.decorators.api_handler import api_handler


logger = Logger("ACA Routes - Example")

PREFIX = "/example"

example_routes = Blueprint(__name__)

logger.info(f"Registering {PREFIX} routes")


@example_routes.route(f"{PREFIX}/health", methods=["GET"])
@api_handler
def health_check() -> Response:
    return Response(status_code=200, body={"status": "healthy"})


@example_routes.route(f"{PREFIX}", methods=["GET"], cors=True)
@api_handler
def list_examples() -> Response:
    logger.add_inside_method("list_examples Route")
    logger.info("Listing all examples")
    response = ExampleUseCase().list_all()
    return response.dict()


@example_routes.route(f"{PREFIX}/{{id}}", methods=["GET"], cors=True)
@api_handler
def get_example(id: str) -> Response:
    logger.add_inside_method("get_example Route")
    logger.info(f"Getting example with ID: {id}")
    example_id = int(id)
    response = ExampleUseCase().get_by_id(example_id)
    return response.dict()


@example_routes.route(f"{PREFIX}/code/{{code}}", methods=["GET"], cors=True)
@api_handler
def get_example_by_code(code: str) -> Response:
    logger.add_inside_method("get_example_by_code Route")
    logger.info(f"Getting example with code: {code}")
    response = ExampleUseCase().get_by_code(code)
    return response.dict()


@example_routes.route(f"{PREFIX}", methods=["POST"], cors=True)
@api_handler
def create_example() -> Response:
    logger.add_inside_method("create_example Route")
    logger.info("Creating new example")
    request = example_routes.current_request
    data = CreateExampleSchema.parse_obj(request.json_body)
    response = ExampleUseCase().create(data)
    return response.dict()


@example_routes.route(f"{PREFIX}/{{id}}", methods=["PUT"], cors=True)
@api_handler
def update_example(id: str) -> Response:
    logger.add_inside_method("update_example Route")
    logger.info(f"Updating example with ID: {id}")
    request = example_routes.current_request
    example_id = int(id)
    data = UpdateExampleSchema.parse_obj(request.json_body)
    response = ExampleUseCase().update(example_id, data)
    return response.dict()


@example_routes.route(f"{PREFIX}/{{id}}", methods=["DELETE"], cors=True)
@api_handler
def delete_example(id: str) -> Response:
    logger.add_inside_method("delete_example Route")
    logger.info(f"Deleting example with ID: {id}")
    example_id = int(id)
    response = ExampleUseCase().delete(example_id)
    return response.dict()
