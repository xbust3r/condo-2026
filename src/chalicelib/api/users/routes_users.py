from chalice import Blueprint, Response

from chalicelib.dddpy.shared.decorators.api_handler import api_handler
from chalicelib.dddpy.shared.logging.logging import Logger

from chalicelib.dddpy.users.usecase.users_usecase import UsersUseCase
from chalicelib.dddpy.users.usecase.users_cmd_schema import CreateUserSchema, UpdateUserSchema


logger = Logger("users API")

PREFIX = "/users"

users_routes = Blueprint(__name__)

print(f"Registering {PREFIX} routes")


@users_routes.route(f"{PREFIX}/health", methods=["GET"])
def health_check() -> Response:
    return Response(status_code=200, body={"status": "healthy"})


@users_routes.route(f"{PREFIX}", methods=["GET"], cors=True)
@api_handler
def get_all_users() -> Response:
    logger.add_inside_method("get_all_users")
    logger.info("Fetching all users")
    
    usecase = UsersUseCase()
    result = usecase.get_all()
    
    return Response(
        status_code=200,
        body={"success": True, "data": [r.to_dict() for r in result]}
    )


@users_routes.route(f"{PREFIX}/{{id}}", methods=["GET"], cors=True)
@api_handler
def get_user_by_id(id: int) -> Response:
    logger.add_inside_method("get_user_by_id")
    logger.info(f"Fetching user by id: {id}")
    
    usecase = UsersUseCase()
    result = usecase.get_by_id(id)
    
    return Response(
        status_code=200,
        body={"success": True, "data": result.to_dict()}
    )


@users_routes.route(f"{PREFIX}", methods=["POST"], cors=True)
@api_handler
def create_user() -> Response:
    logger.add_inside_method("create_user")
    logger.info("Creating new user")
    
    request = users_routes.current_request
    data = CreateUserSchema.parse_obj(request.json_body)
    
    usecase = UsersUseCase()
    result = usecase.create(data)
    
    return Response(
        status_code=201,
        body={"success": result.success, "message": result.message, "data": result.data}
    )


@users_routes.route(f"{PREFIX}/{{id}}", methods=["PUT"], cors=True)
@api_handler
def update_user(id: int) -> Response:
    logger.add_inside_method("update_user")
    logger.info(f"Updating user id: {id}")
    
    request = users_routes.current_request
    data = UpdateUserSchema.parse_obj(request.json_body)
    
    usecase = UsersUseCase()
    result = usecase.update(id, data)
    
    return Response(
        status_code=200,
        body={"success": result.success, "message": result.message, "data": result.data}
    )


@users_routes.route(f"{PREFIX}/{{id}}", methods=["DELETE"], cors=True)
@api_handler
def delete_user(id: int) -> Response:
    logger.add_inside_method("delete_user")
    logger.info(f"Deleting user id: {id}")
    
    usecase = UsersUseCase()
    result = usecase.delete(id)
    
    return Response(
        status_code=200,
        body={"success": result.success, "message": result.message, "data": result.data}
    )
