"""
Payment Proof Query Repository Implementation — with bulk enrichment.
"""
from typing import Optional, List, Tuple

from sqlalchemy import text

from library.dddpy.core_payment_proofs.domain.payment_proof_entity import PaymentProofEntity
from library.dddpy.core_payment_proofs.domain.payment_proof_query_repository import (
    PaymentProofQueryRepository,
)
from library.dddpy.core_payment_proofs.infrastructure.dbpayment_proof import DBPaymentProof
from library.dddpy.core_payment_proofs.infrastructure.payment_proof_mapper import (
    PaymentProofMapper,
)
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("PaymentProofQueryRepository")


class PaymentProofQueryRepositoryImpl(PaymentProofQueryRepository):

    def _user_names_map(self, user_ids: set) -> dict:
        if not user_ids:
            return {}
        with session_scope() as session:
            result = session.execute(
                text("""
                    SELECT u.id,
                           COALESCE(CONCAT(p.first_name, ' ', p.last_name), u.email) AS full_name
                    FROM users u
                    LEFT JOIN user_profiles p ON p.user_id = u.id AND p.deleted_at IS NULL
                    WHERE u.id IN :ids
                """),
                {"ids": tuple(user_ids)},
            )
            return {row.id: row.full_name for row in result}

    def _unit_codes_map(self, unit_ids: set) -> dict:
        if not unit_ids:
            return {}
        with session_scope() as session:
            from library.dddpy.core_units.infrastructure.dbunits import DBUnits

            result = session.query(DBUnits.id, DBUnits.code).filter(
                DBUnits.id.in_(unit_ids)
            ).all()
            return dict(result)

    def _condo_names_map(self, condo_ids: set) -> dict:
        if not condo_ids:
            return {}
        with session_scope() as session:
            from library.dddpy.core_condominiums.infrastructure.dbcondominiums import (
                DBCondominiums,
            )

            result = session.query(DBCondominiums.id, DBCondominiums.name).filter(
                DBCondominiums.id.in_(condo_ids)
            ).all()
            return dict(result)

    def _ar_refs_map(self, ar_ids: set) -> dict:
        if not ar_ids:
            return {}
        with session_scope() as session:
            from library.dddpy.core_accounts_receivable.infrastructure.dbar import DBAR

            result = session.query(
                DBAR.id, DBAR.reference_code, DBAR.amount
            ).filter(DBAR.id.in_(ar_ids)).all()
            return {
                r.id: {"reference_code": r.reference_code, "amount": float(r.amount)}
                for r in result
            }

    def _receipt_numbers_map(self, receipt_ids: set) -> dict:
        if not receipt_ids:
            return {}
        with session_scope() as session:
            from library.dddpy.core_receipts.infrastructure.dbreceipt import DBReceipt

            result = session.query(
                DBReceipt.id, DBReceipt.receipt_number
            ).filter(DBReceipt.id.in_(receipt_ids)).all()
            return dict(result)

    def _bulk_enrich(self, rows: List[DBPaymentProof]) -> List[PaymentProofEntity]:
        if not rows:
            return []

        user_ids = {r.submitted_by for r in rows}
        reviewed_ids = {r.reviewed_by for r in rows if r.reviewed_by}
        user_ids.update(reviewed_ids)
        unit_ids = {r.unit_id for r in rows}
        condo_ids = {r.condominium_id for r in rows}
        ar_ids = {r.ar_id for r in rows}
        receipt_ids = {r.receipt_id for r in rows if r.receipt_id}

        user_names = self._user_names_map(user_ids)
        unit_codes = self._unit_codes_map(unit_ids)
        condo_names = self._condo_names_map(condo_ids)
        ar_refs = self._ar_refs_map(ar_ids)
        receipt_nums = self._receipt_numbers_map(receipt_ids)

        result = []
        for row in rows:
            ar_info = ar_refs.get(row.ar_id, {})
            entity = PaymentProofMapper.to_domain_enriched(
                row,
                submitted_by_name=user_names.get(row.submitted_by),
                reviewed_by_name=user_names.get(row.reviewed_by) if row.reviewed_by else None,
                unit_code=unit_codes.get(row.unit_id),
                condominium_name=condo_names.get(row.condominium_id),
                ar_reference=ar_info.get("reference_code"),
                ar_amount=ar_info.get("amount"),
                receipt_number=receipt_nums.get(row.receipt_id) if row.receipt_id else None,
            )
            result.append(entity)
        return result

    def get_by_id(self, id: int) -> Optional[PaymentProofEntity]:
        logger.debug(f"Fetching payment proof by id={id}")
        with session_scope() as session:
            row = session.query(DBPaymentProof).filter(
                DBPaymentProof.id == id,
                DBPaymentProof.deleted_at.is_(None),
            ).first()
            if not row:
                return None
            enriched = self._bulk_enrich([row])
            return enriched[0] if enriched else None

    def get_by_uuid(self, uuid: str) -> Optional[PaymentProofEntity]:
        logger.debug(f"Fetching payment proof by uuid={uuid}")
        with session_scope() as session:
            row = session.query(DBPaymentProof).filter(
                DBPaymentProof.uuid == uuid,
                DBPaymentProof.deleted_at.is_(None),
            ).first()
            if not row:
                return None
            enriched = self._bulk_enrich([row])
            return enriched[0] if enriched else None

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
    ) -> Tuple[List[PaymentProofEntity], int]:
        logger.debug(f"Listing payment proofs skip={skip} limit={limit}")
        with session_scope() as session:
            query = session.query(DBPaymentProof)
            if not include_deleted:
                query = query.filter(DBPaymentProof.deleted_at.is_(None))
            if condominium_id is not None:
                query = query.filter(DBPaymentProof.condominium_id == condominium_id)
            if unit_id is not None:
                query = query.filter(DBPaymentProof.unit_id == unit_id)
            if ar_id is not None:
                query = query.filter(DBPaymentProof.ar_id == ar_id)
            if status:
                query = query.filter(DBPaymentProof.status == status)
            if submitted_by is not None:
                query = query.filter(DBPaymentProof.submitted_by == submitted_by)

            total = query.count()
            rows = (
                query.order_by(DBPaymentProof.created_at.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            return self._bulk_enrich(rows), total
