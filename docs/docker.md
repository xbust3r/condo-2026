# Docker - condo-py

Este documento describe la configuración de Docker para el proyecto condo-py.

## Overview

El proyecto utiliza Docker para ejecutar la aplicación en un entorno aislado:

- **CLI**: Contenedor para ejecutar comandos (migraciones, tests, etc.)
- **dev**: Contenedor con la aplicación completa (FastAPI)

## Estructura de Docker

```
docker/
├── cli/              # Receta para CLI
│   └── Dockerfile
└── latest/           # Receta para el servicio
    ├── Dockerfile
    └── entrypoint.sh
```

## Comandos

### Construir los contenedores

```bash
make build
```

### Levantar el servicio

```bash
make up
```

Levanta el contenedor del backend y lo conecta a la red `services_network`.

### Detener el servicio

```bash
make stop
```

### Ingresar al contenedor

```bash
make ssh
```

### Ejecutar comandos genéricos

```bash
make command COMMAND="tu_comando"
```

Usa este target para comandos generales del proyecto dentro del contenedor CLI, por ejemplo:

```bash
make command COMMAND="pytest"
make command COMMAND="pytest -q"
make command COMMAND="python script.py"
```

### Cuándo usar `make command`

Úsalo para tareas que viven principalmente en `src/`, como:

- pruebas unitarias o de integración con `pytest`
- scripts Python
- comandos generales de desarrollo

Este target monta `src/` dentro del contenedor en `/app`.

### Ejecutar Alembic

```bash
make alembic COMMAND="alembic upgrade head"
```

También puedes usar otros comandos de migración:

```bash
make alembic COMMAND="alembic revision --autogenerate -m 'add new field'"
make alembic COMMAND="alembic current"
make alembic COMMAND="alembic history"
```

### Cuándo usar `make alembic`

Úsalo específicamente para migraciones, porque este target monta la raíz completa del repositorio en `/app` y deja disponible el directorio `alembic/`.

En otras palabras:

- **`make command`** → comandos generales y pruebas
- **`make alembic`** → migraciones y comandos de Alembic

No se recomienda usar `make command` para Alembic si el comando necesita acceder a la estructura completa del repo.

## Red Docker

El proyecto usa la red `services_network` para comunicarse con:

- **MySQL** (`services_mysql`): Base de datos
- **HAProxy** (`balancer`): Balanceador

## Variables de Entorno (src/.env)

```env
MYSQL_USER=root
MYSQL_PASSWORD=123456
MYSQL_HOST=mysql
MYSQL_PORT=3306
MYSQL_DB=db_condominiums
```

## Notas

- `make command` monta la carpeta `src/` como volumen en `/app` dentro del contenedor CLI
- `make alembic` monta la raíz completa del repositorio en `/app`
- Alembic lee la configuración desde `src/.env`
- El proyecto usa **FastAPI** (no Chalice)
