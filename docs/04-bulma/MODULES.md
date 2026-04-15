# Módulos del Sistema condo-py

## Estado General

| Estado | Significado |
|--------|-------------|
| ✅ | Implementado completamente en Python |
| ❌ | Pendiente — documentado en README.md pero sin código Python |
| 📋 | Plantilla de referencia (no agregar lógica de negocio) |

---

## Módulos Implementados

### ✅ `shared/` — Componentes Compartidos
**Ruta:** `src/library/dddpy/shared/`

Componentes transversales:
- `decorators/` — `api_handler.py`, `domain_exception.py`
- `schemas/` — `response_schema.py` (ResponseSuccessSchema, ResponseErrorSchema)
- `logging/` — `logging.py`
- `mysql/` — `base.py`, `session_manager.py`
- `postgresql/` — `base.py`, `session_manager.py`
- `constants/` — `status_constants.py`
- `utils/` — `images.py`, `password.py`, `urls.py`, `uploads.py`, `validate_email.py`
- `timezone.py`

---

### 📋 `example/` — Plantilla de Referencia DDD
**Ruta:** `src/library/dddpy/example/`

Este módulo **NO es lógica de negocio real**. Es la plantilla que define el patrón arquitectónico.

```
example/
├── domain/
│   ├── example_entity.py
│   ├── example_data.py
│   ├── example_exception.py
│   ├── example_success.py
│   ├── example_repository.py
│   ├── example_cmd_repository.py
│   └── example_query_repository.py
├── infrastructure/
│   ├── dbexample.py
│   ├── example_mapper.py
│   ├── example_cmd_repository.py
│   └── example_query_repository.py
└── usecase/
    ├── example_cmd_schema.py
    ├── example_cmd_usecase.py
    ├── example_query_usecase.py
    ├── example_usecase.py (facade)
    └── example_factory.py
```

Rutas API: `src/api/example/routes_example.py`

---

### ✅ `core_condominiums/` — Gestión de Condominios
**Ruta:** `src/library/dddpy/core_condominiums/`

Módulo funcional completo (domain + infrastructure + usecase).

Rutas API: `src/api/condominiums/routes_condominiums.py`

---

## Módulos Pendientes de Implementar

### ✅ `core_buildings/` — Torres/Edificios
**Ruta:** `src/library/dddpy/core_buildings/`
**Rutas API:** `src/api/buildings/routes_buildings.py`

### ✅ `core_buildings_types/` — Tipos de Edificio
**Ruta:** `src/library/dddpy/core_buildings_types/`
**Rutas API:** `src/api/buildings_types/routes_building_types.py`

### ✅ `core_units/` — Unidades Inmobiliarias
**Ruta:** `src/library/dddpy/core_units/`
**Rutas API:** `src/api/units/routes_units.py`

### ✅ `core_unit_types/` — Tipos de Unidad
**Ruta:** `src/library/dddpy/core_unit_types/`
**Rutas API:** `src/api/unit_types/routes_unit_types.py`

### ✅ `users/` — Usuarios del Sistema
**Tabla:** `users` (auth: email, password_hash, status, security fields)

### ✅ `user_profiles/` — Perfil Humano
**Tabla:** `user_profiles` (1:1 con users: first_name, last_name, doc_identity, phone)

### 🔄 `core_unit_ownerships/` — Titularidad de Unidades
**En construcción:** DDD module + migration 012

### 🔄 `core_unit_occupancies/` — Ocupación de Unidades
**En construcción:** DDD module + migration 013

### 🔄 `core_condominium_roles/` — Roles por Condominio
**En construcción:** DDD module + migration 014

### ❌ `users_residents/` — Tabla Deprecada
**Estado:** ⚠️ DEPRECADO — solo referencia histórica. NO usar en código nuevo.
**Tabla DB:** `users_residents` — presente como fallback hasta validación con datos reales.
**Eliminación física:** pendiente de validación (Bloque D — standby).
**Reemplazo:** `core_unit_ownerships` + `core_unit_occupancies` + `core_condominium_roles`

---

## Patrón de Estructura DDD por Módulo

Todo módulo nuevo debe seguir esta estructura:

```
{modulo}/
├── domain/
│   ├── {modulo}_entity.py          # Entidad de dominio
│   ├── {modulo}_data.py            # Data objects (opcional)
│   ├── {modulo}_exception.py       # Excepciones del módulo
│   ├── {modulo}_success.py         # Catálogo de mensajes de éxito
│   ├── {modulo}_repository.py      # Contrato agregado (opcional si cmd/query basta)
│   ├── {modulo}_cmd_repository.py  # Contrato de escritura
│   └── {modulo}_query_repository.py # Contrato de lectura
├── infrastructure/
│   ├── db{modulo}.py               # Modelo SQLAlchemy
│   ├── {modulo}_mapper.py          # Mapper DB → Dominio
│   ├── {modulo}_cmd_repository.py  # Repositorio concreto de escritura
│   └── {modulo}_query_repository.py # Repositorio concreto de lectura
└── usecase/
    ├── {modulo}_cmd_schema.py      # Schemas de entrada (commands)
    ├── {modulo}_cmd_usecase.py     # Caso de uso de escritura
    ├── {modulo}_query_usecase.py   # Caso de uso de lectura
    ├── {modulo}_usecase.py        # Fachada que returns ResponseSuccessSchema
    └── {modulo}_factory.py        # Ensamblaje de dependencias
```

Ruta API: `src/api/{modulo}/routes_{modulo}.py`

---

## Contratos Transversales

### Response Schema
```python
class ResponseSuccessSchema(BaseModel):
    success: bool = True
    message: str
    data: Optional[Any] = None

class ResponseErrorSchema(BaseModel):
    success: bool = False
    message: str
```

### Exception Base
```python
class DomainException(Exception):
    def __init__(self, message: str, status_code: int = 500): ...
```

### Decorator
```python
@api_handler  # Maneja DomainException, ValidationError, y errores inesperados
```

---

## Flujo Oficial

```
route → parse schema → use case → ResponseSuccessSchema → response.dict()
                                                    ↓
                              @api_handler captura DomainException / ValidationError
```

---

*Última actualización: 2026-04-10*
