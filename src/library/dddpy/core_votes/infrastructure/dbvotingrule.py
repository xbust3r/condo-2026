"""
DBVotingRule — SQLAlchemy model for core_voting_rules table.
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, DateTime, ForeignKey
from library.dddpy.shared.mysql.base import Base


class DBVotingRule(Base):
    __tablename__ = "core_voting_rules"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True)
    condominium_id = Column(
        BigInteger,
        ForeignKey("core_condominiums.id", name="fk_voting_rule_condominium"),
        nullable=False,
        index=True,
    )
    building_id = Column(
        BigInteger,
        nullable=True,
        comment="NULL = applies to whole condominium",
    )
    name = Column(String(100), nullable=False)

    # Eligibility
    owners_only = Column(Boolean, nullable=False, server_default="1")
    max_debt_months = Column(Integer, nullable=False, server_default="2")
    allow_tenants = Column(Boolean, nullable=False, server_default="0")

    # Vote calculation
    vote_calculation_type = Column(String(20), nullable=False, server_default="by_unit")
    include_parking = Column(Boolean, nullable=False, server_default="0")
    include_annexes = Column(Boolean, nullable=False, server_default="0")

    # Scope
    scope_type = Column(String(20), nullable=False, server_default="condominium")

    # Lifecycle
    is_active = Column(Boolean, nullable=False, server_default="1")
    created_by_user_id = Column(
        BigInteger,
        ForeignKey("users.id", name="fk_voting_rule_created_by"),
        nullable=False,
    )
    created_at = Column(DateTime, nullable=False, server_default="CURRENT_TIMESTAMP")
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
