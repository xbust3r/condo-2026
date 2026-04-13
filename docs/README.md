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
| `03-modules/models/core_condominiums.md` | Modelo: Condominios |
| `03-modules/models/core_buildings.md` | Modelo: Edificios/Torres |
| `03-modules/models/core_buildings_types.md` | Modelo: Tipos de edificio |
| `03-modules/models/core_unitys.md` | Modelo: Unidades inmobiliarias |
| `03-modules/models/core_unittys_types.md` | Modelo: Tipos de unidad |
| `03-modules/models/users.md` | Modelo: Usuarios del sistema |
| `03-modules/models/users_residents.md` | Modelo: Residentes (pivot) |
| `03-modules/module-roadmap.md` | Orden recomendado de implementación de módulos y sprints |

---

## 📂 04-bulma — Equipo Dev (Reglas y Guías)

| Archivo | Descripción |
|---|---|
| `04-bulma/README.md` | Índice del equipo BULMA |
| `04-bulma/MODULES.md` | Estado y mapa de módulos |
| `04-bulma/architecture-rules.md` | Reglas de arquitectura |
| `04-bulma/implementation-guidelines.md` | Guías de implementación |
| `04-bulma/anti-patterns.md` | Anti-patterns a evitar |
| `04-bulma/change-playbook.md` | Playbook de cambios |
| `04-bulma/module-map.md` | Mapa de módulos del sistema |

---

## 📂 05-research — Research en Curso

Carpeta para datos de mercado, investigación y documentación en proceso de análisis.

> **Estado:** Pendiente de uso para research de features y posicionamiento.

---

## 📂 06-competitor-analysis — Análisis Competitivo

| Archivo | Descripción |
|---|---|
| `06-competitor-analysis/competitive-analysis.md` | Reporte de inteligencia competitiva — 8 competidores mapeados |
| `06-competitor-analysis/lelouch-strategic-analysis.md` | Análisis estratégico de Lelouch |

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
