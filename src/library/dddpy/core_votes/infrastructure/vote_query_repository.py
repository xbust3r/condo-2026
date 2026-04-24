"""
from typing import Optional
Vote query repository implementation — read operations with enrichment.
"""
from typing import Optional, List, Tuple
from sqlalchemy import and_, text

from library.dddpy.core_votes.domain.vote_entity import VoteEntity
from library.dddpy.core_votes.domain.vote_query_repository import VoteQueryRepository
from library.dddpy.core_votes.infrastructure.dbvote import DBVote, DBVoteOption, DBVoteRecord
from library.dddpy.core_votes.infrastructure.vote_mapper import VoteMapper
from library.dddpy.core_condominiums.infrastructure.dbcondominiums import DBCondominium
from library.dddpy.shared.mysql.session_manager import session_scope
from library.dddpy.shared.logging.logging import Logger


logger = Logger("VoteQueryRepository")


class VoteQueryRepositoryImpl(VoteQueryRepository):

    def __init__(self):
        logger.info("VoteQueryRepositoryImpl initialized")

    def _bulk_enrich(self, rows: List[DBVote]) -> List[VoteEntity]:
        """Apply user + condominium enrichment to vote rows."""
        if not rows:
            return []

        vote_ids = [r.id for r in rows]
        condo_ids = list({r.condominium_id for r in rows if r.condominium_id})
        creator_ids = list({r.created_by_user_id for r in rows if r.created_by_user_id})

        with session_scope() as session:
            # 1. Condominiums
            condo_map: dict[int, DBCondominium] = {}
            if condo_ids:
                condo_map = {
                    c.id: c
                    for c in session.query(DBCondominium)
                    .filter(DBCondominium.id.in_(condo_ids))
                    .all()
                }

            # 2. User full names via raw SQL on user_profiles
            user_name_map: dict[int, str] = {}
            all_user_ids = list(set(creator_ids))
            if all_user_ids:
                placeholders = ", ".join([f":u{i}" for i in range(len(all_user_ids))])
                sql = f"""
                    SELECT user_id, first_name, last_name
                    FROM user_profiles
                    WHERE user_id IN ({placeholders})
                """
                params = {f"u{i}": uid for i, uid in enumerate(all_user_ids)}
                result = session.execute(text(sql), params)
                for row in result:
                    uid, fname, lname = row[0], row[1], row[2]
                    user_name_map[uid] = f"{fname or ''} {lname or ''}".strip()

            # 3. Options for all votes
            options_map: dict[int, List[DBVoteOption]] = {}
            if vote_ids:
                opts = (
                    session.query(DBVoteOption)
                    .filter(DBVoteOption.vote_id.in_(vote_ids))
                    .all()
                )
                for o in opts:
                    if o.vote_id not in options_map:
                        options_map[o.vote_id] = []
                    options_map[o.vote_id].append(o)

            result_entities = []
            for row in rows:
                condo = condo_map.get(row.condominium_id)
                entity = VoteMapper.to_domain_enriched(
                    row,
                    db_options=options_map.get(row.id, []),
                    created_by_user_full_name=user_name_map.get(row.created_by_user_id),
                    condominium_name=condo.name if condo else None,
                )
                result_entities.append(entity)
            return result_entities

    def get_by_id(self, id: int) -> Optional[VoteEntity]:
        logger.debug(f"Fetching vote by id={id}")
        with session_scope() as session:
            db_vote = (
                session.query(DBVote)
                .filter(
                    DBVote.id == id,
                    DBVote.deleted_at.is_(None),
                )
                .first()
            )
            if not db_vote:
                return None
            db_options = (
                session.query(DBVoteOption)
                .filter(DBVoteOption.vote_id == id)
                .all()
            )
            enriched = self._bulk_enrich([db_vote])
            if enriched:
                enriched[0].options = [
                    VoteMapper._option_to_domain(o) for o in db_options
                ]
            return enriched[0] if enriched else None

    def get_by_uuid(self, uuid: str) -> Optional[VoteEntity]:
        logger.debug(f"Fetching vote by uuid={uuid}")
        with session_scope() as session:
            db_vote = (
                session.query(DBVote)
                .filter(
                    DBVote.uuid == uuid,
                    DBVote.deleted_at.is_(None),
                )
                .first()
            )
            if not db_vote:
                return None
            db_options = (
                session.query(DBVoteOption)
                .filter(DBVoteOption.vote_id == db_vote.id)
                .all()
            )
            enriched = self._bulk_enrich([db_vote])
            if enriched:
                enriched[0].options = [
                    VoteMapper._option_to_domain(o) for o in db_options
                ]
            return enriched[0] if enriched else None

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
        status: Optional[str] = None,
        created_by_user_id: Optional[int] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[VoteEntity], int]:
        logger.debug(f"Listing votes skip={skip} limit={limit}")
        with session_scope() as session:
            query = session.query(DBVote)

            if not include_deleted:
                query = query.filter(DBVote.deleted_at.is_(None))
            if condominium_id is not None:
                query = query.filter(DBVote.condominium_id == condominium_id)
            if status is not None:
                query = query.filter(DBVote.status == status)
            if created_by_user_id is not None:
                query = query.filter(DBVote.created_by_user_id == created_by_user_id)

            total = query.count()
            results = (
                query
                .order_by(DBVote.id.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            return self._bulk_enrich(results), total

    def list_by_condominium(
        self,
        condominium_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[VoteEntity], int]:
        logger.debug(f"Listing votes for condominium_id={condominium_id}")
        with session_scope() as session:
            query = session.query(DBVote).filter(
                DBVote.condominium_id == condominium_id
            )

            if not include_deleted:
                query = query.filter(DBVote.deleted_at.is_(None))
            if status is not None:
                query = query.filter(DBVote.status == status)

            total = query.count()
            results = (
                query
                .order_by(DBVote.id.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            return self._bulk_enrich(results), total

    def list_active(
        self,
        skip: int = 0,
        limit: int = 100,
        condominium_id: Optional[int] = None,
    ) -> Tuple[List[VoteEntity], int]:
        """List votes currently in active voting period."""
        logger.debug(f"Listing active votes skip={skip} limit={limit}")
        from datetime import datetime
        now = datetime.utcnow()
        with session_scope() as session:
            query = session.query(DBVote).filter(
                DBVote.status == "active",
                DBVote.voting_starts_at <= now,
                DBVote.voting_ends_at >= now,
            )

            if condominium_id is not None:
                query = query.filter(DBVote.condominium_id == condominium_id)

            total = query.count()
            results = (
                query
                .order_by(DBVote.id.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            return self._bulk_enrich(results), total

    def _get_by_id_any_status(self, id: int) -> Optional[VoteEntity]:
        """Re-fetch entity ignoring soft-delete filter. For use after mutations."""
        logger.debug(f"Fetching vote by id={id} (any status)")
        with session_scope() as session:
            db_vote = (
                session.query(DBVote)
                .filter(DBVote.id == id)
                .first()
            )
            if not db_vote:
                return None
            db_options = (
                session.query(DBVoteOption)
                .filter(DBVoteOption.vote_id == id)
                .all()
            )
            return VoteMapper.to_domain(db_vote, db_options=db_options)
