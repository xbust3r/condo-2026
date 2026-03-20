from functools import wraps
from typing import Any, Optional
import traceback

from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from library.dddpy.shared.logging.logging import Logger
from library.dddpy.shared.schemas.response_schema import ResponseErrorSchema
from library.dddpy.shared.decorators.domain_exception import DomainException


logger = Logger("Api Handler Decorator")


def _find_request(args: tuple[Any, ...], kwargs: dict[str, Any]) -> Optional[Request]:
    for arg in args:
        if isinstance(arg, Request):
            return arg

    for value in kwargs.values():
        if isinstance(value, Request):
            return value

    return None


def api_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = _find_request(args, kwargs)

        logger.add_inside_method(func.__name__)
        logger.info("--- Start Request ---")

        if request:
            try:
                forwarded_for = request.headers.get("x-forwarded-for")
                client_ip = forwarded_for.split(",")[0].strip() if forwarded_for else (
                    request.client.host if request.client else "unknown"
                )
                logger.info(
                    f"Method: {request.method} | Path: {request.url.path} | IP: {client_ip}"
                )
            except Exception as log_error:
                logger.warning(f"Could not log complete request details: {log_error}")
        else:
            logger.info("Request context not provided to route.")

        try:
            return func(*args, **kwargs)

        except DomainException as e:
            logger.warning(f"Domain Exception: {str(e)}")
            error_response = ResponseErrorSchema(success=False, message=str(e))
            return JSONResponse(content=error_response.dict(), status_code=e.status_code)

        except ValidationError as e:
            logger.error(f"Validation Error: {e}")
            error_response = ResponseErrorSchema(success=False, message=str(e))
            return JSONResponse(content=error_response.dict(), status_code=400)

        except Exception as e:
            logger.error(f"Critical Error: {str(e)}")
            logger.error(traceback.format_exc())
            error_response = ResponseErrorSchema(
                success=False,
                message="Internal Server Error",
            )
            return JSONResponse(content=error_response.dict(), status_code=500)

    return wrapper
