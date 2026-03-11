# Patrón de Conexiones de Base de Datos para AWS Lambda

## Problema Solucionado

Este módulo resuelve el error común en AWS Lambda: `FATAL: The IAM authentication failed` que ocurre cuando se reutilizan conexiones con tokens IAM expirados.

## ¿Por Qué Ocurre el Error?

1. **Cold Start**: Primera invocación crea un nuevo contenedor con engine global
2. **Warm Start**: AWS reutiliza el contenedor pero el token IAM (15 min) ya expiró
3. **Error**: La base de datos rechaza el token obsoleto

## Solución Implementada

### Patrón Unificado en `session_manager.py`

Toda la lógica de conexión está centralizada en `session_manager.py`:

```python
def get_session():
    """
    Crea un nuevo engine y devuelve una nueva sesión de base de datos,
    asegurando que se genere un nuevo token de IAM para cada uso.
    """
    # Genera nuevo token IAM cada vez
    password = rds_client.generate_db_auth_token(...)
    # Crea nuevo engine
    engine = create_engine(DATABASE_URL, ...)
    # Devuelve sesión fresca
    return SessionLocal()

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = get_session()  # <-- USA LA FUNCIÓN CORRECTA AQUÍ
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error en la sesión de base de datos: {e}")
        raise
    finally:
        session.close()
```

### Uso en Repositorios

**Patrón Correcto** (ya implementado en todos los repositorios):

```python
from chalicelib.dddpy.shared.postgresql.session_manager import session_scope

class MiRepositorioImpl:
    def create(self, data):
        with session_scope() as session:
            # Cada operación obtiene sesión fresca con token nuevo
            nuevo_registro = MiTabla(data)
            session.add(nuevo_registro)
            session.commit()
            return nuevo_registro
```

**Patrón Incorrecto** (NO usar):

```python
# ❌ NO crear engine global
engine = create_engine(...)
SessionLocal = sessionmaker(bind=engine)

# ❌ NO usar sesiones globales
session = SessionLocal()
```

## Beneficios

✅ **Token IAM fresco** por operación
✅ **Compatible** con ciclo de vida Lambda
✅ **Sin conexiones obsoletas**
✅ **Manejo automático** de errores y commits
✅ **Cierre automático** de sesiones
✅ **Lógica centralizada** en un solo archivo

## Configuración de Variables de Entorno

```bash
# Para IAM Authentication (Producción)
DB_USER=miusuario
DB_HOST=mi-rds.amazonaws.com
DB_PORT=5432
DB_NAME=midb
IAM_AUTH_RDS=ENABLED

# Para desarrollo local (opcional)
DB_PASSWORD=mipassword
IAM_AUTH_RDS=DISABLED
```

## Arquitectura

```
Lambda Invocation → session_scope() → get_session() → Nuevo Token IAM → Nueva Sesión → Operación DB → Cierre Sesión
```

## Archivos Importantes

- **`session_manager.py`**: Contiene toda la lógica de conexión y gestión de sesiones
- **`base.py`**: Solo contiene la definición de `Base` para modelos SQLAlchemy
- **`README.md`**: Esta documentación

Este patrón asegura que cada operación de base de datos use credenciales completamente nuevas, eliminando el riesgo de tokens expirados.