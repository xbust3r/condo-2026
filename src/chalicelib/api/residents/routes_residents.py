from chalice import Blueprint, Response

from chalicelib.dddpy.shared.decorators.api_handler import api_handler
from chalicelib.dddpy.shared.logging.logging import Logger

from chalicelib.dddpy.users_residents.usecase.residents_usecase import UsersResidentsUseCase
from chalicelib.dddpy.users_residents.usecase.residents_cmd_schema import CreateResidentSchema, UpdateResidentSchema


logger = Logger("residents API")

PREFIX = "/residents"

residents_routes = Blueprint(__name__)

print(f"Registering {PREFIX} routes")


@residents_routes.route(f"{PREFIX}/health", methods=["GET"])
def health_check() -> Response:
    return Response(status_code=200, body={"status": "healthy"})


@residents_routes.route(f"{PREFIX}", methods=["GET"], cors=True)
@api_handler
def get_all_residents() -> Response:
    logger.add_inside_method("get_all_residents")
    logger.info("Fetching all residents")
    
    usecase = UsersResidentsUseCase()
    result = usecase.get_all()
    
    return Response(
        status_code=200,
        body={"success": True, "data": [r.to_dict() for r in result]}
    )


@residents_routes.route(f"{PREFIX}/{{id}}", methods=["GET"], cors=True)
@api_handler
def get_resident_by_id(id: int) -> Response:
    logger.add_inside_method("get_resident_by_id")
    logger.info(f"Fetching resident by id: {id}")
    
    usecase = UsersResidentsUseCase()
    result = usecase.get_by_id(id)
    
    return Response(
        status_code=200,
        body={"success": True, "data": result.to_dict()}
    )


@residents_routes.route(f"{PREFIX}", methods=["POST"], cors=True)
@api_handler
def create_resident() -> Response:
    logger.add_inside_method("create_resident")
    logger.info("Creating new resident")
    
    request = residents_routes.current_request
    data = CreateResidentSchema.parse_obj(request.json_body)
    
    usecase = UsersResidentsUseCase()
    result = usecase.create(data)
    
    return Response(
        status_code=201,
        body={"success": result.success, "message": result.message, "data": result.data}
    )


@residents_routes.route(f"{PREFIX}/{{id}}", methods=["PUT"], cors=True)
@api_handler
def update_resident(id: int) -> Response:
    logger.add_inside_method("update_resident")
    logger.info(f"Updating resident id: {id}")
    
    request = residents_routes.current_request
    data = UpdateResidentSchema.parse_obj(request.json_body)
    
    usecase = UsersResidentsUseCase()
    result = usecase.update(id, data)
    
    return Response(
        status_code=200,
        body={"success": result.success, "message": result.message, "data": result.data}
    )


@residents_routes.route(f"{PREFIX}/{{id}}", methods=["DELETE"], cors=True)
@api_handler
def delete_resident(id: int) -> Response:
    logger.add_inside_method("delete_resident")
    logger.info(f"Deleting resident id: {id}")
    
    usecase = UsersResidentsUseCase()
    result = usecase.delete(id)
    
    return Response(
        status_code=200,
        body={"success": result.success, "message": result.message, "data": result.data}
    )
