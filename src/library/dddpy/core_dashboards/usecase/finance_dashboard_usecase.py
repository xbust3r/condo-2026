"""
Finance Dashboard Use Case — aggregates financial metrics for a condominium.

This is a query-only facade. It consumes data from existing repositories
and returns aggregated metrics. No domain entities or repositories are
created for this module.
"""
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Optional

from library.dddpy.core_accounts_receivable.infrastructure.ar_query_repository import (
    ARQueryRepositoryImpl,
)
from library.dddpy.core_payments.infrastructure.payment_query_repository import (
    PaymentQueryRepositoryImpl,
)
from library.dddpy.core_charges.infrastructure.charge_query_repository import (
    ChargeQueryRepositoryImpl,
)
from library.dddpy.core_charge_types.infrastructure.charge_type_query_repository import (
    ChargeTypeQueryRepositoryImpl,
)


class FinanceDashboardUseCase:
    """Aggregates financial metrics for a condominium."""

    def get_dashboard(self, condominium_id: int) -> dict:
        """
        Returns financial dashboard:
        - accounts_receivable: total_pending, by_status (current, 30_days, 90_days)
        - collections: this_month (expected, collected, rate_percent)
        - recent_payments: last 10 payments
        - charges: by_charge_type breakdown
        """
        today = date.today()
        current_month_start = today.replace(day=1)
        # Next month start (for range queries on payments)
        if today.month == 12:
            next_month_start = today.replace(year=today.year + 1, month=1, day=1)
        else:
            next_month_start = today.replace(month=today.month + 1, day=1)

        cutoff_30_days = today - timedelta(days=30)
        cutoff_90_days = today - timedelta(days=90)

        ar_repo = ARQueryRepositoryImpl()
        payment_repo = PaymentQueryRepositoryImpl()
        charge_repo = ChargeQueryRepositoryImpl()
        charge_type_repo = ChargeTypeQueryRepositoryImpl()

        # ── 1. AR by aging bucket ────────────────────────────────────────────
        # Fetch all non-paid ARs for the condominium (no status filter = all;
        # we'll filter by status in Python)
        all_ar, _ = ar_repo.list_all(
            condominium_id=condominium_id,
            limit=10000,  # get them all for aggregation
        )

        ar_current = Decimal("0.00")
        ar_30_days = Decimal("0.00")
        ar_90_days = Decimal("0.00")

        for ar in all_ar:
            if ar.status in ("paid", "cancelled"):
                continue
            pending = Decimal(str(ar.amount)) - Decimal(str(ar.paid_amount))
            if pending <= 0:
                continue

            if ar.due_date >= today:
                ar_current += pending
            elif ar.due_date >= cutoff_30_days:
                ar_30_days += pending
            else:
                ar_90_days += pending

        ar_pending_total = float(ar_current + ar_30_days + ar_90_days)

        # ── 2. Collections this month ────────────────────────────────────────
        # Expected: sum of all AR with due_date in current month (non-paid)
        expected_this_month = Decimal("0.00")
        for ar in all_ar:
            if ar.status in ("paid", "cancelled"):
                continue
            if ar.due_date.year == today.year and ar.due_date.month == today.month:
                pending = Decimal(str(ar.amount)) - Decimal(str(ar.paid_amount))
                if pending > 0:
                    expected_this_month += pending

        # Collected this month: payments with paid_at in current month
        all_payments_this_month, _ = payment_repo.list_all(
            condominium_id=condominium_id,
            limit=10000,
        )

        collected_this_month = Decimal("0.00")
        for p in all_payments_this_month:
            if p.paid_at and p.paid_at.date() >= current_month_start and p.paid_at.date() < next_month_start:
                collected_this_month += Decimal(str(p.amount))

        expected_val = float(expected_this_month)
        collected_val = float(collected_this_month)
        collection_rate = (
            round((collected_val / expected_val) * 100, 1)
            if expected_val > 0
            else 0.0
        )

        # ── 3. Recent payments (last 10) ────────────────────────────────────
        recent_payments_raw, _ = payment_repo.list_all(
            condominium_id=condominium_id,
            limit=10,
        )
        recent_payments = []
        for p in recent_payments_raw:
            recent_payments.append({
                "id": p.id,
                "amount": float(p.amount),
                "unit_code": getattr(p, "unit_code", None),
                "date": p.paid_at.isoformat() if p.paid_at else None,
                "receipt_number": getattr(p, "receipt_number", None),
            })

        # ── 4. Charges by charge type ────────────────────────────────────────
        charge_types, _ = charge_type_repo.list_all(is_active=True, limit=100)
        by_charge_type = []
        for ct in charge_types:
            charges_for_type, total = charge_repo.list_all(
                condominium_id=condominium_id,
                charge_type_id=ct.id,
                limit=1,
            )
            # Sum amounts for this charge type (current period)
            charge_sum = Decimal("0.00")
            if charges_for_type:
                # Re-query with higher limit to sum
                all_charges_for_type, _ = charge_repo.list_all(
                    condominium_id=condominium_id,
                    charge_type_id=ct.id,
                    limit=10000,
                )
                for ch in all_charges_for_type:
                    charge_sum += Decimal(str(ch.amount))

            by_charge_type.append({
                "charge_type_id": ct.id,
                "charge_type_name": ct.name,
                "charge_type_code": ct.code,
                "total_amount": float(charge_sum),
            })

        # ── 5. Amenity bookings summary ──────────────────────────────────────
        booking_summary = self._get_booking_summary(condominium_id)

        return {
            "condominium_id": condominium_id,
            "as_of": datetime.utcnow().isoformat() + "Z",
            "accounts_receivable": {
                "total_pending": ar_pending_total,
                "by_status": {
                    "current": float(ar_current),
                    "30_days": float(ar_30_days),
                    "90_days": float(ar_90_days),
                },
            },
            "collections": {
                "this_month": {
                    "expected": expected_val,
                    "collected": collected_val,
                    "rate_percent": collection_rate,
                },
            },
            "recent_payments": recent_payments,
            "charges": {
                "active_charge_types": len(charge_types),
                "by_charge_type": by_charge_type,
            },
            "amenity_bookings": booking_summary,
        }

    def _get_booking_summary(self, condominium_id: int) -> dict:
        """Get amenity bookings summary for the dashboard."""
        from sqlalchemy import text
        from library.dddpy.shared.mysql.session_manager import session_scope as ss

        with ss() as session:
            result = session.execute(
                text("""
                    SELECT
                        COUNT(*) AS total,
                        SUM(CASE WHEN status = 'confirmed' THEN 1 ELSE 0 END) AS confirmed,
                        SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) AS completed,
                        COALESCE(SUM(booking_fee_amount), 0) AS total_fees,
                        COALESCE(SUM(CASE
                            WHEN deposit_status IN ('pending', 'paid')
                            THEN security_deposit_amount ELSE 0
                        END), 0) AS deposits_in_custody
                    FROM core_amenity_bookings
                    WHERE condominium_id = :condo_id
                      AND deleted_at IS NULL
                """),
                {"condo_id": condominium_id},
            ).fetchone()

        return {
            "total_bookings": int(result.total or 0),
            "confirmed": int(result.confirmed or 0),
            "completed": int(result.completed or 0),
            "total_fees": float(result.total_fees or 0),
            "deposits_in_custody": float(result.deposits_in_custody or 0),
        }
