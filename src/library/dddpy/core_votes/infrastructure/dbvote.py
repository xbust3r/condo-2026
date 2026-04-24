"""
SQLAlchemy models for core_votes, core_vote_options, core_vote_records.
"""
from sqlalchemy import Column, BigInteger, String, Text, DateTime, Boolean, Integer, ForeignKey, UniqueConstraint
from library.dddpy.shared.mysql.base import Base


class DBVote(Base):
    __tablename__ = 'core_votes'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True)
    condominium_id = Column(BigInteger, nullable=False, index=True)
    meeting_id = Column(BigInteger, nullable=True)
    title = Column(String(200), nullable=False)
    description = Column(Text(), nullable=True)
    voting_starts_at = Column(DateTime(), nullable=False)
    voting_ends_at = Column(DateTime(), nullable=False)
    status = Column(String(20), nullable=False, server_default='draft')
    vote_type = Column(String(20), nullable=False, server_default='open')
    quorum_required = Column(Boolean(), nullable=False, server_default='0')
    quorum_percentage = Column(Integer(), nullable=False, server_default='51')
    approval_threshold = Column(Integer(), nullable=False, server_default='51')
    total_eligible_voters = Column(Integer(), nullable=False, server_default='0')
    total_votes_cast = Column(Integer(), nullable=False, server_default='0')
    total_yes_votes = Column(Integer(), nullable=False, server_default='0')
    total_no_votes = Column(Integer(), nullable=False, server_default='0')
    total_abstain_votes = Column(Integer(), nullable=False, server_default='0')
    result_proclaimed_at = Column(DateTime(), nullable=True)
    created_by_user_id = Column(BigInteger, nullable=False, index=True)
    created_at = Column(DateTime(), nullable=False, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime(), nullable=True)
    deleted_at = Column(DateTime(), nullable=True)

    __table_args__ = (
        # Index on (condominium_id, status) — covered by individual column indexes above
        # Index on voting_ends_at covered by column index above
    )


class DBVoteOption(Base):
    __tablename__ = 'core_vote_options'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    vote_id = Column(BigInteger, nullable=False, index=True)
    option_text = Column(String(100), nullable=False)
    option_key = Column(String(20), nullable=False)
    vote_count = Column(Integer(), nullable=False, server_default='0')

    __table_args__ = (
        UniqueConstraint('vote_id', 'option_key', name='uk_vote_option'),
    )


class DBVoteRecord(Base):
    __tablename__ = 'core_vote_records'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    vote_id = Column(BigInteger, nullable=False, index=True)
    user_id = Column(BigInteger, nullable=False, index=True)
    option_key = Column(String(20), nullable=False)
    voted_at = Column(DateTime(), nullable=False, server_default='CURRENT_TIMESTAMP')

    __table_args__ = (
        UniqueConstraint('vote_id', 'user_id', name='uk_vote_user'),
    )
