import os
import boto3
import json
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from chalicelib.dddpy.shared.logging.logging import Logger

logger = Logger("session_manager")


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

    logger.debug(f"Connecting to DB: {DB_HOST}:{DB_PORT}/{DB_NAME}")

    password = ""
    ssl_args = {}

    if IAM_AUTH_RDS.upper() == "ENABLED":
        aws_region = "us-west-1"
        rds_client = boto3.client("rds", region_name=aws_region)
        try:
            password = rds_client.generate_db_auth_token(
                DBHostname=DB_HOST,
                Port=int(DB_PORT),
                DBUsername=DB_USER,
                Region=aws_region,
            )
            ssl_args = {"sslmode": "require"}
        except Exception as e:
            logger.error(f"Failed to generate IAM token: {e}")
            raise
    else:
        secret_arn = os.environ.get("DB_SECRET_ARN")
        if secret_arn:
            try:
                secrets_client = boto3.client("secretsmanager", region_name="us-west-1")
                secret = secrets_client.get_secret_value(SecretId=secret_arn)
                secret_string = secret["SecretString"]
                try:
                    secret_dict = json.loads(secret_string)
                    password = secret_dict.get("password")
                    if password is None:
                        raise ValueError("No password key in secret")
                except (json.JSONDecodeError, ValueError):
                    password = secret_string
            except Exception as e:
                logger.error(f"Failed to get password from Secrets Manager: {e}")
                password = os.environ.get("DB_PASSWORD")
                if not password:
                    raise
        else:
            password = os.environ.get("DB_PASSWORD")

    DATABASE_URL = (
        f"postgresql+psycopg2://{DB_USER}:{password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    engine = create_engine(DATABASE_URL, connect_args=ssl_args, echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return SessionLocal()


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = get_session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Database session error: {e}")
        raise
    finally:
        session.close()
