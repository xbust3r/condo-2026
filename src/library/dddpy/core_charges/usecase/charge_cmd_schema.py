"""
Charge command schemas — Pydantic models for API request bodies.
"""
from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import date


VALID_SCOPES = {"unit", "building", "condominium"}
VALID_DISTRIBUTION_MODES = {
    "fixed_unit_amount",
    "prorated_by_building_coefficient",
    "prorated_by_condominium_coefficient",
}


class CreateChargeSchema(BaseModel):
    condominium_id: int = Field(..., description="Condominium ID")
    charge_type_id: int = Field(..., description="Charge type FK")
    scope: str = Field("unit", description="Scope: unit | building | condominium")
    unit_id: Optional[int] = Field(None, description="Unit ID (required when scope=unit)")
    building_id: Optional[int] = Field(None, description="Building ID (required when scope=building)")
    distribution_mode: str = Field("fixed_unit_amount",
                                   description="fixed_unit_amount | prorated_by_building_coefficient | prorated_by_condominium_coefficient")
    description: Optional[str] = Field(None, description="Charge description")
    amount: float = Field(..., gt=0, description="Charge amount (must be > 0)")
    currency: str = Field("PEN", max_length=3, description="Currency code")
    is_recurrent: bool = Field(False, description="Whether this charge recurs monthly")
    period_pattern: Optional[str] = Field(
        None,
        max_length=7,
        pattern=r"^\d{4}-\d{2}$",
        description="Period pattern YYYY-MM (required if is_recurrent=True)",
    )
    start_date: date = Field(..., description="Charge start date")
    end_date: Optional[date] = Field(None, description="Charge end date (null = indefinite)")
    status: str = Field("active", description="Status: active/inactive/expired")

    @model_validator(mode="after")
    def validate_scope_consistency(self):
        """Blind scope rules."""
        if self.scope not in VALID_SCOPES:
            raise ValueError(f"scope must be one of: {', '.join(sorted(VALID_SCOPES))}")
        if self.distribution_mode not in VALID_DISTRIBUTION_MODES:
            raise ValueError(f"distribution_mode must be one of: {', '.join(sorted(VALID_DISTRIBUTION_MODES))}")

        # No ambiguity: scope dictates which FK is required
        if self.scope == "unit" and self.unit_id is None:
            raise ValueError("unit_id is required when scope=unit")
        if self.scope == "unit" and self.building_id is not None:
            raise ValueError("building_id must be null when scope=unit")

        if self.scope == "building" and self.building_id is None:
            raise ValueError("building_id is required when scope=building")
        if self.scope == "building" and self.unit_id is not None:
            raise ValueError("unit_id must be null when scope=building")

        if self.scope == "condominium":
            if self.unit_id is not None:
                raise ValueError("unit_id must be null when scope=condominium")
            if self.building_id is not None:
                raise ValueError("building_id must be null when scope=condominium")

        return self


class UpdateChargeSchema(BaseModel):
    description: Optional[str] = Field(None)
    amount: Optional[float] = Field(None, gt=0)
    scope: Optional[str] = Field(None, description="Scope: unit | building | condominium")
    unit_id: Optional[int] = Field(None, description="Unit ID (set to override; clear_unit_id=True to null)")
    building_id: Optional[int] = Field(None, description="Building ID (set to override; clear_building_id=True to null)")
    distribution_mode: Optional[str] = Field(None)
    clear_unit_id: bool = Field(False, description="Explicitly set unit_id to null")
    clear_building_id: bool = Field(False, description="Explicitly set building_id to null")
    is_recurrent: Optional[bool] = Field(None)
    period_pattern: Optional[str] = Field(None, max_length=7, pattern=r"^\d{4}-\d{2}$")
    start_date: Optional[date] = Field(None)
    end_date: Optional[date] = Field(None)
    status: Optional[str] = Field(None, description="Status: active/inactive/expired")

    @model_validator(mode="after")
    def validate_scope_consistency(self):
        """Validate scope consistency. When scope is provided, check it doesn't conflict
        with unit_id/building_id also provided in the same request."""
        if self.scope is not None and self.scope not in VALID_SCOPES:
            raise ValueError(f"scope must be one of: {', '.join(sorted(VALID_SCOPES))}")
        if self.distribution_mode is not None and self.distribution_mode not in VALID_DISTRIBUTION_MODES:
            raise ValueError(
                f"distribution_mode must be one of: {', '.join(sorted(VALID_DISTRIBUTION_MODES))}"
            )

        # If scope is being set in this request, validate FK consistency
        if self.scope is not None:
            if self.scope == "unit":
                if self.clear_unit_id:
                    raise ValueError("cannot clear unit_id when scope=unit")
                if self.clear_building_id is False and self.building_id is not None:
                    raise ValueError("building_id must be null when scope=unit. Set clear_building_id=true or omit building_id.")
            if self.scope == "building":
                if self.clear_building_id:
                    raise ValueError("cannot clear building_id when scope=building")
                if self.clear_unit_id is False and self.unit_id is not None:
                    raise ValueError("unit_id must be null when scope=building. Set clear_unit_id=true or omit unit_id.")
            if self.scope == "condominium":
                if not self.clear_unit_id and self.unit_id is not None:
                    raise ValueError("unit_id must be null when scope=condominium. Set clear_unit_id=true or omit unit_id.")
                if not self.clear_building_id and self.building_id is not None:
                    raise ValueError("building_id must be null when scope=condominium. Set clear_building_id=true or omit building_id.")

        return self
