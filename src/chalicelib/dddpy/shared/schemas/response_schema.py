from pydantic import BaseModel
from typing import Optional, Any


class ResponseErrorSchema(BaseModel):
    success: bool = False
    message: str


class ResponseSuccessSchema(BaseModel):
    success: bool = True
    message: str
    data: Optional[Any] = None
