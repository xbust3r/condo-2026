# Guía de Arquitectura de `condo-py`

> **Proyecto:** `condo-py`
>
> **Framework HTTP:** FastAPI
>
> **Persistencia:** SQLAlchemy + MySQL
>
> **Validación:** Pydantic
>
> **Testing:** Pytest
>
> **Migraciones:** Alembic

---

## 1. Visión General

`condo-py` es un backend para gestión de condominios construido con:

- **FastAPI** - Framework HTTP moderno y rápido
- **SQLAlchemy** - ORM para MySQL
- **Pydantic** - Validación de datos
- **Alembic** - Migraciones de base de datos
- **Arquitectura DDD** - Patrón Domain-Driven Design

---

## 2. Estructura del Proyecto

```
condo-py/
├── alembic/                  # Migraciones
│   ├── env.py                # Configuración (lee src/.env)
│   └── versions/             # Archivos de migración
├── src/
│   ├── app.py               # FastAPI entry point
│   ├── api/                 # Routers HTTP
│   │   ├── condominiums/
│   │   ├── buildings/
│   │   ├── buildings_types/
│   │   ├── unitys/
│   │   ├── unittys_types/
│   │   ├── users/
│   │   └── residents/
│   ├── library/             # ⬅️ Antes chalicelib
│   │   └── dddpy/
│   │       ├── shared/      # Componentes compartidos
│   │       │   ├── mysql/   # Base, Session
│   │       │   ├── constants/
│   │       │   ├── schemas/
│   │       │   └── logging/
│   │       ├── core_condominiums/
│   │       ├── core_buildings/
│   │       ├── core_buildings_types/
│   │       ├── core_unitys/
│   │       ├── core_unittys_types/
│   │       ├── users/
│   │       └── users_residents/
│   └── .env                # Configuración
├── Makefile
└── docker-compose.yml
```

---

## 3. Arquitectura DDD

Cada módulo sigue la estructura:

```
{modulo}/
├── domain/
│   ├── {modulo}.py          # Entidad de dominio
│   ├── {modulo}_exception.py
│   └── {modulo}_repository.py
├── infrastructure/
│   ├── {modulo}.py          # Modelo SQLAlchemy
│   ├── {modulo}_mapper.py
│   ├── {modulo}_cmd_repository.py
│   └── {modulo}_query_repository.py
└── usecase/
    ├── {modulo}_cmd_schema.py
    ├── {modulo}_usecase.py
    └── {modulo}_factory.py
```

### Flujo de una request

```
HTTP Request
  → FastAPI Router
  → Pydantic Schema
  → UseCase
  → Repository
  → SQLAlchemy Model
  → MySQL
```

---

## 4. Módulos Actuales

| Módulo | Tabla | Descripción |
|--------|-------|-------------|
| `core_condominiums` | `core_condominiums` | Gestión de condominios |
| `core_buildings` | `core_buildings` | Torres/edificios |
| `core_buildings_types` | `core_buildings_types` | Tipos de edificio |
| `core_unitys` | `core_unitys` | Unidades inmobiliarias |
| `core_unittys_types` | `core_unittys_types` | Tipos de unidad |
| `users` | `users` | Usuarios del sistema |
| `users_residents` | `users_residents` | Residentes (pivot) |

---

## 5. API Endpoints

### Condominios
- `POST /condominiums` - Crear
- `GET /condominiums` - Listar todos
- `GET /condominiums/{id}` - Obtener por ID
- `PUT /condominiums/{id}` - Actualizar
- `DELETE /condominiums/{id}` - Eliminar

### Edificios
- `POST /buildings` - Crear
- `GET /buildings` - Listar todos
- `GET /buildings/by-condominium/{id}` - Por condominio
- `GET /buildings/{id}` - Obtener por ID
- `PUT /buildings/{id}` - Actualizar
- `DELETE /buildings/{id}` - Eliminar

### Tipos de Edificio
- `POST /buildings-types` - Crear
- `GET /buildings-types` - Listar todos
- `GET /buildings-types/{id}` - Obtener por ID
- `PUT /buildings-types/{id}` - Actualizar
- `DELETE /buildings-types/{id}` - Eliminar

### Unidades
- `POST /unitys` - Crear
- `GET /unitys` - Listar todos
- `GET /unitys/by-building/{id}` - Por edificio
- `GET /unitys/{id}` - Obtener por ID
- `PUT /unitys/{id}` - Actualizar
- `DELETE /unitys/{id}` - Eliminar

### Tipos de Unidad
- `POST /unit-types` - Crear
- `GET /unit-types` - Listar todos
- `GET /unit-types/{id}` - Obtener por ID
- `PUT /unit-types/{id}` - Actualizar
- `DELETE /unit-types/{id}` - Eliminar

### Usuarios
- `POST /users` - Crear
- `GET /users` - Listar todos
- `GET /users/{id}` - Obtener por ID
- `PUT /users/{id}` - Actualizar
- `DELETE /users/{id}` - Eliminar

### Residentes
- `POST /residents` - Crear
- `GET /residents` - Listar todos
- `GET /residents/by-user/{id}` - Por usuario
- `GET /residents/by-unity/{id}` - Por unidad
- `GET /residents/{id}` - Obtener por ID
- `PUT /residents/{id}` - Actualizar
- `DELETE /residents/{id}` - Eliminar

---

## 6. Configuración

### Variables de Entorno (src/.env)

```env
MYSQL_USER=root
MYSQL_PASSWORD=123456
MYSQL_HOST=mysql
MYSQL_PORT=3306
MYSQL_DB=db_condominiums
```

### Alembic

Alembic lee la configuración de la base de datos desde `src/.env`.

```bash
# Generar migración
alembic revision --autogenerate -m "nombre_migracion"

# Aplicar migraciones
alembic upgrade head

# Revertir última
alembic downgrade -1
```

---

## 7. Respuestas API

Todas las respuestas siguen el formato:

```json
{
  "success": true,
  "message": "Operation successful",
  "data": { ... }
}
```

---

## 8. Ejecución Local

### Con Docker
```bash
make build
make up
```

###直接
```bash
pip install -r src/requirements.txt
uvicorn src.app:app --reload --port 8000
```

---

## 9. Convenciones

### Nombrado
- **Tablas:** plural snake_case (e.g., `core_condominiums`)
- **Modelos:** Prefijo `DB` + nombre singular (e.g., `DBCondominiums`)
- **Entidades:** Nombre singular (e.g., `Condominium`)
- **Routers:** plural del recurso (e.g., `/condominiums`)

### Excepciones
Cada módulo tiene sus propias excepciones:
- `XxxNotFoundException` - 404
- `XxxAlreadyExistsException` - 409

---

## 10. Referencias

- `src/app.py` - FastAPI main
- `src/api/` - Routers
- `src/library/dddpy/` - Módulos DDD
- `src/.env` - Configuración
