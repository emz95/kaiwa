from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class ScenarioBase(BaseModel):
    """Base scenario model with common fields"""
    slug: str
    name: str
    description: Optional[str] = None
    order_index: int = 0
    is_active: bool = True

class ScenarioCreate(ScenarioBase):
    pass

class ScenarioUpdate(BaseModel):
    """Model for updating a scenario - all fields optional for partial updates"""
    slug: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    order_index: Optional[int] = None
    is_active: Optional[bool] = None

class ScenarioResponse(ScenarioBase):
    id: UUID 
    created_at: datetime  
    class Config:
        from_attributes = True  

Scenario = ScenarioResponse
