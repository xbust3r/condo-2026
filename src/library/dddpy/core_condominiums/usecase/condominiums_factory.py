# Condominium Factory
from library.dddpy.core_condominiums.domain.condominiums_repository import CondominiumRepository
from library.dddpy.core_condominiums.infrastructure.condominiums_cmd_repository import CondominiumCmdRepositoryImpl
from library.dddpy.core_condominiums.usecase.condominiums_usecase import CondominiumUseCase


def create_condominium_repository() -> CondominiumRepository:
    """Factory function to create Condominium repository"""
    return CondominiumCmdRepositoryImpl()


def create_condominium_usecase() -> CondominiumUseCase:
    """Factory function to create Condominium use case"""
    repository = create_condominium_repository()
    return CondominiumUseCase(repository)
