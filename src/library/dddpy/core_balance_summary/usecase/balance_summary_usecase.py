"""
Balance Summary Use Case — aggregated balance with separate rubros.

Rubros:
- maintenance:         ARs from maintenance charges (charge-based)
- extraordinary:       ARs from extraordinary charges
- amenity_bookings:    ARs from amenity booking fees (origin_type=amenity_booking_fee)
- security_deposits:   ARs from security deposits in custody (origin_type=amenity_security_deposit, not returned)

Query-only facade. Consumes AR/booking/charge data and returns aggregated balance.
"""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import text

from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("BalanceSummaryUseCase")


class BalanceSummaryUseCase:
    """Aggregates balance with separate rubros for building/condominium."""

    def get_condominium_balance(self, condominium_id: int) -> dict:
        """
        Balance consolidado del condominio con rubros separados.

        Returns maintenance, extraordinary, amenity bookings, and security
        deposits as separate line items.
        """
        today = date.today()
        period = today.strftime('%Y-%m')

        with session_scope() as session:
            # ── Maintenance ARs (charge-based, not booking-related) ──
            maintenance = self._query_ar_summary(
                session, condominium_id=condominium_id,
                origin_filter="charge_based",
            )

            # ── Amenity Booking Fees ──
            booking_fees = self._query_ar_summary(
                session, condominium_id=condominium_id,
                origin_filter="amenity_booking_fee",
            )

            # ── Security Deposits in Custody ──
            security_deposits = self._query_ar_summary(
                session, condominium_id=condominium_id,
                origin_filter="amenity_security_deposit",
            )

            # ── Booking Stats ──
            booking_stats = self._query_booking_stats(session, condominium_id)

        total_expected = (
            maintenance['expected'] +
            booking_fees['expected'] +
            security_deposits['expected']
        )
        total_collected = (
            maintenance['collected'] +
            booking_fees['collected'] +
            security_deposits['collected']
        )

        return {
            "condominium_id": condominium_id,
            "period": period,
            "as_of": datetime.utcnow().isoformat() + "Z",
            "total": {
                "expected": round(total_expected, 2),
                "collected": round(total_collected, 2),
                "pending": round(total_expected - total_collected, 2),
                "collection_rate_pct": (
                    round((total_collected / total_expected) * 100, 1)
                    if total_expected > 0 else 0.0
                ),
            },
            "rubros": {
                "maintenance": {
                    "label": "Mantenimiento",
                    "expected": round(maintenance['expected'], 2),
                    "collected": round(maintenance['collected'], 2),
                    "pending": round(maintenance['expected'] - maintenance['collected'], 2),
                    "ar_count": maintenance['count'],
                },
                "amenity_bookings": {
                    "label": "Reservas de Áreas Comunes",
                    "expected": round(booking_fees['expected'], 2),
                    "collected": round(booking_fees['collected'], 2),
                    "pending": round(booking_fees['expected'] - booking_fees['collected'], 2),
                    "ar_count": booking_fees['count'],
                    "booking_count": booking_stats['total_bookings'],
                    "confirmed": booking_stats['confirmed'],
                    "completed": booking_stats['completed'],
                },
                "security_deposits": {
                    "label": "Garantías en Custodia",
                    "expected": round(security_deposits['expected'], 2),
                    "collected": round(security_deposits['collected'], 2),
                    "pending": round(security_deposits['expected'] - security_deposits['collected'], 2),
                    "ar_count": security_deposits['count'],
                    "in_custody": booking_stats['deposits_in_custody'],
                },
            },
        }

    def get_unit_balance(self, unit_id: int) -> dict:
        """
        Balance de unidad con rubros separados.

        Incluye contexto de edificio y condominio para trazabilidad.
        """
        from library.dddpy.core_units.infrastructure.unit_query_repository import (
            UnitQueryRepositoryImpl,
        )
        from library.dddpy.core_buildings.infrastructure.building_query_repository import (
            BuildingQueryRepositoryImpl,
        )
        unit_repo = UnitQueryRepositoryImpl()
        unit = unit_repo.get_by_id(unit_id)
        if not unit:
            return {"error": f"Unit id={unit_id} not found"}

        building_repo = BuildingQueryRepositoryImpl()
        building = building_repo.get_by_id(unit.building_id)
        condominium_id = building.condominium_id if building else None

        today = date.today()
        period = today.strftime('%Y-%m')

        with session_scope() as session:
            maintenance = self._query_ar_summary(
                session, condominium_id=condominium_id,
                unit_id=unit_id, origin_filter="charge_based",
            )
            booking_fees = self._query_ar_summary(
                session, condominium_id=condominium_id,
                unit_id=unit_id, origin_filter="amenity_booking_fee",
            )
            security_deposits = self._query_ar_summary(
                session, condominium_id=condominium_id,
                unit_id=unit_id, origin_filter="amenity_security_deposit",
            )
            booking_stats = self._query_booking_stats(
                session, condominium_id, unit_id=unit_id,
            )

        total_expected = (
            maintenance['expected'] +
            booking_fees['expected'] +
            security_deposits['expected']
        )
        total_collected = (
            maintenance['collected'] +
            booking_fees['collected'] +
            security_deposits['collected']
        )

        return {
            "unit_id": unit_id,
            "unit_number": getattr(unit, 'unit_number', None),
            "building_id": unit.building_id,
            "building_name": building.name if building else None,
            "condominium_id": condominium_id,
            "period": period,
            "as_of": datetime.utcnow().isoformat() + "Z",
            "total": {
                "expected": round(total_expected, 2),
                "collected": round(total_collected, 2),
                "pending": round(total_expected - total_collected, 2),
                "collection_rate_pct": (
                    round((total_collected / total_expected) * 100, 1)
                    if total_expected > 0 else 0.0
                ),
            },
            "rubros": {
                "maintenance": {
                    "label": "Mantenimiento",
                    "expected": round(maintenance['expected'], 2),
                    "collected": round(maintenance['collected'], 2),
                    "pending": round(maintenance['expected'] - maintenance['collected'], 2),
                    "ar_count": maintenance['count'],
                },
                "amenity_bookings": {
                    "label": "Reservas de Áreas Comunes",
                    "expected": round(booking_fees['expected'], 2),
                    "collected": round(booking_fees['collected'], 2),
                    "pending": round(booking_fees['expected'] - booking_fees['collected'], 2),
                    "ar_count": booking_fees['count'],
                    "booking_count": booking_stats['total_bookings'],
                    "confirmed": booking_stats['confirmed'],
                    "completed": booking_stats['completed'],
                },
                "security_deposits": {
                    "label": "Garantías en Custodia",
                    "expected": round(security_deposits['expected'], 2),
                    "collected": round(security_deposits['collected'], 2),
                    "pending": round(security_deposits['expected'] - security_deposits['collected'], 2),
                    "ar_count": security_deposits['count'],
                    "in_custody": booking_stats['deposits_in_custody'],
                },
            },
        }

    def get_building_balance(self, building_id: int) -> dict:
        """
        Balance de edificio con rubros separados.
        """
        from library.dddpy.core_buildings.infrastructure.building_query_repository import (
            BuildingQueryRepositoryImpl,
        )
        building_repo = BuildingQueryRepositoryImpl()
        building = building_repo.get_by_id(building_id)
        condominium_id = building.condominium_id if building else None

        if not building:
            return {"error": f"Building id={building_id} not found"}

        today = date.today()
        period = today.strftime('%Y-%m')

        with session_scope() as session:
            maintenance = self._query_ar_summary(
                session, condominium_id=condominium_id,
                building_id=building_id, origin_filter="charge_based",
            )
            booking_fees = self._query_ar_summary(
                session, condominium_id=condominium_id,
                building_id=building_id, origin_filter="amenity_booking_fee",
            )
            security_deposits = self._query_ar_summary(
                session, condominium_id=condominium_id,
                building_id=building_id, origin_filter="amenity_security_deposit",
            )
            booking_stats = self._query_booking_stats(
                session, condominium_id, building_id=building_id,
            )

        total_expected = (
            maintenance['expected'] +
            booking_fees['expected'] +
            security_deposits['expected']
        )
        total_collected = (
            maintenance['collected'] +
            booking_fees['collected'] +
            security_deposits['collected']
        )

        return {
            "building_id": building_id,
            "condominium_id": condominium_id,
            "building_name": building.name if building else None,
            "period": period,
            "as_of": datetime.utcnow().isoformat() + "Z",
            "total": {
                "expected": round(total_expected, 2),
                "collected": round(total_collected, 2),
                "pending": round(total_expected - total_collected, 2),
                "collection_rate_pct": (
                    round((total_collected / total_expected) * 100, 1)
                    if total_expected > 0 else 0.0
                ),
            },
            "rubros": {
                "maintenance": {
                    "label": "Mantenimiento",
                    "expected": round(maintenance['expected'], 2),
                    "collected": round(maintenance['collected'], 2),
                    "pending": round(maintenance['expected'] - maintenance['collected'], 2),
                    "ar_count": maintenance['count'],
                },
                "amenity_bookings": {
                    "label": "Reservas de Áreas Comunes",
                    "expected": round(booking_fees['expected'], 2),
                    "collected": round(booking_fees['collected'], 2),
                    "pending": round(booking_fees['expected'] - booking_fees['collected'], 2),
                    "ar_count": booking_fees['count'],
                    "booking_count": booking_stats['total_bookings'],
                    "confirmed": booking_stats['confirmed'],
                    "completed": booking_stats['completed'],
                },
                "security_deposits": {
                    "label": "Garantías en Custodia",
                    "expected": round(security_deposits['expected'], 2),
                    "collected": round(security_deposits['collected'], 2),
                    "pending": round(security_deposits['expected'] - security_deposits['collected'], 2),
                    "ar_count": security_deposits['count'],
                    "in_custody": booking_stats['deposits_in_custody'],
                },
            },
        }

    # ── Query helpers ─────────────────────────────────────────────────

    def _query_ar_summary(
        self,
        session,
        condominium_id: int,
        building_id: Optional[int] = None,
        unit_id: Optional[int] = None,
        origin_filter: str = "charge_based",
    ) -> dict:
        """
        Query AR totals filtered by origin type.

        origin_filter:
        - "charge_based": origin_type IS NULL (traditional maintenance charges)
        - "amenity_booking_fee": origin_type = 'amenity_booking_fee'
        - "amenity_security_deposit": origin_type = 'amenity_security_deposit'
        """
        origin_clause = {
            "charge_based": "ar.origin_type IS NULL",
            "amenity_booking_fee": "ar.origin_type = 'amenity_booking_fee'",
            "amenity_security_deposit": "ar.origin_type = 'amenity_security_deposit'",
        }.get(origin_filter, "ar.origin_type IS NULL")

        extra_joins = ""
        extra_wheres = []
        params = {"condo_id": condominium_id}

        if unit_id is not None:
            extra_wheres.append("ar.unit_id = :unit_id")
            params["unit_id"] = unit_id
        elif building_id is not None:
            extra_joins = "JOIN core_units u ON u.id = ar.unit_id"
            extra_wheres.append("u.building_id = :building_id")
            params["building_id"] = building_id

        extra_where = ""
        if extra_wheres:
            extra_where = "AND " + " AND ".join(extra_wheres)

        result = session.execute(
            text(f"""
                SELECT
                    COALESCE(SUM(ar.amount), 0) AS expected,
                    COALESCE(SUM(ar.paid_amount), 0) AS collected,
                    COUNT(ar.id) AS ar_count
                FROM core_accounts_receivable ar
                {extra_joins}
                WHERE ar.condominium_id = :condo_id
                  AND ar.status != 'cancelled'
                  AND ar.deleted_at IS NULL
                  AND {origin_clause}
                  {extra_where}
            """),
            params,
        ).fetchone()

        return {
            "expected": float(result.expected or 0),
            "collected": float(result.collected or 0),
            "count": int(result.ar_count or 0),
        }

    def _query_booking_stats(
        self,
        session,
        condominium_id: int,
        building_id: Optional[int] = None,
        unit_id: Optional[int] = None,
    ) -> dict:
        """Query booking counts and deposit custody totals."""
        extra_wheres = []
        params = {"condo_id": condominium_id}

        if unit_id is not None:
            extra_wheres.append("b.unit_id = :unit_id")
            params["unit_id"] = unit_id
        elif building_id is not None:
            extra_wheres.append("b.building_id = :building_id")
            params["building_id"] = building_id

        extra_where = ""
        if extra_wheres:
            extra_where = "AND " + " AND ".join(extra_wheres)

        result = session.execute(
            text(f"""
                SELECT
                    COUNT(*) AS total_bookings,
                    SUM(CASE WHEN b.status = 'confirmed' THEN 1 ELSE 0 END) AS confirmed,
                    SUM(CASE WHEN b.status = 'completed' THEN 1 ELSE 0 END) AS completed,
                    COALESCE(SUM(CASE
                        WHEN b.deposit_status IN ('pending', 'paid')
                        THEN b.security_deposit_amount
                        ELSE 0
                    END), 0) AS deposits_in_custody
                FROM core_amenity_bookings b
                WHERE b.condominium_id = :condo_id
                  AND b.deleted_at IS NULL
                  {extra_where}
            """),
            params,
        ).fetchone()

        return {
            "total_bookings": int(result.total_bookings or 0),
            "confirmed": int(result.confirmed or 0),
            "completed": int(result.completed or 0),
            "deposits_in_custody": float(result.deposits_in_custody or 0),
        }
