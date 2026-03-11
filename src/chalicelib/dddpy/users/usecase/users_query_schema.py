from pydantic import BaseModel
from typing import Optional


class UserQuerySchema(BaseModel):
    id: Optional[int] = None
    email: Optional[str] = None
    status: Optional[str] = None
