import os
import boto3
import json
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_session():
    """
    Crea un nuevo engine y devuelve una nueva sesión de base de datos,
    asegurando que se genere un nuevo token de IAM para cada uso.
    """
    DB_USER = os.environ.get("DB_USER")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT", "5432")
    DB_NAME = os.environ.get("DB_NAME")
    IAM_AUTH_RDS = os.environ.get("IAM_AUTH_RDS", "DISABLED")

    # --- LOGGING DETALLADO PARA DEPURACIÓN ---
    print("--- INICIANDO CONEXIÓN A LA BASE DE DATOS ---")
    print(f"DB_HOST: {DB_HOST}")
    print(f"DB_USER: {DB_USER}")
    print(f"DB_PORT: {DB_PORT}")
    print(f"DB_NAME: {DB_NAME}")
    print(f"IAM_AUTH_RDS: {IAM_AUTH_RDS}")
    print(f"Timestamp: {__import__('datetime').datetime.now()}")
    # ------------------------------------------------

    password = ""
    ssl_args = {}

    if IAM_AUTH_RDS.upper() == "ENABLED":
        aws_region = 'us-west-1'
        rds_client = boto3.client('rds', region_name=aws_region)
        try:
            print("Generando token de autenticación IAM...")
            password = rds_client.generate_db_auth_token(
                DBHostname=DB_HOST, Port=int(DB_PORT), DBUsername=DB_USER, Region=aws_region
            )
            print("Token generado exitosamente.")
            ssl_args = {'sslmode': 'require'}
        except Exception as e:
            # --- LOGGING MEJORADO PARA ERRORES ---
            print(f"ERROR: No se pudo generar el token de IAM. Excepción: {type(e).__name__} - {e}")
            print(f"Detalles del error: {str(e)}")
            # -----------------------------------------
            raise
    else:
        print("Autenticación IAM deshabilitada, obteniendo contraseña...")
        secret_arn = os.environ.get("DB_SECRET_ARN")
        print(f"DB_SECRET_ARN: {secret_arn}")
        if secret_arn:
            try:
                secrets_client = boto3.client('secretsmanager', region_name='us-west-1')
                print("Cliente de Secrets Manager creado.")
                secret = secrets_client.get_secret_value(SecretId=secret_arn)
                print("Secreto obtenido.")
                secret_string = secret['SecretString']
                try:
                    secret_dict = json.loads(secret_string)
                    print(f"Secreto parseado como JSON: {list(secret_dict.keys())}")
                    password = secret_dict.get('password')
                    if password is None:
                        print("Clave 'password' no encontrada en el secreto JSON.")
                        raise ValueError("No password key in secret")
                except (json.JSONDecodeError, ValueError):
                    print("Secreto no es JSON, asumiendo que es la contraseña directamente.")
                    password = secret_string
                print(f"Contraseña obtenida desde Secrets Manager, longitud: {len(password) if password else 0}")
            except Exception as e:
                print(f"Error obteniendo contraseña desde Secrets Manager: {e}")
                print("Intentando usar DB_PASSWORD desde variables de entorno...")
                password = os.environ.get("DB_PASSWORD")
                if not password:
                    print("DB_PASSWORD no está configurada.")
                    raise
                print("Usando DB_PASSWORD.")
        else:
            password = os.environ.get("DB_PASSWORD")
            print("Usando autenticación por contraseña desde variable de entorno (desarrollo)")

    DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    print(f"DATABASE_URL construida: postgresql+psycopg2://{DB_USER}:[TOKEN]@{DB_HOST}:{DB_PORT}/{DB_NAME}")

    print("Creando engine de SQLAlchemy...")
    engine = create_engine(DATABASE_URL, connect_args=ssl_args, echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    print("Sesión creada exitosamente. Preparando para devolver.")
    return SessionLocal()

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    print("--- INICIANDO NUEVA TRANSACCIÓN DE BASE DE DATOS ---")
    session = get_session()  # <-- USA LA FUNCIÓN CORRECTA AQUÍ
    try:
        print("Transacción iniciada. Ejecutando operaciones...")
        yield session
        print("Operaciones completadas. Realizando commit...")
        session.commit()
        print("Commit realizado exitosamente.")
    except Exception as e:
        print(f"--- ERROR EN LA SESIÓN DE BASE DE DATOS ---")
        print(f"Realizando rollback de la transacción...")
        session.rollback()
        print(f"Tipo de error: {type(e).__name__}")
        print(f"Mensaje de error: {str(e)}")
        print(f"Error completo: {e}")
        # Re-lanzar la excepción para que llegue al código que la llama
        raise
    finally:
        print("Cerrando sesión de base de datos...")
        session.close()
        print("Sesión cerrada.")
