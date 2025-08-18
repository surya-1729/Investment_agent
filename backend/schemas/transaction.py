"""
Transaction schemas for API validation
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TransactionBase(BaseModel):
    transaction_type: str  # buy, sell, dividend, deposit, withdrawal
    symbol: str
    quantity: float
    price: float
    fees: float = 0.0
    order_type: str = "market"
    notes: Optional[str] = None


class TransactionCreate(TransactionBase):
    portfolio_id: int
    asset_id: Optional[int] = None


class TransactionResponse(TransactionBase):
    id: int
    user_id: int
    portfolio_id: int
    asset_id: Optional[int] = None
    total_amount: float
    net_amount: float
    status: str
    strategy_id: Optional[int] = None
    strategy_execution_id: Optional[int] = None
    external_order_id: Optional[str] = None
    created_at: datetime
    executed_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True