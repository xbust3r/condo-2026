from chalice import Blueprint, Response

from chalicelib.dddpy.shared.decorators.api_handler import api_handler
from chalicelib.dddpy.shared.logging.logging import Logger

from chalicelib.dddpy.core_unitys.usecase.unitys_usecase import UnitysUseCase
from chalicelib.dddpy.core_unitys.usecase.unitys_cmd_schema import CreateUnitySchema, UpdateUnitySchema


logger = Logger("unitys API")

PREFIX = "/unitys"

unitys_routes = Blueprint(__name__)

print(f"Registering {PREFIX} routes")


@unitys_routes.route(f"{PREFIX}/health", methods=["GET"])
def health_check() -> Response:
    return Response(status_code=200, body={"status": "healthy"})


@unitys_routes.route(f"{PREFIX}", methods=["GET"], cors=True)
@api_handler
def get_all_unitys() -> Response:
    logger.add_inside_method("get_all_unitys")
    logger.info("Fetching all unitys")
    
    usecase = UnitysUseCase()
    result = usecase.get_all()
    
    return Response(
        status_code=200,
        body={"success": True, "data": [r.to_dict() for r in result]}
    )


@unitys_routes.route(f"{PREFIX}/{{id}}", methods=["GET"], cors=True)
@api_handler
def get_unity_by_id(id: int) -> Response:
    logger.add_inside_method("get_unity_by_id")
    logger.info(f"Fetching unity by id: {id}")
    
    usecase = UnitysUseCase()
    result = usecase.get_by_id(id)
    
    return Response(
        status_code=200,
        body={"success": True, "data": result.to_dict()}
    )


@unitys_routes.route(f"{PREFIX}", methods=["POST"], cors=True)
@api_handler
def create_unity() -> Response:
    logger.add_inside_method("create_unity")
    logger.info("Creating new unity")
    
    request = unitys_routes.current_request
    data = CreateUnitySchema.parse_obj(request.json_body)
    
    usecase = UnitysUseCase()
    result = usecase.create(data)
    
    return Response(
        status_code=201,
        body={"success": result.success, "message": result.message, "data": result.data}
    )


@unitys_routes.route(f"{PREFIX}/{{id}}", methods=["PUT"], cors=True)
@api_handler
def update_unity(id: int) -> Response:
    logger.add_inside_method("update_unity")
    logger.info(f"Updating unity id: {id}")
    
    request = unitys_routes.current_request
    data = UpdateUnitySchema.parse_obj(request.json_body)
    
    usecase = UnitysUseCase()
    result = usecase.update(id, data)
    
    return Response(
        status_code=200,
        body={"success": result.success, "message": result.message, "data": result.data}
    )


@unitys_routes.route(f"{PREFIX}/{{id}}", methods=["DELETE"], cors=True)
@api_handler
def delete_unity(id: int) -> Response:
    logger.add_inside_method("delete_unity")
    logger.info(f"Deleting unity id: {id}")
    
    usecase = UnitysUseCase()
    result = usecase.delete(id)
    
    return Response(
        status_code=200,
        body={"success": result.success, "message": result.message, "data": result.data}
    )
