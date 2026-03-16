"""
Constantes de estado del sistema.

Este módulo define los estados explícitos para Leads y Routing Logs,
eliminando números mágicos del código.
"""

from enum import IntEnum


class LeadStatus(IntEnum):
    """
    Estados posibles de un Lead.
    
    - PENDING_ROUTING (9): Lead recién registrado, aún no ha sido procesado por routing
    - SUCCESS (1): Lead procesado exitosamente
    - FAILURE (3): Lead falló en el procesamiento
    """
    PENDING_ROUTING = 9
    SUCCESS = 1
    FAILURE = 3


class RoutingLogStatus(IntEnum):
    """
    Estados del log de ejecución de routing.
    
    - STARTED (0): Ejecución iniciada
    - SUCCESS (1): Ejecución exitosa
    - ERROR (3): Error en la ejecución o envío
    - PROVIDER_ERROR (5): Respuesta no exitosa del proveedor externo
    """
    STARTED = 0
    SUCCESS = 1
    ERROR = 3
    PROVIDER_ERROR = 5
