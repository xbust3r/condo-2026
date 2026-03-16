# Core Condominiums Module
from library.dddpy.core_condominiums.domain import (
    Condominium,
    CondominiumException,
    CondominiumNotFoundException,
    CondominiumAlreadyExistsException,
    CondominiumValidationException,
    CondominiumRepository,
)
from library.dddpy.core_condominiums.infrastructure import (
    DBCondominiums,
    CondominiumMapper,
    CondominiumCmdRepositoryImpl,
    CondominiumQueryRepositoryImpl,
)
from library.dddpy.core_condominiums.usecase.condominiums_usecase import CondominiumUseCase
from library.dddpy.core_condominiums.usecase.condominiums_factory import create_condominium_usecase

# Command schemas
from library.dddpy.core_condominiums.usecase.cmd import (
    CreateCondominiumCmdSchema,
    UpdateCondominiumCmdSchema,
)

# Query schemas
from library.dddpy.core_condominiums.usecase.query import (
    CondominiumQuerySchema,
    CondominiumListQuerySchema,
)

__all__ = [
    # Domain
    "Condominium",
    "CondominiumException",
    "CondominiumNotFoundException",
    "CondominiumAlreadyExistsException",
    "CondominiumValidationException",
    "CondominiumRepository",
    # Infrastructure
    "DBCondominiums",
    "CondominiumMapper",
    "CondominiumCmdRepositoryImpl",
    "CondominiumQueryRepositoryImpl",
    # Use Case
    "CondominiumUseCase",
    "create_condominium_usecase",
    # Command Schemas
    "CreateCondominiumCmdSchema",
    "UpdateCondominiumCmdSchema",
    # Query Schemas
    "CondominiumQuerySchema",
    "CondominiumListQuerySchema",
]
