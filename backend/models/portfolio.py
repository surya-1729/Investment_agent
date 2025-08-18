"""
Portfolio model for managing user investment portfolios
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.core.database import Base


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Portfolio details
    name = Column(String, nullable=False)
    description = Column(String)
    
    # Financial metrics
    total_value = Column(Float, default=0.0)
    cash_balance = Column(Float, default=0.0)
    invested_amount = Column(Float, default=0.0)
    
    # Performance metrics
    total_return = Column(Float, default=0.0)
    total_return_percentage = Column(Float, default=0.0)
    daily_return = Column(Float, default=0.0)
    
    # Risk metrics
    beta = Column(Float, default=1.0)
    sharpe_ratio = Column(Float, default=0.0)
    max_drawdown = Column(Float, default=0.0)
    volatility = Column(Float, default=0.0)
    
    # Settings
    is_active = Column(Boolean, default=True)
    auto_rebalance = Column(Boolean, default=False)
    rebalance_threshold = Column(Float, default=5.0)  # Percentage
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_rebalanced = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User", back_populates="portfolios")
    holdings = relationship("Asset", back_populates="portfolio")
    transactions = relationship("Transaction", back_populates="portfolio")