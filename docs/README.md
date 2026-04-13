# condo-py — Documentación del Proyecto

> Índice central de toda la documentación del proyecto.
> Cada carpeta numerada representa una categoría lógica de documentación.

---

## 📁 Estructura de Documentos

```
docs/
├── 00-archive/          # Documentación obsoleta o redundante (no usar como referencia)
├── 01-general/         # Documentación general del proyecto
├── 02-architecture/    # Arquitectura DDD/CQRS y guías de diseño
├── 03-modules/         # Modelos de datos y documentación de módulos
├── 04-bulma/           # Guías y reglas del equipo BULMA (Dev)
├── 05-research/        # Research y datos de mercado en curso
└── 06-competitor-analysis/  # Análisis competitivo y posicionamiento
```

---

## 📂 01-general — Documentación General

| Archivo | Descripción |
|---|---|
| `README.md` | Este archivo — índice general del proyecto |
| `architecture.md` | Arquitectura general del sistema |
| `docker.md` | Guía de configuración y despliegue con Docker |

---

## 📂 02-architecture — Arquitectura DDD/CQRS

| Archivo | Descripción |
|---|---|
| `new-standard/ddd-architecture-base-guide.md` | Guía base del patrón DDD adoptado |
| `new-standard/observations/` | Observaciones y notas de arquitectura |

**Subcarpetas:**
- `new-standard/observations/` — Notas técnicas sobre decisiones de arquitectura

---

## 📂 03-modules — Modelos de Datos

| Archivo | Descripción |
|---|---|
| `models/core_condominiums.md` | Modelo: Condominios |
| `models/core_buildings.md` | Modelo: Edificios/Torres |
| `models/core_buildings_types.md` | Modelo: Tipos de edificio |
| `models/core_unitys.md` | Modelo: Unidades inmobiliarias |
| `models/core_unittys_types.md` | Modelo: Tipos de unidad |
| `models/users.md` | Modelo: Usuarios del sistema |
| `models/users_residents.md` | Modelo: Residentes (pivot) |

---

## 📂 04-bulma — Equipo Dev (Reglas y Guías)

| Archivo | Descripción |
|---|---|
| `BULMA/README.md` | Índice del equipo BULMA |
| `BULMA/MODULES.md` | Estado y mapa de módulos |
| `BULMA/architecture-rules.md` | Reglas de arquitectura |
| `BULMA/implementation-guidelines.md` | Guías de implementación |
| `BULMA/anti-patterns.md` | Anti-patterns a evitar |
| `BULMA/change-playbook.md` | Playbook de cambios |
| `BULMA/module-map.md` | Mapa de módulos del sistema |

---

## 📂 05-research — Research en Curso

Carpeta para datos de mercado, investigación y documentación en proceso de análisis.

> **Estado:** Pendiente de uso para research de features y posicionamiento.

---

## 📂 06-competitor-analysis — Análisis Competitivo

| Archivo | Descripción |
|---|---|
| `competitive-analysis.md` | Reporte de inteligencia competitiva — 8 competidores mapeados |
| `lelouch-strategic-analysis.md` | Análisis estratégico de Lelouch |

**Competidores analizados:**
- 🇺🇸 Buildium, AppFolio, Condo Control, Propertyware
- 🇧🇷 Superlógica, CondoLivre, TownSq
- 🇪🇺 Kastle (seguridad física)

---

## 🔗 Referencias del Proyecto

- **Repo:** `/home/miguel/servers/condo-py/`
- **Src:** `/home/miguel/servers/condo-py/src/`
- **Workspace docs:** `/home/miguel/.openclaw/workspace/` (archivos operativos de Misato)

---

*Última actualización: 2026-04-13 — Reorganización por Misato K*
