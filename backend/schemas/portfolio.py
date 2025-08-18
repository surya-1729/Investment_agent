"""
Portfolio schemas for API validation
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class PortfolioBase(BaseModel):
    name: str
    description: Optional[str] = None
    auto_rebalance: bool = False
    rebalance_threshold: float = 5.0


class PortfolioCreate(PortfolioBase):
    pass


class PortfolioUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    auto_rebalance: Optional[bool] = None
    rebalance_threshold: Optional[float] = None


class PortfolioResponse(PortfolioBase):
    id: int
    user_id: int
    total_value: float
    cash_balance: float
    invested_amount: float
    total_return: float
    total_return_percentage: float
    daily_return: float
    beta: float
    sharpe_ratio: float
    max_drawdown: float
    volatility: float
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_rebalanced: Optional[datetime] = None
    
    class Config:
        from_attributes = True