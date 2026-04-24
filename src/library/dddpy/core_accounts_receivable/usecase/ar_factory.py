"""
AccountsReceivable factory — singleton factory for use case instances.
"""
from library.dddpy.core_accounts_receivable.usecase.ar_cmd_usecase import (
    ARCmdUseCase,
    ar_cmd_usecase_factory,
)
from library.dddpy.core_accounts_receivable.usecase.ar_query_usecase import (
    ARQueryUseCase,
    ar_query_usecase_factory,
)


__all__ = [
    "ARCmdUseCase",
    "ar_cmd_usecase_factory",
    "ARQueryUseCase",
    "ar_query_usecase_factory",
]
