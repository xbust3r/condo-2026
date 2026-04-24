"""
Payment command repository interface — abstract.
"""
from abc import ABC, abstractmethod
from typing import Optional

from library.dddpy.core_payments.domain.payment_data import CreatePaymentData
from library.dddpy.core_payments.domain.payment_entity import PaymentEntity


class PaymentCmdRepository(ABC):
    """Abstract write repository for payments."""

    @abstractmethod
    def create(self, data: CreatePaymentData, receipt_id: int) -> PaymentEntity:
        pass
