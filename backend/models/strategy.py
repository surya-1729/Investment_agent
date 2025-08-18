"""
Strategy models for investment strategies and their executions
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.core.database import Base


class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Strategy details
    name = Column(String, nullable=False)
    description = Column(Text)
    strategy_type = Column(String, nullable=False)  # technical, fundamental, momentum, mean_reversion, etc.
    
    # Strategy parameters (stored as JSON)
    parameters = Column(JSON, default={})
    
    # Risk management
    max_position_size = Column(Float, default=10.0)  # Percentage of portfolio
    stop_loss_percentage = Column(Float, default=5.0)
    take_profit_percentage = Column(Float, default=15.0)
    
    # Performance tracking
    total_trades = Column(Integer, default=0)
    winning_trades = Column(Integer, default=0)
    losing_trades = Column(Integer, default=0)
    win_rate = Column(Float, default=0.0)
    
    # Financial performance
    total_return = Column(Float, default=0.0)
    total_return_percentage = Column(Float, default=0.0)
    sharpe_ratio = Column(Float, default=0.0)
    max_drawdown = Column(Float, default=0.0)
    
    # Status and settings
    is_active = Column(Boolean, default=True)
    is_paper_trading = Column(Boolean, default=True)
    auto_execute = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_executed = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User", back_populates="strategies")
    executions = relationship("StrategyExecution", back_populates="strategy")
    transactions = relationship("Transaction", back_populates="strategy")


class StrategyExecution(Base):
    __tablename__ = "strategy_executions"

    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"), nullable=False)
    
    # Execution details
    execution_type = Column(String, nullable=False)  # backtest, paper_trade, live_trade
    status = Column(String, default="pending")  # pending, running, completed, failed, cancelled
    
    # Time period
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    
    # Performance metrics
    initial_capital = Column(Float, default=10000.0)
    final_capital = Column(Float, default=0.0)
    total_return = Column(Float, default=0.0)
    total_return_percentage = Column(Float, default=0.0)
    
    # Trade statistics
    total_trades = Column(Integer, default=0)
    winning_trades = Column(Integer, default=0)
    losing_trades = Column(Integer, default=0)
    win_rate = Column(Float, default=0.0)
    
    # Risk metrics
    sharpe_ratio = Column(Float, default=0.0)
    max_drawdown = Column(Float, default=0.0)
    volatility = Column(Float, default=0.0)
    
    # Execution logs and results
    execution_log = Column(Text)
    results = Column(JSON, default={})
    error_message = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    strategy = relationship("Strategy", back_populates="executions")
    transactions = relationship("Transaction", back_populates="strategy_execution")