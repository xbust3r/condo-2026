"""
Document command schemas.
"""
from typing import Optional

from pydantic import BaseModel, Field


class CreateDocumentSchema(BaseModel):
    condominium_id: int = Field(..., description="Condominium ID")
    uploader_user_id: int = Field(..., description="Uploader user ID")
    title: str = Field(..., min_length=3, max_length=200, description="Document title")
    description: Optional[str] = Field(None, description="Optional description")
    file_url: str = Field(..., min_length=5, description="URL/path to the stored file")
    file_size_bytes: Optional[int] = Field(None, description="File size in bytes")
    mime_type: Optional[str] = Field(None, description="MIME type (e.g. application/pdf)")
    category: str = Field('other', description="Category: bylaws, minutes, regulation, contract, invoice, other")


class UpdateDocumentSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None)
    category: Optional[str] = Field(None)
