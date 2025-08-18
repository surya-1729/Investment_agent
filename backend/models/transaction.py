"""
Transaction model for recording all trading activities
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.core.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=True)
    
    # Transaction details
    transaction_type = Column(String, nullable=False)  # buy, sell, dividend, deposit, withdrawal
    symbol = Column(String, nullable=False, index=True)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    
    # Financial details
    total_amount = Column(Float, nullable=False)
    fees = Column(Float, default=0.0)
    net_amount = Column(Float, nullable=False)
    
    # Transaction metadata
    order_type = Column(String, default="market")  # market, limit, stop, stop_limit
    status = Column(String, default="pending")  # pending, executed, cancelled, failed
    
    # Strategy information
    strategy_id = Column(Integer, ForeignKey("strategies.id"), nullable=True)
    strategy_execution_id = Column(Integer, ForeignKey("strategy_executions.id"), nullable=True)
    
    # Additional information
    notes = Column(Text)
    external_order_id = Column(String)  # For broker integration
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    executed_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="transactions")
    portfolio = relationship("Portfolio", back_populates="transactions")
    asset = relationship("Asset", back_populates="transactions")
    strategy = relationship("Strategy", back_populates="transactions")
    strategy_execution = relationship("StrategyExecution", back_populates="transactions")