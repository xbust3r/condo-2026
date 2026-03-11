from chalice import Blueprint, Response

from chalicelib.dddpy.shared.decorators.api_handler import api_handler
from chalicelib.dddpy.shared.logging.logging import Logger

from chalicelib.dddpy.core_unittys_types.usecase.unittys_types_usecase import UnittysTypesUseCase
from chalicelib.dddpy.core_unittys_types.usecase.unittys_types_cmd_schema import CreateUnityTypeSchema, UpdateUnityTypeSchema


logger = Logger("unittys_types API")

PREFIX = "/unitys-types"

unittys_types_routes = Blueprint(__name__)

print(f"Registering {PREFIX} routes")


@unittys_types_routes.route(f"{PREFIX}/health", methods=["GET"])
def health_check() -> Response:
    return Response(status_code=200, body={"status": "healthy"})


@unittys_types_routes.route(f"{PREFIX}", methods=["GET"], cors=True)
@api_handler
def get_all_unittys_types() -> Response:
    logger.add_inside_method("get_all_unittys_types")
    logger.info("Fetching all unitys types")
    
    usecase = UnittysTypesUseCase()
    result = usecase.get_all()
    
    return Response(
        status_code=200,
        body={"success": True, "data": [r.to_dict() for r in result]}
    )


@unittys_types_routes.route(f"{PREFIX}/{{id}}", methods=["GET"], cors=True)
@api_handler
def get_unity_type_by_id(id: int) -> Response:
    logger.add_inside_method("get_unity_type_by_id")
    logger.info(f"Fetching unity type by id: {id}")
    
    usecase = UnittysTypesUseCase()
    result = usecase.get_by_id(id)
    
    return Response(
        status_code=200,
        body={"success": True, "data": result.to_dict()}
    )


@unittys_types_routes.route(f"{PREFIX}", methods=["POST"], cors=True)
@api_handler
def create_unity_type() -> Response:
    logger.add_inside_method("create_unity_type")
    logger.info("Creating new unity type")
    
    request = unittys_types_routes.current_request
    data = CreateUnityTypeSchema.parse_obj(request.json_body)
    
    usecase = UnittysTypesUseCase()
    result = usecase.create(data)
    
    return Response(
        status_code=201,
        body={"success": result.success, "message": result.message, "data": result.data}
    )


@unittys_types_routes.route(f"{PREFIX}/{{id}}", methods=["PUT"], cors=True)
@api_handler
def update_unity_type(id: int) -> Response:
    logger.add_inside_method("update_unity_type")
    logger.info(f"Updating unity type id: {id}")
    
    request = unittys_types_routes.current_request
    data = UpdateUnityTypeSchema.parse_obj(request.json_body)
    
    usecase = UnittysTypesUseCase()
    result = usecase.update(id, data)
    
    return Response(
        status_code=200,
        body={"success": result.success, "message": result.message, "data": result.data}
    )


@unittys_types_routes.route(f"{PREFIX}/{{id}}", methods=["DELETE"], cors=True)
@api_handler
def delete_unity_type(id: int) -> Response:
    logger.add_inside_method("delete_unity_type")
    logger.info(f"Deleting unity type id: {id}")
    
    usecase = UnittysTypesUseCase()
    result = usecase.delete(id)
    
    return Response(
        status_code=200,
        body={"success": result.success, "message": result.message, "data": result.data}
    )
