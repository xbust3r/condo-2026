from chalice import Blueprint, Response

from chalicelib.dddpy.shared.decorators.api_handler import api_handler
from chalicelib.dddpy.shared.logging.logging import Logger

from chalicelib.dddpy.core_buildings_types.usecase.buildings_types_usecase import BuildingsTypesUseCase
from chalicelib.dddpy.core_buildings_types.usecase.buildings_types_cmd_schema import CreateBuildingTypeSchema, UpdateBuildingTypeSchema


logger = Logger("buildings_types API")

PREFIX = "/buildings-types"

buildings_types_routes = Blueprint(__name__)

print(f"Registering {PREFIX} routes")


@buildings_types_routes.route(f"{PREFIX}/health", methods=["GET"])
def health_check() -> Response:
    return Response(status_code=200, body={"status": "healthy"})


@buildings_types_routes.route(f"{PREFIX}", methods=["GET"], cors=True)
@api_handler
def get_all_buildings_types() -> Response:
    logger.add_inside_method("get_all_buildings_types")
    logger.info("Fetching all buildings types")
    
    usecase = BuildingsTypesUseCase()
    result = usecase.get_all()
    
    return Response(
        status_code=200,
        body={"success": True, "data": [r.to_dict() for r in result]}
    )


@buildings_types_routes.route(f"{PREFIX}/{{id}}", methods=["GET"], cors=True)
@api_handler
def get_building_type_by_id(id: int) -> Response:
    logger.add_inside_method("get_building_type_by_id")
    logger.info(f"Fetching building type by id: {id}")
    
    usecase = BuildingsTypesUseCase()
    result = usecase.get_by_id(id)
    
    return Response(
        status_code=200,
        body={"success": True, "data": result.to_dict()}
    )


@buildings_types_routes.route(f"{PREFIX}", methods=["POST"], cors=True)
@api_handler
def create_building_type() -> Response:
    logger.add_inside_method("create_building_type")
    logger.info("Creating new building type")
    
    request = buildings_types_routes.current_request
    data = CreateBuildingTypeSchema.parse_obj(request.json_body)
    
    usecase = BuildingsTypesUseCase()
    result = usecase.create(data)
    
    return Response(
        status_code=201,
        body={"success": result.success, "message": result.message, "data": result.data}
    )


@buildings_types_routes.route(f"{PREFIX}/{{id}}", methods=["PUT"], cors=True)
@api_handler
def update_building_type(id: int) -> Response:
    logger.add_inside_method("update_building_type")
    logger.info(f"Updating building type id: {id}")
    
    request = buildings_types_routes.current_request
    data = UpdateBuildingTypeSchema.parse_obj(request.json_body)
    
    usecase = BuildingsTypesUseCase()
    result = usecase.update(id, data)
    
    return Response(
        status_code=200,
        body={"success": result.success, "message": result.message, "data": result.data}
    )


@buildings_types_routes.route(f"{PREFIX}/{{id}}", methods=["DELETE"], cors=True)
@api_handler
def delete_building_type(id: int) -> Response:
    logger.add_inside_method("delete_building_type")
    logger.info(f"Deleting building type id: {id}")
    
    usecase = BuildingsTypesUseCase()
    result = usecase.delete(id)
    
    return Response(
        status_code=200,
        body={"success": result.success, "message": result.message, "data": result.data}
    )
