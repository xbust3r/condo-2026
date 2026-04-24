# FastAPI Main Application
# =============================================================================
# condo-py — Sistema de Gestión para Condominios
# =============================================================================
from dotenv import load_dotenv
import os
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
#
# ESTADO DE MÓDULOS DEL SISTEMA
# ----------------------------
#
# PLANTILLA DE REFERENCIA (completos):
#   ✅ shared/             — Componentes compartidos (decorators, schemas, logging, mysql, postgresql, utils, constants)
#   ✅ example/            — Módulo patrón de referencia DDD (domain/infrastructure/usecase completo)
#
# MÓDULOS IMPLEMENTADOS EN PYTHON:
#   ✅ core_condominiums/  — Gestión de condominios (domain + infrastructure + usecase + api/routes)
#   ✅ core_buildings/     — Torres/edificios (domain + infrastructure + usecase + api/routes)
#   ✅ core_buildings_types/ — Catálogo de tipos de edificio con scope global/custom (DDD completo)
#   ✅ core_units/         — Unidades inmobiliarias (domain + infrastructure + usecase + api/routes)
#   ✅ core_unit_types/    — Catálogo de tipos de unidad con scope global/custom (DDD completo)
#   ✅ users/              — Usuarios del sistema (auth + CRUD)
#   ✅ user_profiles/      — Perfil humano (DDD + API)
#   ✅ core_unit_ownerships/   — Propiedad de unidades (DDD completo)
#   ✅ core_unit_occupancies/  — Ocupación de unidades (DDD completo)
#   ✅ core_condominium_roles/ — Roles administrativos (DDD completo)
#   ✅ core_occupancy_types/   — Catálogo de tipos de ocupación (DDD completo)
#   ✅ core_charge_types/     — Catálogo de tipos de cargo (DDD completo)
#   ✅ core_charges/          — Cargos recurrentes y extraordinarios (DDD completo)
#   ✅ core_accounts_receivable/ — Cuentas por cobrar (DDD completo)
#   ✅ core_receipts/          — Recibos de pago (DDD completo)
#   ✅ core_payments/         — Pagos contra AR (DDD completo)
#   ✅ core_ledger_entries/  — Libro mayor por unidad (DDD completo)
#
# ESTRUCTURA DDD ESPERADA POR MÓDULO:
#   {modulo}/
#   ├── domain/
#   │   ├── {modulo}_entity.py
#   │   ├── {modulo}_data.py
#   │   ├── {modulo}_exception.py
#   │   ├── {modulo}_success.py
#   │   ├── {modulo}_repository.py
#   │   ├── {modulo}_cmd_repository.py
#   │   └── {modulo}_query_repository.py
#   ├── infrastructure/
#   │   ├── db{modulo}.py
#   │   ├── {modulo}_mapper.py
#   │   ├── {modulo}_cmd_repository.py
#   │   └── {modulo}_query_repository.py
#   └── usecase/
#       ├── {modulo}_cmd_schema.py
#       ├── {modulo}_cmd_usecase.py
#       ├── {modulo}_query_usecase.py
#       ├── {modulo}_usecase.py
#       └── {modulo}_factory.py
#
# API ROUTES esperadas:
#   {modulo}_routes.py en api/{modulo}/
#
# =============================================================================

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from library.dddpy.shared.schemas.response_schema import ResponseSchema
import os
from mangum import Mangum

# Import routers
from api.condominiums.routes_condominiums import condominium_routes
from api.buildings.routes_buildings import building_routes
from api.buildings_types.routes_building_types import building_type_routes
from api.units.routes_units import unit_routes
from api.unit_types.routes_unit_types import unit_type_routes, public_unit_type_routes
from api.unit_ownerships.routes_unit_ownerships import unit_ownership_routes
from api.unit_occupancies.routes_unit_occupancies import unit_occupancy_routes
from api.condominium_roles.routes_condominium_roles import condominium_role_routes
from api.occupancy_types.routes_occupancy_types import occupancy_type_routes
from api.permissions.routes_permissions import permission_routes
from api.role_permissions.routes_role_permissions import role_permission_routes
from api.auth.routes_auth import auth_routes
from api.users.routes_users import user_routes
from api.user_profiles.routes_user_profiles import user_profile_routes
from api.contexts.routes_contexts import context_routes
from api.example.routes_example import example_routes
from api.charge_types.routes_charge_types import charge_type_routes
from api.charges.routes_charges import charge_routes
from api.accounts_receivable.routes_accounts_receivable import ar_routes
from api.receipts.routes_receipts import receipt_routes
from api.payments.routes_payments import payment_routes
from api.ledger_entries.routes_ledger import ledger_routes
from api.announcements.routes_announcements import announcement_routes
from api.meetings.routes_meetings import meeting_routes
from api.documents.routes_documents import document_routes
from api.incidents.routes_incidents import incident_routes, condominium_incident_routes
from api.notifications.routes_notifications import notification_routes
from api.visitors.routes_visitors import visitor_routes, condominium_visitor_routes
from api.amenities.routes_amenities import amenity_routes
from api.packages.routes_packages import package_routes
from api.residents.routes_residents import resident_routes
from api.audit_logs.routes_audit_logs import audit_log_routes


app = FastAPI(
    title="Condo-Py API",
    description="Backend for Condominium Management System",
    version="1.0.0",
)

# CORS middleware
# ⚠️ CRÍTICO: allow_credentials=True NO es compatible con allow_origins=["*"]
# según el estándar Fetch. En producción usar orígenes específicos, ej.:
#   ALLOWED_ORIGINS = ["https://app.tudominio.com", "https://admin.tudominio.com"]
# Si no necesitás credenciales (cookies/auth headers), cambiá allow_credentials a False.
import os
ALLOWED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ResponseSchema(
            success=False,
            message="Internal server error",
            errors=[str(exc)]
        ).dict()
    )



# Health check
@app.get("/health")
def health_check():
    return ResponseSchema(success=True, message="API is running", data={"status": "healthy"})


# Include routers
app.include_router(condominium_routes)
app.include_router(building_routes)
app.include_router(building_type_routes)
app.include_router(unit_routes)
app.include_router(unit_type_routes)
app.include_router(public_unit_type_routes)
app.include_router(unit_ownership_routes)
app.include_router(unit_occupancy_routes)
app.include_router(condominium_role_routes)
app.include_router(occupancy_type_routes)
app.include_router(charge_type_routes)
app.include_router(charge_routes)
app.include_router(ar_routes)
app.include_router(receipt_routes)
app.include_router(payment_routes)
app.include_router(ledger_routes)
app.include_router(announcement_routes)
app.include_router(meeting_routes)
app.include_router(document_routes)
app.include_router(incident_routes)
app.include_router(condominium_incident_routes)
app.include_router(notification_routes)
app.include_router(visitor_routes)
app.include_router(condominium_visitor_routes)
app.include_router(amenity_routes)
app.include_router(package_routes)
app.include_router(resident_routes)
app.include_router(permission_routes)
app.include_router(role_permission_routes)
app.include_router(auth_routes)
app.include_router(user_routes)
app.include_router(user_profile_routes)
app.include_router(context_routes)
app.include_router(audit_log_routes)
app.include_router(example_routes)