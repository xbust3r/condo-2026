from typing import Optional
from pydantic import BaseModel
from typing import Optional, Any, List


class ResponseSchema(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    errors: Optional[List[str]] = None


class ResponseErrorSchema(BaseModel):
    success: bool = False
    message: str


class ResponseSuccessSchema(BaseModel):
    success: bool = True
    message: str
    data: Optional[Any] = None
