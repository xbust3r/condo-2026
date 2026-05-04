"""
Payment Proof query repository interface.
"""
from typing import Optional, List, Tuple

from library.dddpy.core_payment_proofs.domain.payment_proof_entity import PaymentProofEntity


class PaymentProofQueryRepository:
    def get_by_id(self, id: int) -> Optional[PaymentProofEntity]: pass
    def get_by_uuid(self, uuid: str) -> Optional[PaymentProofEntity]: pass
    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        unit_id: Optional[int] = None,
        ar_id: Optional[int] = None,
        status: Optional[str] = None,
        submitted_by: Optional[int] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[PaymentProofEntity], int]: pass
