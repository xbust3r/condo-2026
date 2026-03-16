from functools import wraps
from chalice import Response, Chalice, Blueprint # <--- Importamos Chalice y Blueprint
from pydantic import ValidationError
import traceback

from chalicelib.dddpy.shared.logging.logging import Logger
from chalicelib.dddpy.shared.schemas.response_schema import ResponseErrorSchema
from chalicelib.dddpy.shared.decorators.domain_exception import DomainException

logger = Logger("Api Handler Decorator")

def get_current_request(func):
    """
    Busca dinámicamente la instancia de Chalice o Blueprint en las variables
    globales de la función decorada para obtener el current_request.
    """
    # Iteramos sobre todas las variables globales del archivo donde está la ruta
    for obj in func.__globals__.values():
        # Verificamos si el objeto es una App de Chalice o un Blueprint
        if isinstance(obj, (Chalice, Blueprint)):
            try:
                # Intentamos obtener el request. Si estamos en un contexto válido,
                # cualquier blueprint o app devolverá el request actual.
                if obj.current_request:
                    return obj.current_request
            except Exception:
                continue
    return None

def api_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 1. Obtener request dinámicamente (Solución al bug)
        request = get_current_request(func)
        
        logger.info(f"--- Start Request: {func.__name__} ---")

        if request:
            try:
                ip_address = request.context.get("identity", {}).get("sourceIp", "unknown")
                resource_path = request.context.get('resourcePath', 'unknown')
                logger.info(f"IP: {ip_address} | Path: {resource_path}")
                # Ten cuidado logueando el body completo si hay datos sensibles
                if request.json_body:
                    logger.info(f"Body: {request.json_body}")
            except Exception as log_error:
                logger.warning(f"Could not log complete request details: {log_error}")
        else:
            logger.warning("Could not detect Chalice current_request context.")

        try:
            # 2. Ejecutar la función original (La ruta)
            return func(*args, **kwargs)

        # 3. Manejo de Excepciones de Dominio
        except DomainException as e:
            logger.warning(f"Domain Exception in {func.__name__}: {str(e)}")
            error_response = ResponseErrorSchema(success=False, message=str(e))
            return Response(body=error_response.dict(), status_code=e.status_code)

        # 4. Manejo de Pydantic
        except ValidationError as e:
            logger.error(f"Validation Error: {e}")
            error_response = ResponseErrorSchema(success=False, message=str(e))
            return Response(body=error_response.dict(), status_code=400)

        # 5. Manejo de Errores Generales (500)
        except Exception as e:
            logger.error(f"Critical Error in {func.__name__}: {str(e)}")
            logger.error(traceback.format_exc())
            error_response = ResponseErrorSchema(
                success=False, message="Internal Server Error"
            )
            return Response(body=error_response.dict(), status_code=500)

    return wrapper