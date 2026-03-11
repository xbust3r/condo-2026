from chalice import Blueprint, Response

from chalicelib.dddpy.shared.decorators.api_handler import api_handler
from chalicelib.dddpy.shared.logging.logging import Logger

from chalicelib.dddpy.core_condominiums.usecase.condominiums_usecase import CondominiumsUseCase
from chalicelib.dddpy.core_condominiums.usecase.condominiums_cmd_schema import CreateCondominiumSchema, UpdateCondominiumSchema


logger = Logger("condominiums API")

PREFIX = "/condominiums"

condominiums_routes = Blueprint(__name__)

print(f"Registering {PREFIX} routes")


@condominiums_routes.route(f"{PREFIX}/health", methods=["GET"])
def health_check() -> Response:
    return Response(status_code=200, body={"status": "healthy"})


@condominiums_routes.route(f"{PREFIX}", methods=["GET"], cors=True)
@api_handler
def get_all_condominiums() -> Response:
    logger.add_inside_method("get_all_condominiums")
    logger.info("Fetching all condominiums")
    
    usecase = CondominiumsUseCase()
    result = usecase.get_all()
    
    return Response(
        status_code=200,
        body={"success": True, "data": [r.to_dict() for r in result]}
    )


@condominiums_routes.route(f"{PREFIX}/{{id}}", methods=["GET"], cors=True)
@api_handler
def get_condominium_by_id(id: int) -> Response:
    logger.add_inside_method("get_condominium_by_id")
    logger.info(f"Fetching condominium by id: {id}")
    
    usecase = CondominiumsUseCase()
    result = usecase.get_by_id(id)
    
    return Response(
        status_code=200,
        body={"success": True, "data": result.to_dict()}
    )


@condominiums_routes.route(f"{PREFIX}", methods=["POST"], cors=True)
@api_handler
def create_condominium() -> Response:
    logger.add_inside_method("create_condominium")
    logger.info("Creating new condominium")
    
    request = condominiums_routes.current_request
    data = CreateCondominiumSchema.parse_obj(request.json_body)
    
    usecase = CondominiumsUseCase()
    result = usecase.create(data)
    
    return Response(
        status_code=201,
        body={"success": result.success, "message": result.message, "data": result.data}
    )


@condominiums_routes.route(f"{PREFIX}/{{id}}", methods=["PUT"], cors=True)
@api_handler
def update_condominium(id: int) -> Response:
    logger.add_inside_method("update_condominium")
    logger.info(f"Updating condominium id: {id}")
    
    request = condominiums_routes.current_request
    data = UpdateCondominiumSchema.parse_obj(request.json_body)
    
    usecase = CondominiumsUseCase()
    result = usecase.update(id, data)
    
    return Response(
        status_code=200,
        body={"success": result.success, "message": result.message, "data": result.data}
    )


@condominiums_routes.route(f"{PREFIX}/{{id}}", methods=["DELETE"], cors=True)
@api_handler
def delete_condominium(id: int) -> Response:
    logger.add_inside_method("delete_condominium")
    logger.info(f"Deleting condominium id: {id}")
    
    usecase = CondominiumsUseCase()
    result = usecase.delete(id)
    
    return Response(
        status_code=200,
        body={"success": result.success, "message": result.message, "data": result.data}
    )
