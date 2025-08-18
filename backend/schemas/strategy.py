"""
Strategy schemas for API validation
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class StrategyBase(BaseModel):
    name: str
    description: Optional[str] = None
    strategy_type: str
    parameters: Dict[str, Any] = {}
    max_position_size: float = 10.0
    stop_loss_percentage: float = 5.0
    take_profit_percentage: float = 15.0
    auto_execute: bool = False


class StrategyCreate(StrategyBase):
    pass


class StrategyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    max_position_size: Optional[float] = None
    stop_loss_percentage: Optional[float] = None
    take_profit_percentage: Optional[float] = None
    is_active: Optional[bool] = None
    auto_execute: Optional[bool] = None


class StrategyResponse(StrategyBase):
    id: int
    user_id: int
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    total_return: float
    total_return_percentage: float
    sharpe_ratio: float
    max_drawdown: float
    is_active: bool
    is_paper_trading: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_executed: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class StrategyExecutionResponse(BaseModel):
    id: int
    strategy_id: int
    execution_type: str
    status: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    initial_capital: float
    final_capital: float
    total_return: float
    total_return_percentage: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    sharpe_ratio: float
    max_drawdown: float
    volatility: float
    execution_log: Optional[str] = None
    results: Dict[str, Any] = {}
    error_message: Optional[str] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True