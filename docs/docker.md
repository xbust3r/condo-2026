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

### Ejecutar comandos

```bash
make command COMMAND="tu_comando"
```

### Ejecutar Alembic

```bash
# Copiar alembic al contenedor
docker cp alembic/ <container>:/app/

# Ejecutar migraciones
docker exec -w /app <container> alembic upgrade head

# O usar make
make alembic COMMAND="upgrade head"
```

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

- La carpeta `src/` se monta como volumen en `/app` dentro del contenedor
- Alembic lee la configuración desde `src/.env`
- El proyecto usa **FastAPI** (no Chalice)
