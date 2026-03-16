# MySQL Base configuration for SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DB_USER = os.environ.get("MYSQL_USER", "stg_panelhub")
DB_PASSWORD = os.environ.get("MYSQL_PASSWORD", "c3p4NFSbiddUDMPhOpLmXknff/Y=")
DB_HOST = os.environ.get("MYSQL_HOST", "herav4-production.cluster-cymuhlhwsajk.us-west-2.rds.amazonaws.com")
DB_PORT = os.environ.get("MYSQL_PORT", "3306")
DB_NAME = os.environ.get("MYSQL_DB", "stg_panelhub")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
