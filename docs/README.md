# condo-py — Documentación del Proyecto

> Índice central de toda la documentación del proyecto.
> Cada carpeta numerada representa una categoría lógica de documentación.

---

## 📁 Estructura de Documentos

```
docs/
├── 00-archive/              # Documentación obsoleta o redundante
├── 01-general/              # Documentación general del proyecto
├── 02-architecture/         # Arquitectura DDD/CQRS y guías de diseño
├── 03-modules/              # Modelos de datos y documentación de módulos
├── 04-bulma/                # Guías y reglas del equipo BULMA (Dev)
├── 05-research/             # Research y datos de mercado en curso
├── 06-competitor-analysis/  # Análisis competitivo y posicionamiento
└── 07-roadmap/              # Roadmap oficial del proyecto
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
| `models/core_unities.md` | Modelo: Unidades inmobiliarias |
| `models/core_unittys_types.md` | Modelo: Tipos de unidad |
| `models/users.md` | Modelo: Usuarios del sistema |
| `models/users_residents.md` | Modelo: Residentes (pivot) |
| `MODULES.md` | Estado y mapa de módulos |

---

## 📂 04-bulma — Equipo Dev (Reglas y Guías)

| Archivo | Descripción |
|---|---|
| `README.md` | Índice del equipo BULMA |
| `MODULES.md` | Estado y mapa de módulos |
| `architecture-rules.md` | Reglas de arquitectura |
| `implementation-guidelines.md` | Guías de implementación |
| `anti-patterns.md` | Anti-patterns a evitar |
| `change-playbook.md` | Playbook de cambios |
| `module-map.md` | Mapa de módulos del sistema |

---

## 📂 05-research — Research en Curso

Carpeta para datos de mercado, investigación y documentación en proceso de análisis.

> **Estado:** research competitivo completado — 8 competidores mapeados.

---

## 📂 06-competitor-analysis — Análisis Competitivo

| Archivo | Descripción |
|---|---|
| `competitive-analysis.md` | Reporte de inteligencia competitiva — 8 competidores |
| `lelouch-strategic-analysis.md` | Análisis estratégico de Lelouch |

**Competidores analizados:**
- 🇺🇸 Buildium, AppFolio, Condo Control, Propertyware
- 🇧🇷 Superlógica, CondoLivre, TownSq
- 🇪🇺 Kastle (seguridad física)

---

## 📂 07-roadmap — Roadmap del Proyecto

| Archivo | Descripción |
|---|---|
| `module-roadmap.md` | Roadmap oficial de implementación — por Lelouch S |

---

## 🔗 Referencias del Proyecto

- **Repo:** `/home/miguel/servers/condo-py/`
- **Src:** `/home/miguel/servers/condo-py/src/`
- **Workspace docs:** `/home/miguel/.openclaw/workspace/` (archivos operativos de Misato)

---

*Última actualización: 2026-04-13 — Reorganización por Misato K*

---

## 📂 10-agents — Equipo de Agentes IA *(Nuevo 2026-04-28)*

> Documentación del equipo de IA que desarrolla el proyecto de forma autónoma.

| Archivo | Descripción |
|---|---|
| `10-agents/README.md` | Índice del equipo IA |
| `10-agents/AI_TEAM.md` | Definición completa del equipo, modelos y responsabilidades |
| `10-agents/TASKS.md` | Distribución de tareas y guía de coordinación |

### Agentes activos

| Nombre | Modelo | Rol |
|---|---|---|
| **Lelouch** | GPT 5.4 | Architect — Arquitectura, diseño técnico, planning |
| **Misato** | Minimax 2.7 | Coordinator — Coordinación, priorización, gestión de flujo |
| **Bulma** | Minimax 2.7 / DeepSeek 4 Pro / Flash | Dev Lead — Implementación Python + Next.js |
| **Miguel** | — (humano) | Technical Leader — Code review, DB modeling, visión |

*Última actualización: 2026-04-28*
