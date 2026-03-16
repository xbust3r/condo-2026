from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class UsersQuerySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    first_name: str
    last_name: str
    email: str
    doc_identity: Optional[str]
    phone: Optional[str]
    status: int
    created_at: datetime
    updated_at: datetime

class UsersListQuerySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    first_name: str
    last_name: str
    email: str
    status: int
