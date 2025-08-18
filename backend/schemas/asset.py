"""
Asset schemas for API validation
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AssetBase(BaseModel):
    symbol: str
    name: Optional[str] = None
    asset_type: str
    exchange: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    country: Optional[str] = None
    currency: str = "USD"
    target_allocation: float = 0.0


class AssetCreate(AssetBase):
    portfolio_id: int
    quantity: float = 0.0
    average_cost: float = 0.0


class AssetUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[float] = None
    average_cost: Optional[float] = None
    current_price: Optional[float] = None
    target_allocation: Optional[float] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    country: Optional[str] = None


class AssetResponse(AssetBase):
    id: int
    portfolio_id: int
    quantity: float
    average_cost: float
    current_price: float
    market_value: float
    unrealized_gain_loss: float
    unrealized_gain_loss_percentage: float
    current_allocation: float
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_price_update: Optional[datetime] = None
    
    class Config:
        from_attributes = True