"""
Payment Proof command repository interface.
"""


class PaymentProofCmdRepository:
    def create(self, data) -> int: pass
    def approve(self, proof_id: int, review_data, reviewed_by: int) -> bool: pass
    def reject(self, proof_id: int, rejection_reason: str, reviewed_by: int) -> bool: pass
    def soft_delete(self, id: int) -> bool: pass
