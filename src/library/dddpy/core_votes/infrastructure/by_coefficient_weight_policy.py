"""
ByCoefficientWeightPolicy — weight = unit's coefficient from core_units.
"""
from decimal import Decimal

from library.dddpy.core_votes.domain.vote_weight_policy import VoteWeightPolicy
from library.dddpy.core_votes.domain.vote_entity import VoteEntity
from library.dddpy.core_unit_ownerships.infrastructure.dbunit_ownership import DBUnitOwnership
from library.dddpy.core_units.infrastructure.dbunits import DBUnits
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("ByCoefficientWeightPolicy")


class ByCoefficientWeightPolicy(VoteWeightPolicy):
    """BY_COEFFICIENT: weight = coefficient of the unit."""

    def calculate_weight(
        self,
        unit_ownership_id: int,
        vote: VoteEntity,
    ) -> Decimal:
        with session_scope() as session:
            own = (
                session.query(DBUnitOwnership)
                .filter(DBUnitOwnership.id == unit_ownership_id)
                .first()
            )
            if own is None:
                return Decimal("0")

            unit = (
                session.query(DBUnits)
                .filter(DBUnits.id == own.unit_id)
                .first()
            )
            if unit is None:
                return Decimal("0")

            return Decimal(str(unit.coefficient)) if unit.coefficient else Decimal("1.0")
