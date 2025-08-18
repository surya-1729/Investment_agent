"""
Asset model for tracking individual holdings in portfolios
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.core.database import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)
    
    # Asset identification
    symbol = Column(String, nullable=False, index=True)
    name = Column(String)
    asset_type = Column(String, nullable=False)  # stock, crypto, bond, etf, etc.
    exchange = Column(String)
    
    # Position details
    quantity = Column(Float, default=0.0)
    average_cost = Column(Float, default=0.0)
    current_price = Column(Float, default=0.0)
    
    # Calculated values
    market_value = Column(Float, default=0.0)
    unrealized_gain_loss = Column(Float, default=0.0)
    unrealized_gain_loss_percentage = Column(Float, default=0.0)
    
    # Portfolio allocation
    target_allocation = Column(Float, default=0.0)  # Target percentage of portfolio
    current_allocation = Column(Float, default=0.0)  # Current percentage of portfolio
    
    # Asset metadata
    sector = Column(String)
    industry = Column(String)
    country = Column(String)
    currency = Column(String, default="USD")
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_price_update = Column(DateTime(timezone=True))
    
    # Relationships
    portfolio = relationship("Portfolio", back_populates="holdings")
    transactions = relationship("Transaction", back_populates="asset")