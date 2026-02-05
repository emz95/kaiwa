from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class CardBase(BaseModel):
    """Base card model with common fields"""
    scenario_id: UUID
    npc: str
    intent: str
    notes: Optional[str] = None

class CardCreate(CardBase):
    """Model for creating a new card"""
    pass

class CardUpdate(BaseModel):
    """Model for updating a card - all fields optional for partial updates"""
    scenario_id: Optional[UUID] = None
    npc: Optional[str] = None
    intent: Optional[str] = None
    notes: Optional[str] = None

class CardResponse(CardBase):
    """Model for card response (includes database fields)"""
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

Card = CardResponse
