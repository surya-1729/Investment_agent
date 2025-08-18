"""
Portfolio management API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.core.database import get_db
from backend.schemas.portfolio import PortfolioCreate, PortfolioResponse, PortfolioUpdate
from backend.api.endpoints.auth import get_current_user
from backend.models.portfolio import Portfolio

router = APIRouter()


@router.post("/", response_model=PortfolioResponse)
async def create_portfolio(
    portfolio_create: PortfolioCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new portfolio"""
    db_portfolio = Portfolio(
        user_id=current_user.id,
        name=portfolio_create.name,
        description=portfolio_create.description,
        auto_rebalance=portfolio_create.auto_rebalance,
        rebalance_threshold=portfolio_create.rebalance_threshold,
        cash_balance=current_user.initial_balance
    )
    
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio


@router.get("/", response_model=List[PortfolioResponse])
async def get_user_portfolios(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all portfolios for the current user"""
    portfolios = db.query(Portfolio).filter(
        Portfolio.user_id == current_user.id,
        Portfolio.is_active == True
    ).all()
    return portfolios


@router.get("/{portfolio_id}", response_model=PortfolioResponse)
async def get_portfolio(
    portfolio_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific portfolio"""
    portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id,
        Portfolio.user_id == current_user.id
    ).first()
    
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    return portfolio


@router.put("/{portfolio_id}", response_model=PortfolioResponse)
async def update_portfolio(
    portfolio_id: int,
    portfolio_update: PortfolioUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a portfolio"""
    portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id,
        Portfolio.user_id == current_user.id
    ).first()
    
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    # Update portfolio fields
    update_data = portfolio_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(portfolio, field):
            setattr(portfolio, field, value)
    
    db.commit()
    db.refresh(portfolio)
    return portfolio


@router.delete("/{portfolio_id}")
async def delete_portfolio(
    portfolio_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a portfolio (soft delete)"""
    portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id,
        Portfolio.user_id == current_user.id
    ).first()
    
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    portfolio.is_active = False
    db.commit()
    
    return {"message": "Portfolio deleted successfully"}