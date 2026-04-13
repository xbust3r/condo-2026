# =============================================================================
# API Routes: core_condominiums
# Módulo ✅ IMPLEMENTADO — Gestión de condominios
#
# Este módulo sigue el patrón DDD completo:
#   domain/    → entidad, exceptions, repository contracts (cmd/query)
#   infrastructure/ → DB model (SQLAlchemy), mapper, concrete repositories
#   usecase/   → cmd/query schemas, cmd/query use cases, facade (usecase.py), factory
#
# Módulos aún pendientes: core_buildings, core_buildings_types, core_unitys,
#                         core_unittys_types, users, users_residents
# =============================================================================

from fastapi import APIRouter

from library.dddpy.core_condominiums.usecase.condominium_usecase import CondominiumUseCase
from library.dddpy.core_condominiums.usecase.condominium_cmd_schema import CreateCondominiumSchema, UpdateCondominiumSchema
from library.dddpy.shared.decorators.api_handler import api_handler


PREFIX = "/condominiums"

condominium_routes = APIRouter(prefix=PREFIX)


@condominium_routes.get("/health")
def health_check() -> dict:
    return {"status": "healthy"}


@condominium_routes.get("")
@api_handler
def list_condominiums(skip: int = 0, limit: int = 100) -> dict:
    if limit > 500:
        limit = 500  # Safety cap
    response = CondominiumUseCase().list_all(skip=skip, limit=limit)
    return response.dict()


@condominium_routes.get("/{id}")
@api_handler
def get_condominium(id: int) -> dict:
    response = CondominiumUseCase().get_by_id(id)
    return response.dict()


@condominium_routes.get("/uuid/{uuid}")
@api_handler
def get_condominium_by_uuid(uuid: str) -> dict:
    response = CondominiumUseCase().get_by_uuid(uuid)
    return response.dict()


@condominium_routes.get("/code/{code}")
@api_handler
def get_condominium_by_code(code: str) -> dict:
    response = CondominiumUseCase().get_by_code(code)
    return response.dict()


@condominium_routes.post("")
@api_handler
def create_condominium(request: CreateCondominiumSchema) -> dict:
    response = CondominiumUseCase().create(request)
    return response.dict()


@condominium_routes.put("/{id}")
@api_handler
def update_condominium(id: int, request: UpdateCondominiumSchema) -> dict:
    response = CondominiumUseCase().update(id, request)
    return response.dict()


@condominium_routes.delete("/{id}")
@api_handler
def delete_condominium(id: int) -> dict:
    response = CondominiumUseCase().delete(id)
    return response.dict()
