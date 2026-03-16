# Response schemas for consistent API responses
from pydantic import BaseModel, ConfigDict
from typing import Optional, Any, Generic, TypeVar


T = TypeVar("T")


class ResponseSchema(BaseModel, Generic[T]):
    """Standard API response wrapper"""
    model_config = ConfigDict(from_attributes=True)
    
    success: bool = True
    message: str = "Operation successful"
    data: Optional[T] = None
    errors: Optional[list] = None


class ErrorResponse(BaseModel):
    """Standard error response"""
    success: bool = False
    message: str
    errors: Optional[list] = None


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response wrapper"""
    model_config = ConfigDict(from_attributes=True)
    
    success: bool = True
    data: list[T]
    total: int
    page: int
    per_page: int
    pages: int
