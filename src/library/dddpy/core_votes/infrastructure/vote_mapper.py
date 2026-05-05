"""
Vote mapper — maps between DB models and domain entities.
"""
from typing import List, Optional

from library.dddpy.core_votes.infrastructure.dbvote import DBVote, DBVoteOption, DBVoteRecord
from library.dddpy.core_votes.domain.vote_entity import VoteEntity, VoteOptionEntity
from library.dddpy.core_votes.domain.vote_rules_snapshot import VotingRulesSnapshot


class VoteMapper:

    @staticmethod
    def _option_to_domain(db_option: DBVoteOption) -> VoteOptionEntity:
        return VoteOptionEntity(
            id=db_option.id,
            vote_id=db_option.vote_id,
            option_text=db_option.option_text,
            option_key=db_option.option_key,
            vote_count=db_option.vote_count or 0,
        )

    @staticmethod
    def to_domain(
        db_vote: DBVote,
        db_options: List[DBVoteOption] = None,
        db_records: List[DBVoteRecord] = None,
    ) -> VoteEntity:
        options = [VoteMapper._option_to_domain(o) for o in (db_options or [])]

        # Hydrate rules_snapshot from JSON if present
        rules_snapshot = None
        if db_vote.rules_snapshot:
            try:
                rules_snapshot = VotingRulesSnapshot.from_dict(db_vote.rules_snapshot)
            except Exception:
                # Legacy data may not conform — leave as None
                pass

        return VoteEntity(
            id=db_vote.id,
            uuid=db_vote.uuid,
            condominium_id=db_vote.condominium_id,
            meeting_id=db_vote.meeting_id,
            title=db_vote.title,
            description=db_vote.description,
            voting_starts_at=db_vote.voting_starts_at,
            voting_ends_at=db_vote.voting_ends_at,
            status=db_vote.status,
            vote_type=db_vote.vote_type,
            quorum_required=db_vote.quorum_required or False,
            quorum_percentage=db_vote.quorum_percentage or 51,
            approval_threshold=db_vote.approval_threshold or 51,
            total_eligible_voters=db_vote.total_eligible_voters or 0,
            total_votes_cast=db_vote.total_votes_cast or 0,
            total_yes_votes=db_vote.total_yes_votes or 0,
            total_no_votes=db_vote.total_no_votes or 0,
            total_abstain_votes=db_vote.total_abstain_votes or 0,
            result_proclaimed_at=db_vote.result_proclaimed_at,
            created_by_user_id=db_vote.created_by_user_id,
            created_at=db_vote.created_at,
            updated_at=db_vote.updated_at,
            deleted_at=db_vote.deleted_at,
            scope_type=db_vote.scope_type,
            vote_calculation_type=db_vote.vote_calculation_type,
            building_id=db_vote.building_id,
            options=options,
            rules_snapshot=rules_snapshot,
        )

    @staticmethod
    def to_domain_enriched(
        db_vote: DBVote,
        db_options: List[DBVoteOption] = None,
        db_records: List[DBVoteRecord] = None,
        created_by_user_full_name: str = None,
        condominium_name: str = None,
    ) -> VoteEntity:
        entity = VoteMapper.to_domain(db_vote, db_options, db_records)
        entity.created_by_user_full_name = created_by_user_full_name
        entity.condominium_name = condominium_name
        return entity
