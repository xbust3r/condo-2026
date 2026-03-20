# Documentación de `condo-py`

Este directorio separa tres niveles del tablero:

1. **Arquitectura operativa del proyecto** — cómo debe organizarse el código hoy.
2. **Observaciones para humanos** — explicaciones pedagógicas sobre decisiones, deudas y fronteras.
3. **Reglas tácticas para BULMA** — instrucciones compactas para una agente de IA que vaya a modificar el proyecto.

## Base actual del proyecto

La referencia arquitectónica vigente es:

- `src/library/dddpy/shared/` → base transversal compartida
- `src/library/dddpy/example/` → módulo patrón para nuevas implementaciones
- `src/api/example/` → referencia del patrón de route limpio con `@api_handler`
- `src/app.py` → borde FastAPI actual del servicio

Los módulos viejos no deben tomarse como fuente doctrinal si contradicen esta base.

## Orden recomendado de lectura

### Para humanos
1. `architecture.md`
2. `observations/README.md`
3. `docker.md`
4. `models/` (si aplica como inventario de tablas)

### Para agentes de IA
1. `BULMA/README.md`
2. `BULMA/architecture-rules.md`
3. `BULMA/module-map.md`
4. `BULMA/implementation-guidelines.md`
5. `BULMA/anti-patterns.md`
6. `BULMA/change-playbook.md`

## Mapa del directorio

```text
docs/
├── README.md
├── architecture.md
├── docker.md
├── models/
├── observations/
│   ├── README.md
│   ├── architecture-observations.md
│   ├── domain-vs-application.md
│   ├── recommendations-explained.md
│   └── junior-guide.md
├── BULMA/
│   ├── README.md
│   ├── architecture-rules.md
│   ├── module-map.md
│   ├── implementation-guidelines.md
│   ├── anti-patterns.md
│   └── change-playbook.md
└── new-standard/
```

## Regla importante

`docs/new-standard/` es la base doctrinal de referencia.
No debe editarse durante documentación operativa normal del proyecto.

## Qué pretende esta documentación

- Aterrizar la teoría DDD a la base real actual.
- Hacer explícito el patrón de módulo basado en `example`.
- Dejar claro el uso de mapper, exceptions compartidas, response schemas y `@api_handler`.
- Dar una guía útil tanto para humanos como para BULMA.

La arquitectura no debe depender de memoria tribal.
Debe leerse como un mapa de guerra reproducible.
