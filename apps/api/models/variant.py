from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class VariantBase(BaseModel):
    """Base variant model with common fields"""
    card_id: UUID
    jp: str
    confidence: str

class VariantCreate(VariantBase):
    pass

class VariantUpdate(BaseModel):
    """Model for updating a variant - all fields optional for partial updates"""
    card_id: Optional[UUID] = None
    jp: Optional[str] = None
    confidence: Optional[str] = None

class VariantResponse(VariantBase):
    id: UUID
    created_at: datetime
    class Config:
        from_attributes = True

Variant = VariantResponse