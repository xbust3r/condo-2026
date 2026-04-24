"""
Incident factory — builds cmd and query use case instances.
"""
from library.dddpy.core_incidents.infrastructure.incident_cmd_repository import IncidentCmdRepositoryImpl
from library.dddpy.core_incidents.infrastructure.incident_query_repository import IncidentQueryRepositoryImpl
from library.dddpy.core_incidents.usecase.incident_cmd_usecase import IncidentCmdUseCase
from library.dddpy.core_incidents.usecase.incident_query_usecase import IncidentQueryUseCase


def incident_cmd_usecase_factory() -> IncidentCmdUseCase:
    return IncidentCmdUseCase(repository=IncidentCmdRepositoryImpl())


def incident_query_usecase_factory() -> IncidentQueryUseCase:
    return IncidentQueryUseCase(repository=IncidentQueryRepositoryImpl())
