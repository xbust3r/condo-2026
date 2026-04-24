"""
from typing import Optional
Receipt use case — orchestrates all receipt operations.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional

from library.dddpy.core_receipts.usecase.receipt_cmd_schema import CreateReceiptSchema
from library.dddpy.core_receipts.domain.receipt_entity import ReceiptEntity
from library.dddpy.core_receipts.domain.receipt_exception import ReceiptNotFound
from library.dddpy.core_receipts.domain.receipt_success import ReceiptSuccessMessage
from library.dddpy.core_receipts.infrastructure.receipt_cmd_repository import ReceiptCmdRepositoryImpl
from library.dddpy.core_receipts.infrastructure.receipt_query_repository import ReceiptQueryRepositoryImpl
from library.dddpy.shared.schemas.response_schema import ResponseSuccessSchema
from library.dddpy.shared.logging.logging import Logger


logger = Logger("ReceiptUseCase")


class ReceiptUseCase:

    def __init__(self):
        self._cmd = ReceiptCmdRepositoryImpl()
        self._query = ReceiptQueryRepositoryImpl()
        logger.info("ReceiptUseCase initialized")

    def create(self, data: CreateReceiptSchema) -> ReceiptEntity:
        logger.add_inside_method("create") if hasattr(logger, 'add_inside_method') else None
        cmd_data = self._cmd.create(data)
        return cmd_data

    def get_next_receipt_number(self, condominium_id: int) -> str:
        return self._cmd.get_next_receipt_number(condominium_id)

    def get_by_id(self, id: int):
        entity = self._query.get_by_id(id)
        if not entity:
            raise ReceiptNotFound()
        return ResponseSuccessSchema(
            success=True,
            message=ReceiptSuccessMessage.RETRIEVED,
            data=entity.to_dict(),
        )

    def get_by_uuid(self, uuid: str):
        entity = self._query.get_by_uuid(uuid)
        if not entity:
            raise ReceiptNotFound()
        return ResponseSuccessSchema(
            success=True,
            message=ReceiptSuccessMessage.RETRIEVED,
            data=entity.to_dict(),
        )

    def get_by_receipt_number(self, receipt_number: str):
        entity = self._query.get_by_receipt_number(receipt_number)
        if not entity:
            raise ReceiptNotFound()
        return ResponseSuccessSchema(
            success=True,
            message=ReceiptSuccessMessage.RETRIEVED,
            data=entity.to_dict(),
        )

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        unit_id: Optional[int] = None,
        ar_id: Optional[int] = None,
    ) -> ResponseSuccessSchema:
        if limit > 500:
            limit = 500
        entities, total = self._query.list_all(
            skip=skip, limit=limit,
            condominium_id=condominium_id,
            unit_id=unit_id,
            ar_id=ar_id,
        )
        return ResponseSuccessSchema(
            success=True,
            message=ReceiptSuccessMessage.LISTED,
            data={
                "items": [e.to_dict() for e in entities],
                "total": total,
                "skip": skip,
                "limit": limit,
            },
        )

    def list_by_unit(self, unit_id: int, skip: int = 0, limit: int = 100) -> ResponseSuccessSchema:
        entities, total = self._query.list_by_unit(unit_id=unit_id, skip=skip, limit=limit)
        return ResponseSuccessSchema(
            success=True,
            message=ReceiptSuccessMessage.LISTED,
            data={
                "items": [e.to_dict() for e in entities],
                "total": total,
                "skip": skip,
                "limit": limit,
            },
        )
