# Sprint 9 — `core_notifications` — Notification Layer

**Fecha:** 2026-04-24
**Proyecto:** `condo-py` (`~/servers/condo-py`)
**Responsable:** Lelouch (análisis + arquitectura) + sub-agentes (implementación)

---

## Overview

`core_notifications` es la **capa glue** que conecta eventos del sistema con usuarios relevantes. No tiene lógica de negocio propia — observa eventos de otros módulos y envía notificaciones a los usuarios correspondientes.

**Fuentes de eventos (providers):**
- `core_announcements` — cuando se crea/publcia un anuncio
- `core_incidents` — cuando cambia el estado de un ticket (asignado, completado, cerrado)
- `core_payments` / `core_receipts` — cuando se genera un recibo o se registra un pago
- (futuro) `core_documents` — cuando se sube un documento relevante

**Canales de entrega (channels):**
- **In-app** — almacenar en DB para que el frontend haga polling o websocket
- **Email** — enviar email al usuario (usar servicio de email ya existente en `auth`)
- **Push (futuro)** — FCM / APNs (no implementar en Sprint 9)

---

## Modelo de Datos

### `NotificationEntity`

```
notification_id: int
uuid: str
user_id: int           → destinatario
channel: str          → 'in_app', 'email'
type: str             → 'announcement_published', 'incident_assigned', 'incident_resolved', 'payment_received', ...
resource_type: str    → 'announcement', 'incident', 'payment', 'receipt'
resource_id: int       → ID del recurso relacionado
title: str            → título de la notificación
body: str             → cuerpo/preview del mensaje
is_read: bool         → default false
read_at: datetime     → nullable
created_at: datetime
deleted_at: datetime  → soft-delete
metadata: JSON         → datos adicionales contextuales (author_name, condo_name, etc.)
```

### Enums

**NotificationChannel:** `in_app`, `email`
**NotificationType:** `announcement_published`, `incident_assigned`, `incident_completed`, `incident_closed`, `payment_received`, `receipt_generated`

---

## Arquitectura DDD

```
src/library/dddpy/core_notifications/
├── domain/
│   ├── notification_entity.py
│   ├── notification_exception.py
│   ├── notification_repository.py    ← ABC cmd
│   └── notification_query_repository.py ← ABC query
├── infrastructure/
│   ├── db_notification.py            ← SQLAlchemy model
│   ├── notification_cmd_repository.py
│   ├── notification_query_repository.py  ← con _bulk_enrich
│   └── notification_mapper.py
├── usecase/
│   ├── notification_cmd_schema.py
│   ├── notification_cmd_usecase.py
│   ├── notification_query_usecase.py
│   ├── notification_factory.py
│   └── notification_service.py       ← servicio de dominio que reciben los módulos productores
└── api/
    └── notifications/routes_notifications.py
```

### El patrón Observer/Lazy-Import

Los módulos productores (`core_announcements`, `core_incidents`) NO hacen import directo de `core_notifications` (evitaría círculos). En cambio:

**Opción A — Domain Events (futuro):** Events del dominio que un event bus dispersa. Más elegante pero más complejo.

**Opción B — Lazy import dentro del usecase:** En los usecases de announcements/incidents, al final del `create()` o `update()`, se importa `NotificationService` y se llama `notify_event()`. El import dentro de la función evita el círculo.

**Opción C —más pragmática para Sprint 9:** Crear `NotificationService` como un servicio reusable. Los módulos que quieran notificar llaman a `NotificationService.get_instance().notify(...)` (singleton). Esto se implementa al final del Sprint cuando ya esté listo todo.

**Recomendado: Opción B** — lazy import, simple, sin cambios en la arquitectura de los módulos existentes.

---

## NotificationService — API del servicio

```python
class NotificationService:
    """Servicio para crear notificaciones desde cualquier módulo."""

    def notify(
        self,
        user_id: int,
        channel: NotificationChannel,
        notif_type: NotificationType,
        resource_type: str,
        resource_id: int,
        title: str,
        body: str,
        metadata: Optional[dict] = None,
    ) -> None:
        """Crea una notificación y la persiste en DB."""

    def notify_multiple(
        self,
        user_ids: List[int],
        channel: NotificationChannel,
        notif_type: NotificationType,
        resource_type: str,
        resource_id: int,
        title: str,
        body: str,
        metadata: Optional[dict] = None,
    ) -> int:
        """Crea notificaciones para múltiples usuarios (bulk). Retorna count."""

    def send_email_notification(
        self,
        user_id: int,
        title: str,
        body: str,
    ) -> None:
        """Envía email usando el EmailService de auth (mock OK)."""
```

---

## Endpoints API

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/notifications` | Listar notificaciones (filtros: user_id, is_read, channel, type) |
| GET | `/notifications/{id}` | Ver una notificación |
| GET | `/notifications/unread-count` | Contador de no leídas para el usuario actual |
| PATCH | `/notifications/{id}/read` | Marcar como leída |
| PATCH | `/notifications/mark-all-read` | Marcar todas como leídas |
| DELETE | `/notifications/{id}` | Soft-delete |
| GET | `/users/{user_id}/notifications` | Notificaciones de un usuario (paginados) |

---

## Integración con módulos existentes

### `core_announcements` — integration point

En `AnnouncementUseCase.create()` y `update()` (cuando se publica), al final del método:

```python
# Al final de announcement_usecase.create()
notification_service = NotificationService()
notification_service.notify(
    user_id=author_user_id,  # o todos los usuarios del condominio
    channel='in_app',
    notif_type='announcement_published',
    resource_type='announcement',
    resource_id=announcement.id,
    title=f"Nuevo anuncio: {data.title}",
    body=data.content[:200],
    metadata={'condominium_id': data.condominium_id},
)
```

### `core_incidents` — integration points

En `IncidentCmdUseCase.update()` (cuando cambia status o se asigna):

```python
# Cuando se asigna
if data.assigned_to_user_id and existing.assigned_to_user_id != data.assigned_to_user_id:
    notification_service.notify(
        user_id=data.assigned_to_user_id,
        channel='in_app',
        notif_type='incident_assigned',
        resource_type='incident',
        resource_id=incident.id,
        title=f"Incidente asignado: {incident.title}",
        body=f"Se te ha asignado el incidente #{incident.id}",
    )

# Cuando se completa
if data.status == 'resolved':
    notification_service.notify(
        user_id=incident.reported_by_user_id,
        channel='in_app',
        notif_type='incident_resolved',
        resource_type='incident',
        resource_id=incident.id,
        title=f"Incidente #{incident.id} resuelto",
        body="Su incidente ha sido marcado como resuelto.",
    )
```

---

## Migración

```sql
CREATE TABLE core_notifications (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  uuid VARCHAR(36) NOT NULL UNIQUE,
  user_id BIGINT NOT NULL,
  channel VARCHAR(20) NOT NULL DEFAULT 'in_app',
  type VARCHAR(50) NOT NULL,
  resource_type VARCHAR(30) NOT NULL,
  resource_id BIGINT NOT NULL,
  title VARCHAR(200) NOT NULL,
  body TEXT,
  is_read BOOLEAN NOT NULL DEFAULT FALSE,
  read_at DATETIME NULL,
  metadata JSON,
  created_at DATETIME NOT NULL DEFAULT NOW(),
  deleted_at DATETIME NULL,
  FOREIGN KEY (user_id) REFERENCES users(id),
  INDEX idx_user_read (user_id, is_read),
  INDEX idx_user_created (user_id, created_at DESC),
  INDEX idx_resource (resource_type, resource_id)
);
```

---

## RBAC

```
notifications:read   → ver notificaciones propias
notifications:read_all → ver notificaciones de cualquier usuario (admin)
notifications:delete → borrar notificaciones
```

---

## Tasks

| Task | Descripción |
|---|---|
| T-1 | Migración 042 `core_notifications` |
| T-2 | DDD domain layer (entity, exceptions, repos ABC) |
| T-3 | Infrastructure (db, cmd repo, query repo con _bulk_enrich, mapper) |
| T-4 | Usecases + NotificationService |
| T-5 | API routes |
| T-6 | Integración en `core_announcements` (create, publish) |
| T-7 | Integración en `core_incidents` (assign, resolve, close) |
| T-8 | Seed RBAC permissions |

---

## Siguiente paso

@Misato K — confirmación: ¿notifications lo hago yo o lo dejamos pendiente para después de Phase 4 completo? El módulo es relativamente simple (DB + API + servicio de notificación), pero requiere integrar con announcements e incidents.
