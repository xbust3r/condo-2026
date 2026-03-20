import os
import boto3

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from library.dddpy.shared.logging.logging import Logger


logger = Logger("PostgreSQLBase")


Base = declarative_base()

def get_db_engine_and_session():
    """
    Crea y devuelve un engine y una session factory de SQLAlchemy.
    Esta función se debe llamar dentro de tu lógica de negocio.
    """
    DB_USER = os.environ.get("DB_USER")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT", "5432")
    DB_NAME = os.environ.get("DB_NAME")
    IAM_AUTH_RDS = os.environ.get("IAM_AUTH_RDS", "DISABLED")

    password = ""
    ssl_args = {}

    if IAM_AUTH_RDS.upper() == "ENABLED":
        aws_region = 'us-west-1'
        rds_client = boto3.client('rds', region_name=aws_region)
        try:
            password = rds_client.generate_db_auth_token(
                DBHostname=DB_HOST,
                Port=int(DB_PORT),
                DBUsername=DB_USER,
                Region=aws_region
            )
            # Para SQLAlchemy, los argumentos SSL se pasan por separado
            ssl_args = {'sslmode': 'require'}
        except Exception as e:
            logger.error(f"Could not generate IAM auth token: {e}")
            raise
    else:
        # Fallback a la contraseña si no es IAM (para pruebas locales, etc.)
        password = os.environ.get("DB_PASSWORD")

    DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Crea el engine aquí, dentro de la función
    engine = create_engine(
        DATABASE_URL,
        connect_args=ssl_args,  # Pasa los argumentos SSL aquí
        echo=False
    )

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, SessionLocal