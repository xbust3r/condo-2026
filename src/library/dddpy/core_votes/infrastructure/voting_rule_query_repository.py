"""
VotingRuleQueryRepository — reads voting rule templates from DB.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from library.dddpy.core_votes.domain.voting_rule_entity import VotingRuleEntity
from library.dddpy.core_votes.infrastructure.dbvotingrule import DBVotingRule
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("VotingRuleQueryRepository")


class VotingRuleQueryRepository:
    """
    Read-only repository for core_voting_rules.

    Used at vote creation time to build the rules_snapshot dict
    from the matching active rule template.
    """

    def find_active(
        self,
        condominium_id: int,
        building_id: Optional[int] = None,
        scope_type: str = "condominium",
    ) -> Optional[VotingRuleEntity]:
        """
        Find the active voting rule for a given condominium + scope.

        Priority:
        1. Building-specific rule (building_id matches)
        2. Condominium-wide rule (building_id IS NULL)
        """
        with session_scope() as session:
            # Try building-specific first
            rule = None
            if building_id is not None:
                rule = (
                    session.query(DBVotingRule)
                    .filter(DBVotingRule.condominium_id == condominium_id)
                    .filter(DBVotingRule.building_id == building_id)
                    .filter(DBVotingRule.scope_type == scope_type)
                    .filter(DBVotingRule.is_active == True)
                    .filter(DBVotingRule.deleted_at.is_(None))
                    .first()
                )

            # Fallback to condominium-wide
            if rule is None:
                rule = (
                    session.query(DBVotingRule)
                    .filter(DBVotingRule.condominium_id == condominium_id)
                    .filter(DBVotingRule.building_id.is_(None))
                    .filter(DBVotingRule.scope_type == scope_type)
                    .filter(DBVotingRule.is_active == True)
                    .filter(DBVotingRule.deleted_at.is_(None))
                    .first()
                )

            if rule is None:
                return None

            return self._to_entity(rule)

    def get_by_id(self, rule_id: int) -> Optional[VotingRuleEntity]:
        with session_scope() as session:
            rule = (
                session.query(DBVotingRule)
                .filter(DBVotingRule.id == rule_id)
                .filter(DBVotingRule.deleted_at.is_(None))
                .first()
            )
            if rule is None:
                return None
            return self._to_entity(rule)

    @staticmethod
    def _to_entity(db: DBVotingRule) -> VotingRuleEntity:
        return VotingRuleEntity(
            id=db.id,
            uuid=db.uuid,
            condominium_id=db.condominium_id,
            name=db.name,
            owners_only=db.owners_only,
            max_debt_months=db.max_debt_months,
            allow_tenants=db.allow_tenants,
            vote_calculation_type=db.vote_calculation_type,
            include_parking=db.include_parking,
            include_annexes=db.include_annexes,
            scope_type=db.scope_type,
            building_id=db.building_id,
            is_active=db.is_active,
            created_by_user_id=db.created_by_user_id,
            created_at=db.created_at,
            updated_at=db.updated_at,
            deleted_at=db.deleted_at,
        )

    @staticmethod
    def to_rules_snapshot_dict(rule: VotingRuleEntity) -> dict:
        """
        Convert a VotingRuleEntity into the rules_snapshot format
        that VotingRulesSnapshot.from_dict() accepts.
        """
        from datetime import timezone as tz

        return {
            "vote_calculation_type": rule.vote_calculation_type,
            "scope": rule.scope_type,
            "building_id": rule.building_id,
            "allow_only_owners": rule.owners_only,
            "allow_tenants": rule.allow_tenants,
            "max_debt_months": str(rule.max_debt_months),
            "include_parking_storage": rule.include_parking or rule.include_annexes,
            "snapshot_at": datetime.now(tz.utc).isoformat(),
            "snapshot_version": 1,
        }
