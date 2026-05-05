# core_announcements — Módulo de Comunicados

## Overview

Módulo DDD para la gestión de anuncios/comunicados dentro de un condominio. Permite publicar comunicados a todo el condominio o dirigido a torres específicas, con control de visibilidad y categorización.

---

## Estructura del modelo

```
core_announcements
├── domain/
│   ├── announcement_entity.py       # Entidad de dominio
│   ├── announcement_cmd_repository.py  # Interfaz comando (escribir)
│   └── announcement_query_repository.py # Interfaz query (leer)
├── infrastructure/
│   ├── dbannouncement.py            # Modelo SQLAlchemy (tabla DB)
│   ├── announcement_mapper.py       # Mapper DB → Entity
│   ├── announcement_cmd_repository.py  # Implementación comando
│   └── announcement_query_repository.py # Implementación query
└── usecase/
    ├── announcement_usecase.py      # Lógica de negocio
    └── announcement_cmd_schema.py  # Schemas Pydantic (input)
```

---

## Modelo de base de datos

Tabla: `core_announcements`

| Campo | Tipo | Notas |
|---|---|---|
| `id` | BIGINT PK | Auto-increment |
| `uuid` | VARCHAR(36) | Único |
| `condominium_id` | BIGINT FK | Required |
| `author_user_id` | BIGINT FK | Required |
| `title` | VARCHAR(200) | Required, min 3 chars |
| `content` | TEXT | Required, min 10 chars |
| `category` | VARCHAR(20) | Default: `info` |
| `visibility` | VARCHAR(20) | Default: `public` |
| `is_pinned` | BOOLEAN | Default: false |
| `tower_id` | BIGINT FK (nullable) | Null = todas las torres |
| `published_at` | DATETIME (nullable) | Null = publicado inmediatamente |
| `expires_at` | DATETIME (nullable) | Null = nunca expira |
| `created_at` | DATETIME | Auto timestamp |
| `updated_at` | DATETIME | Auto on update |
| `deleted_at` | DATETIME | Soft delete |

**Índices:**
- `condominium_id`
- `tower_id`
- `ix_announcements_condo_published` (condominium_id + published_at)
- `ix_announcements_category` (category)

---

## Categorías válidas

```python
VALID_CATEGORIES = {
    'info',        # Informativo general
    'warning',     # Advertencia
    'urgent',      # Emergencia
    'event',       # Evento
    'balance',     # Balance financiero
    'assembly',    # Convocatoria de asamblea
    'maintenance', # Aviso de mantenimiento
    'vote',        # Votación / encuesta
    'rule',        # Nueva norma / reglamento
    'general',     # General
}
```

---

## Alcances de visibilidad

```python
VALID_VISIBILITY_SCOPES = {
    'public',        # Todos (propietarios + residentes)
    'owners_only',   # Solo propietarios
    'residents_only' # Solo residentes
}
```

---

## Alcance por torre

- `tower_id = NULL` → El comunicado llega a **todo el condominio**
- `tower_id = <id>` → El comunicado está dirigido **solo a esa torre**

Filtro disponible en todos los endpoints de lista.

---

## API Endpoints

| Método | Ruta | RBAC | Descripción |
|---|---|---|---|
| `GET` | `/announcements/health` | — | Health check |
| `POST` | `/announcements` | `announcement.write` | Crear comunicado |
| `GET` | `/announcements` | `announcement.read` | Listar (con filtros) |
| `GET` | `/announcements/{id}` | `announcement.read` | Obtener por ID |
| `GET` | `/announcements/uuid/{uuid}` | `announcement.read` | Obtener por UUID |
| `GET` | `/announcements/condominium/{id}/active` | `announcement.read` | Activos para condominio |
| `PUT` | `/announcements/{id}` | `announcement.write` | Actualizar |
| `DELETE` | `/announcements/{id}` | `announcement.delete` | Soft delete |
| `POST` | `/announcements/{id}/restore` | `announcement.write` | Restaurar |
| `DELETE` | `/announcements/{id}/hard` | `announcement.delete` | Hard delete |

### Query params en `GET /announcements`

| Param | Tipo | Descripción |
|---|---|---|
| `condominium_id` | int | Filtrar por condominio |
| `category` | string | Filtrar por categoría |
| `visibility` | string | Filtrar por visibilidad |
| `tower_id` | int | Filtrar por torre |
| `include_deleted` | bool | Incluir eliminados |
| `skip` | int | Offset (default 0) |
| `limit` | int | Límite (default 100, max 500) |

### Endpoint público

`GET /announcements/condominium/{condominium_id}/active` — Lista comunicados activos (publicados y no expirados) sin autenticación RBAC pesada. Soporta `tower_id`, `skip`, `limit`.

---

## Notificaciones automáticas

Al crear o actualizar un comunicado, se genera automáticamente una notificación in-app al autor:

- **Creación:** tipo `announcement_published`
- **Actualización:** tipo `announcement_updated`

---

## Estados y ciclo de vida

```
[CREATED] → published_at null → publicado inmediatamente
         → published_at set   → programado

[ACTIVE]  → published_at ≤ now ≤ expires_at
         → is_pinned = true  → aparece primero

[EXPIRED] → expires_at < now

[DELETED] → soft delete (deleted_at set)
         → hard delete (fila eliminada)

[RESTORED] → soft-deleted → restored (deleted_at cleared)
```

---

## Validaciones en use case

- `title`: mínimo 3 caracteres
- `content`: mínimo 10 caracteres
- `category`: debe estar en `VALID_CATEGORIES`
- `visibility`: debe estar en `VALID_VISIBILITY_SCOPES`
- `expires_at`: debe ser posterior a `published_at` (si se provee)

---

## Enriquecimiento de datos

Al consultar announcements, se hacen joins/enriquecimiento con:
- Nombre completo del autor (`users` + `user_profiles`)
- Nombre del condominio (`core_condominiums`)
- Nombre de la torre (`core_buildings`)

---

## Uso típico

**Comunicado a todo el condominio:**
```json
POST /announcements
{
  "condominium_id": 1,
  "author_user_id": 10,
  "title": "Mantenimiento de ascensores",
  "content": "El día sábado se realizará mantenimiento...",
  "category": "maintenance",
  "visibility": "public",
  "tower_id": null
}
```

**Comunicado solo a torre A:**
```json
{
  "title": "Corte de agua - Torre A",
  "content": "...",
  "category": "urgent",
  "visibility": "public",
  "tower_id": 3
}
```

**Balance financiero (solo propietarios):**
```json
{
  "title": "Balance Abril 2026",
  "content": "...",
  "category": "balance",
  "visibility": "owners_only",
  "tower_id": null
}
```

---

## Migración

`034_create_core_announcements` — Migration Alembic.

---

*Documentado por Misato K — 2026-05-04*