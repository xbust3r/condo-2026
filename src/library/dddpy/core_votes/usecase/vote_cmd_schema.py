"""
Vote command schemas — Pydantic input models.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field


class CreateVoteSchema(BaseModel):
    condominium_id: int = Field(..., description="Condominium ID")
    title: str = Field(..., min_length=3, max_length=200, description="Vote title")
    description: Optional[str] = Field(None, description="Detailed description")
    voting_starts_at: datetime = Field(..., description="Voting start datetime")
    voting_ends_at: datetime = Field(..., description="Voting end datetime")
    vote_type: str = Field('open', description="Vote type: open or secret")
    quorum_required: bool = Field(False, description="Whether quorum is required")
    quorum_percentage: int = Field(51, ge=1, le=100, description="Quorum percentage required")
    approval_threshold: int = Field(51, ge=1, le=100, description="Approval threshold percentage")
    options: List[dict] = Field(
        ...,
        description="List of options as [{\"option_text\": \"Sí\", \"option_key\": \"yes\"}, ...]",
    )
    meeting_id: Optional[int] = Field(None, description="Associated meeting ID (optional)")
    rules_snapshot: Optional[Dict[str, Any]] = Field(
        None,
        description=(
            "Frozen VotingRulesSnapshot dict. If omitted, defaults to "
            "BY_UNIT, CONDOMINIUM scope, owners only, max_debt_months=2."
        ),
    )


class CastVoteSchema(BaseModel):
    option_key: str = Field(..., description="The option key being voted for")
    unit_ownership_id: int = Field(
        ...,
        description="Electoral identity — the unit_ownership_id that is voting",
    )


class UpdateVoteSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None)
    voting_ends_at: Optional[datetime] = Field(
        None,
        description="New end datetime — can only extend, not shorten",
    )
