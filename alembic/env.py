# Alembic Environment - Loads .env from src/
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Load .env from src/
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'src', '.env'))

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Import models AFTER path is set
from library.dddpy.shared.mysql.base import Base
from library.dddpy.core_condominiums.infrastructure.condominiums import DBCondominiums
from library.dddpy.core_buildings_types.infrastructure.buildings_types import DBBuildingsTypes
from library.dddpy.core_buildings.infrastructure.buildings import DBBuildings
from library.dddpy.core_unittys_types.infrastructure.unittys_types import DBUnittysTypes
from library.dddpy.core_unitys.infrastructure.unitys import DBUnitys
from library.dddpy.users.infrastructure.users import DBUsers
from library.dddpy.users_residents.infrastructure.residents import DBResidents

# Get config from alembic
config = context.config

# Load database URL from environment variables (always override)
DB_USER = os.environ.get("MYSQL_USER", "root")
DB_PASSWORD = os.environ.get("MYSQL_PASSWORD", "123456")
DB_HOST = os.environ.get("MYSQL_HOST", "mysql")
DB_PORT = os.environ.get("MYSQL_PORT", "3306")
DB_NAME = os.environ.get("MYSQL_DB", "db_condominiums")

# Build URL and set it
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
config.set_main_option("sqlalchemy.url", DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
