from chalice import Blueprint, Response

from chalicelib.dddpy.shared.decorators.api_handler import api_handler
from chalicelib.dddpy.shared.logging.logging import Logger

from chalicelib.dddpy.core_buildings.usecase.buildings_usecase import BuildingsUseCase
from chalicelib.dddpy.core_buildings.usecase.buildings_cmd_schema import CreateBuildingSchema, UpdateBuildingSchema


logger = Logger("buildings API")

PREFIX = "/buildings"

buildings_routes = Blueprint(__name__)

print(f"Registering {PREFIX} routes")


@buildings_routes.route(f"{PREFIX}/health", methods=["GET"])
def health_check() -> Response:
    return Response(status_code=200, body={"status": "healthy"})


@buildings_routes.route(f"{PREFIX}", methods=["GET"], cors=True)
@api_handler
def get_all_buildings() -> Response:
    logger.add_inside_method("get_all_buildings")
    logger.info("Fetching all buildings")
    
    usecase = BuildingsUseCase()
    result = usecase.get_all()
    
    return Response(
        status_code=200,
        body={"success": True, "data": [r.to_dict() for r in result]}
    )


@buildings_routes.route(f"{PREFIX}/{{id}}", methods=["GET"], cors=True)
@api_handler
def get_building_by_id(id: int) -> Response:
    logger.add_inside_method("get_building_by_id")
    logger.info(f"Fetching building by id: {id}")
    
    usecase = BuildingsUseCase()
    result = usecase.get_by_id(id)
    
    return Response(
        status_code=200,
        body={"success": True, "data": result.to_dict()}
    )


@buildings_routes.route(f"{PREFIX}", methods=["POST"], cors=True)
@api_handler
def create_building() -> Response:
    logger.add_inside_method("create_building")
    logger.info("Creating new building")
    
    request = buildings_routes.current_request
    data = CreateBuildingSchema.parse_obj(request.json_body)
    
    usecase = BuildingsUseCase()
    result = usecase.create(data)
    
    return Response(
        status_code=201,
        body={"success": result.success, "message": result.message, "data": result.data}
    )


@buildings_routes.route(f"{PREFIX}/{{id}}", methods=["PUT"], cors=True)
@api_handler
def update_building(id: int) -> Response:
    logger.add_inside_method("update_building")
    logger.info(f"Updating building id: {id}")
    
    request = buildings_routes.current_request
    data = UpdateBuildingSchema.parse_obj(request.json_body)
    
    usecase = BuildingsUseCase()
    result = usecase.update(id, data)
    
    return Response(
        status_code=200,
        body={"success": result.success, "message": result.message, "data": result.data}
    )


@buildings_routes.route(f"{PREFIX}/{{id}}", methods=["DELETE"], cors=True)
@api_handler
def delete_building(id: int) -> Response:
    logger.add_inside_method("delete_building")
    logger.info(f"Deleting building id: {id}")
    
    usecase = BuildingsUseCase()
    result = usecase.delete(id)
    
    return Response(
        status_code=200,
        body={"success": result.success, "message": result.message, "data": result.data}
    )
