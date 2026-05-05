"""
SQLAlchemy models for voter_eligibility_log and voter_eligibility_reason_codes.
"""
from sqlalchemy import (
    Column, BigInteger, String, Text, Boolean,
    DateTime, DECIMAL, JSON, ForeignKey, CheckConstraint, Index,
    func,
)
from library.dddpy.shared.mysql.base import Base


class DBVoterEligibilityReasonCode(Base):
    """Normalized catalog of eligibility reason codes."""

    __tablename__ = "voter_eligibility_reason_codes"

    code = Column(String(50), primary_key=True)
    description = Column(String(255), nullable=False)
    category = Column(
        String(20),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint(
            "category IN ('ELIGIBLE','REJECTED')",
            name="ck_reason_code_category",
        ),
    )


class DBVoterEligibilityLog(Base):
    """Forensic audit trail for every eligibility evaluation."""

    __tablename__ = "voter_eligibility_log"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    vote_id = Column(BigInteger, nullable=False, index=True)
    unit_ownership_id = Column(BigInteger, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    eligible = Column(Boolean, nullable=False)
    reason_code = Column(
        String(50),
        ForeignKey("voter_eligibility_reason_codes.code", name="fk_eligibility_log_reason"),
        nullable=False,
    )
    debt_months_observed = Column(DECIMAL(5, 2), nullable=True)
    ownership_observed = Column(JSON, nullable=True)
    coefficient_observed = Column(DECIMAL(7, 4), nullable=True)
    rules_snapshot_hash = Column(String(64), nullable=False)
    evaluated_at = Column(DateTime, nullable=False, server_default=func.now())

    __table_args__ = (
        Index("idx_eligibility_vote_unit", "vote_id", "unit_ownership_id"),
        Index("idx_eligibility_rules_hash", "rules_snapshot_hash"),
    )
