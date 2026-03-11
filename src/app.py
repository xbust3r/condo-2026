from chalice import Chalice, Response
import os

from chalicelib.api.lead.routes_lead import lead_routes
from chalicelib.api.routing.routes_routing import routing_routes
from chalicelib.api.condominiums.routes_condominiums import condominiums_routes
from chalicelib.api.buildings.routes_buildings import buildings_routes
from chalicelib.api.buildings_types.routes_buildings_types import buildings_types_routes
from chalicelib.api.unitys.routes_unitys import unitys_routes
from chalicelib.api.unittys_types.routes_unittys_types import unittys_types_routes
from chalicelib.api.users.routes_users import users_routes
from chalicelib.api.residents.routes_residents import residents_routes

from chalicelib.dddpy.shared.logging.logging import Logger

app = Chalice(app_name='zatanna-routing')
logger = Logger('app')

# Verificar cabeceras y agregar cabeceras globales
@app.middleware('http')
def verify_and_add_headers(event, get_response):
    request_headers = event.headers or {}
    api_user = request_headers.get('API_USER')
    api_key = request_headers.get('API_KEY')
    expected_user = os.environ.get('API_USER')
    expected_key = os.environ.get('API_KEY')

    if api_user != expected_user or api_key != expected_key:
        logger.error(f"Unauthorized access attempt. User: {api_user}, Key: {api_key}")
        return Response(status_code=500, body={"error": "KEYS NOT AUTORIZED"})

    try:
        response = get_response(event)
        response.headers['API_USER'] = expected_user
        response.headers['API_KEY'] = expected_key
        return response
    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}")
        raise e

app.register_blueprint(routing_routes)
app.register_blueprint(condominiums_routes)
app.register_blueprint(buildings_routes)
app.register_blueprint(buildings_types_routes)
app.register_blueprint(unitys_routes)
app.register_blueprint(unittys_types_routes)
app.register_blueprint(users_routes)
app.register_blueprint(residents_routes)

@app.route('/')
def index():
    return {'hello': 'world'}
