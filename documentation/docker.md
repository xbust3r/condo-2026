# Docker - condo-py

Este documento describe la configuración de Docker para el proyecto condo-py.

## Overview

El proyecto utiliza Docker para ejecutar la aplicación en un entorno aislado. La estructura de Docker incluye:

- **Receta CLI**: Contenedor para ejecutar comandos (migraciones, tests, etc.)
- **Receta latest**: Contenedor con la aplicación completa (servicio HTTP)

## Estructura de Docker

```
docker/
├── cli/              # Receta para CLI
│   ├── Dockerfile
│   └── resources/
└── latest/           # Receta para el servicio
    ├── Dockerfile
    ├── entrypoint.sh
    ├── nginx.conf
    └── resources/
```

## Requisitos

- Docker
- Docker Compose
- Make

## Comandos

### Construir los contenedores

```bash
make build
```

Este comando:
1. Copia las dependencias de `src/requirements.txt` a las carpetas `resources/`
2. Construye la imagen CLI
3. Construye la imagen del servicio
4. Limpia los archivos temporales

### Levantar el servicio

```bash
make up
```

Levanta el contenedor del backend y lo conecta a la red `services_network`. También agrega el dominio local `condo.test` al archivo `/etc/hosts`.

### Detener el servicio

```bash
make stop
```

Detiene los contenedores sin eliminarlos.

### Ingresar al contenedor (SSH)

```bash
make ssh
```

Abre una terminal bash dentro del contenedor en ejecución. Este es el lugar donde se ejecutan:

- Pruebas unitarias
- Migraciones de Alembic
- Cualquier comando de consola

### Ejecutar comandos en el contenedor

```bash
make command COMMAND="tu_comando"
```

Ejecuta un comando específico en un contenedor temporal.

### Ver logs

```bash
make logs
```

Muestra los logs del contenedor en tiempo real.

### Estado de los contenedores

```bash
make status
```

Muestra el estado de los contenedores.

## Red Docker

El proyecto utiliza una red llamada `services_network` para comunicarse con:

- **MySQL**: Base de datos del proyecto
- **HAProxy**: Balanceador de carga (si está configurado)

La red se crea automáticamente si no existe (`make verify_network`).

## Variables de Entorno

El contenedor espera las siguientes variables de entorno:

- `DB_USER`: Usuario de la base de datos
- `DB_PASSWORD`: Contraseña de la base de datos
- `DB_HOST`: Host de la base de datos (default: mysql)
- `DB_PORT`: Puerto de la base de datos (default: 3306)
- `DB_NAME`: Nombre de la base de datos
- `AWS_DEFAULT_REGION`: Región de AWS (para despliegue)

## Ejecución de Pruebas Unitarias

Las pruebas unitarias se ejecutan **dentro del contenedor**:

```bash
# 1. Ingresar al contenedor
make ssh

# 2. Ejecutar pytest
python -m pytest src/tests/ -v
```

O可以直接:

```bash
make command COMMAND="python -m pytest src/tests/ -v"
```

## Migraciones Alembic

同样, las migraciones se ejecutan dentro del contenedor:

```bash
# Crear migración
make ssh
#Dentro del contenedor:
alembic revision --autogenerate -m "tu_mensaje"

# Aplicar migraciones
alembic upgrade head

# Revisar historial
alembic history
```

## Notas

- La carpeta `src/` se monta como volumen en `/app` dentro del contenedor
- Los directorios `~/.ssh` y `~/.aws` se montan para acceso a claves y configuración de AWS
- El proyecto usa Chalice (AWS Serverless) para el API REST
- La imagen `latest` incluye Nginx como reverse proxy
