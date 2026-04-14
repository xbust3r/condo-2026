# condo-py — Sistema de Gestión para Condominios

> **Estado del proyecto:** Migrado a **FastAPI** + **SQLAlchemy** + **MySQL**
>
> **Arquitectura:** DDD/CQRS con patrón Repository
>
> **Objetivo:** Backend para gestión de condominios con estructura modular DDD

---

## 1. Stack Tecnológico

- **Python** 3.14
- **FastAPI** - Framework HTTP
- **SQLAlchemy** - ORM
- **MySQL** - Base de datos
- **Alembic** - Migraciones
- **Pydantic** - Validación de datos
- **Docker** - Contenedores

---

## 2. Estructura del Proyecto

```
condo-py/
├── alembic/                  # Migraciones Alembic
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── src/
│   ├── app.py               # FastAPI main
│   ├── api/                 # Routers FastAPI
│   │   ├── condominiums/
│   │   ├── buildings/
│   │   ├── buildings_types/
│   │   ├── unitys/
│   │   ├── unittys_types/
│   │   ├── users/
│   │   └── residents/
│   ├── library/
│   │   └── dddpy/
│   │       ├── shared/      # Componentes compartidos
│   │       │   ├── mysql/   # Base, Session
│   │       │   ├── constants/
│   │       │   ├── schemas/
│   │       │   ├── logging/
│   │       │   └── utils/
│   │       ├── core_condominiums/
│   │       ├── core_buildings/
│   │       ├── core_buildings_types/
│   ├── core_unities/
│   │       ├── core_unittys_types/
│   │       ├── users/
│   │       └── users_residents/
│   └── requirements.txt
├── documentation/
│   └── models/             # Documentación de entidades
├── Makefile
├── docker-compose.yml
└── alembic.ini
```

---

## 3. Módulos DDD

| Módulo | Tabla | Descripción |
|--------|-------|-------------|
| `core_condominiums` | `core_condominiums` | Gestión de condominios |
| `core_buildings` | `core_buildings` | Torres/edificios |
| `core_buildings_types` | `core_buildings_types` | Tipos de edificio |
| `core_unities` | `core_unities` | Unidades inmobiliarias |
| `core_unittys_types` | `core_unittys_types` | Tipos de unidad |
| `users` | `users` | Usuarios del sistema |
| `users_residents` | `users_residents` | Residentes (pivot) |

---

## 4. Patrón de Arquitectura (DDD)

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
    ├── {modulo}_cmd_usecase.py
    ├── {modulo}_query_usecase.py
    └── {modulo}_usecase.py
```

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
- `POST /unities` - Crear
- `GET /unities` - Listar todos
- `GET /unities/by-building/{id}` - Por edificio
- `GET /unities/{id}` - Obtener por ID
- `PUT /unities/{id}` - Actualizar
- `DELETE /unities/{id}` - Eliminar

### Tipos de Unidad
- `POST /core_unities_types` - Crear
- `GET /core_unities_types` - Listar todos
- `GET /core_unities_types/{id}` - Obtener por ID
- `GET /core_unities_types/uuid/{uuid}` - Obtener por UUID
- `PUT /core_unities_types/{id}` - Actualizar
- `DELETE /core_unities_types/{id}` - Soft delete
- `POST /core_unities_types/{id}/restore` - Restaurar
- `DELETE /core_unities_types/{id}/hard` - Hard delete

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

## 6. Respuestas API

Todas las respuestas siguen el formato:

```json
{
  "success": true,
  "message": "Operation successful",
  "data": { ... }
}
```

---

## 7. Migraciones

### Configuración de Base de Datos

Alembic lee la configuración de la base de datos directamente desde `src/.env`. No es necesario configurar nada en `alembic.ini`.

Variables requeridas en `src/.env`:
```env
MYSQL_USER=stg_panelhub
MYSQL_PASSWORD=tu_password
MYSQL_HOST=herav4-production.cluster-cymuhlhwsajk.us-west-2.rds.amazonaws.com
MYSQL_PORT=3306
MYSQL_DB=stg_panelhub
```

### Ejecutar Alembic dentro del contenedor

Alembic lee la configuración de base de datos desde `src/.env`.

```bash
# Opción 1: Copiar alembic al contenedor y ejecutar
docker cp alembic/ <container>:/app/
docker exec -w /app <container> alembic upgrade head

# Opción 2: make command (monta /app directo)
make alembic COMMAND="upgrade head"
```

### Comandos útiles Alembic

| Comando | Descripción |
|---------|-------------|
| `alembic revision --autogenerate -m "nombre"` | Generar nueva migración |
| `alembic upgrade head` | Aplicar todas las migraciones |
| `alembic downgrade -1` | Revertir última migración |
| `alembic current` | Ver migración actual |
| `alembic history` | Ver historial de migraciones |

---

## 8. Ejecución Local

### Con Docker
```bash
make build
make up
```

###直接 con Python
```bash
pip install -r src/requirements.txt
uvicorn src.app:app --reload
```

---

## 9. Base de Datos

- **Host:** herav4-production.cluster-cymuhlhwsajk.us-west-2.rds.amazonaws.com
- **Puerto:** 3306
- **Usuario:** stg_panelhub
- **Base:** stg_panelhub

---

**README actualizado - Migración completada de Chalice a FastAPI**
