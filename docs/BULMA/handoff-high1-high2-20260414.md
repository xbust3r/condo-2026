# Handoff — Sprint 1: HIGH-1 + HIGH-2
**Developer:** Bulma S
**Date:** 2026-04-14
**Repo:** `/home/miguel/servers/condo-py`

---

## HIGH-1: Bypass de capas en `restore()`

### Problema
`CondominiumUseCase.restore()` llamaba directamente a
`self.condominium_cmd_usecase.repository.restore(id)` (línea 95),
rompiendo la disciplina de capas.

### Archivos tocados

| Archivo | Cambio |
|---|---|
| `src/library/dddpy/core_condominiums/domain/condominium_repository.py` | Agregado método abstracto `restore(id: int) → bool` |
| `src/library/dddpy/core_condominiums/usecase/condominium_cmd_usecase.py` | Agregado método `restore(self, id: int) → dict` que delega a `self.repository.restore(id)` |
| `src/library/dddpy/core_condominiums/usecase/condominium_usecase.py` | Cambiado `self.condominium_cmd_usecase.repository.restore(id)` → `self.condominium_cmd_usecase.restore(id)` |

### Detalle del cambio en `condominium_usecase.py`

**ANTES (línea ~95):**
```python
restored = self.condominium_cmd_usecase.repository.restore(id)
```

**DESPUÉS:**
```python
restored = self.condominium_cmd_usecase.restore(id)
if not restored.get("restored"):   # <- fix: acceder al bool dentro del dict
    logger.warning(f"Failed to restore condominium id={id}")
    raise CondominiumNotFound()
```

> **Nota de implementación:** `CondominiumCmdUseCase.restore()` retorna `dict` (no `bool`) para permitir extensiones futuras. El check usa `.get("restored")` para extraer el valor booleano del dict retornado.

### Detalle del cambio en `condominium_cmd_usecase.py`

**ANTES:** No existía el método `restore()`.

**DESPUÉS:**
```python
def restore(self, id: int) -> dict:
    logger.info(f"Delegating condominium restore for id={id}")
    restored = self.repository.restore(id)
    return {"id": id, "restored": restored}
```

### Detalle del cambio en `condominium_repository.py` (ABC)

**ANTES:** No existía `restore()`.

**DESPUÉS:** Agregado tras `delete()`:
```python
@abstractmethod
def restore(self, id: int) -> bool:
    """Restore a soft-deleted condominium."""
    pass
```

---

## HIGH-2: Respuesta inconsistente en `delete()`

### Problema
`CondominiumUseCase.delete()` retornaba `existing.deleted_at`, que era un
snapshot previo a la operación de soft-delete, no el timestamp real asignado
por la base de datos.

### Archivos tocados

| Archivo | Cambio |
|---|---|
| `src/library/dddpy/core_condominiums/usecase/condominium_usecase.py` | Query fresa post soft-delete para obtener `deleted_at` real |

### Detalle del cambio en `condominium_usecase.py`

**ANTES (líneas ~83-100):**
```python
deleted = self.condominium_cmd_usecase.delete(id)
if not deleted:
    logger.warning(f"Failed to delete condominium id={id}")
    raise CondominiumNotFound()
success = ResponseSuccessSchema(
    success=True,
    message=CondominiumSuccessMessage.DELETED,
    data={"id": id, "deleted_at": existing.deleted_at},
)
```

**DESPUÉS:**
```python
deleted = self.condominium_cmd_usecase.delete(id)
if not deleted:
    logger.warning(f"Failed to delete condominium id={id}")
    raise CondominiumNotFound()
# Query fresh record to get the real deleted_at timestamp
fresh = self.condominium_query_usecase.get_by_id(id)
real_deleted_at = fresh.deleted_at if fresh else None
success = ResponseSuccessSchema(
    success=True,
    message=CondominiumSuccessMessage.DELETED,
    data={"id": id, "deleted_at": real_deleted_at, "success": True},
)
```

### Nota
- La variable `existing` (snapshot previo) ya no se usa en el response de `delete()`.
- Se reutiliza `self.condominium_query_usecase.get_by_id(id)` (que ya existe en el caso de uso) para obtener el timestamp real.

---

## Resumen de archivos modificados

1. `src/library/dddpy/core_condominiums/domain/condominium_repository.py` — ABC +restore()
2. `src/library/dddpy/core_condominiums/usecase/condominium_cmd_usecase.py` — +restore()
3. `src/library/dddpy/core_condominiums/usecase/condominium_usecase.py` — restore() fix + delete() fix

**No se crearon módulos nuevos. No se modificó lógica de infraestructura.**
