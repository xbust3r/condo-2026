# Documentación de `condo-py`

Este directorio separa tres niveles del tablero:

1. **Arquitectura operativa del proyecto** — cómo está organizado `condo-py` hoy.
2. **Observaciones para humanos** — explicaciones pedagógicas sobre decisiones, deudas y fronteras.
3. **Reglas tácticas para BULMA** — instrucciones compactas para una agente de IA que vaya a modificar el proyecto.

## Orden recomendado de lectura

### Para humanos
1. `architecture.md`
2. `docker.md`
3. `models/` (inventario funcional de tablas)
4. `observations/README.md`

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
├── README.md                  # índice general
├── architecture.md            # arquitectura actual del proyecto
├── docker.md                  # operación local y contenedores
├── models/                    # inventario de tablas / recursos
├── observations/              # explicación humana y pedagógica
│   ├── README.md
│   ├── architecture-observations.md
│   ├── domain-vs-application.md
│   ├── recommendations-explained.md
│   └── junior-guide.md
├── BULMA/                     # instrucciones optimizadas para IA
│   ├── README.md
│   ├── architecture-rules.md
│   ├── module-map.md
│   ├── implementation-guidelines.md
│   ├── anti-patterns.md
│   └── change-playbook.md
└── new-standard/              # base teórica de referencia; no tocar
```

## Regla importante

`docs/new-standard/` es la **base doctrinal** tomada como referencia.
No es la documentación operativa del proyecto.
No debe editarse al documentar `condo-py`, salvo que la tarea sea explícitamente actualizar esa base.

## Qué pretende esta documentación

- Aterrizar la teoría DDD a la realidad de `condo-py`.
- Explicar qué partes del diseño ya están bien.
- Dejar visibles las inconsistencias actuales sin maquillarlas.
- Dar una guía clara para humanos y para agentes de IA.

La arquitectura no debe depender de memoria tribal. Debe poder leerse como un mapa de guerra.
