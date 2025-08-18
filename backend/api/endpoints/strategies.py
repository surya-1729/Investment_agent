"""
Investment strategy API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.core.database import get_db
from backend.schemas.strategy import StrategyCreate, StrategyResponse, StrategyUpdate
from backend.api.endpoints.auth import get_current_user
from backend.models.strategy import Strategy

router = APIRouter()


@router.post("/", response_model=StrategyResponse)
async def create_strategy(
    strategy_create: StrategyCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new investment strategy"""
    db_strategy = Strategy(
        user_id=current_user.id,
        name=strategy_create.name,
        description=strategy_create.description,
        strategy_type=strategy_create.strategy_type,
        parameters=strategy_create.parameters,
        max_position_size=strategy_create.max_position_size,
        stop_loss_percentage=strategy_create.stop_loss_percentage,
        take_profit_percentage=strategy_create.take_profit_percentage,
        auto_execute=strategy_create.auto_execute,
        is_paper_trading=True  # Always start with paper trading
    )
    
    db.add(db_strategy)
    db.commit()
    db.refresh(db_strategy)
    return db_strategy


@router.get("/", response_model=List[StrategyResponse])
async def get_user_strategies(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all strategies for the current user"""
    strategies = db.query(Strategy).filter(
        Strategy.user_id == current_user.id,
        Strategy.is_active == True
    ).all()
    return strategies


@router.get("/{strategy_id}", response_model=StrategyResponse)
async def get_strategy(
    strategy_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific strategy"""
    strategy = db.query(Strategy).filter(
        Strategy.id == strategy_id,
        Strategy.user_id == current_user.id
    ).first()
    
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    
    return strategy


@router.put("/{strategy_id}", response_model=StrategyResponse)
async def update_strategy(
    strategy_id: int,
    strategy_update: StrategyUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a strategy"""
    strategy = db.query(Strategy).filter(
        Strategy.id == strategy_id,
        Strategy.user_id == current_user.id
    ).first()
    
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    
    # Update strategy fields
    update_data = strategy_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(strategy, field):
            setattr(strategy, field, value)
    
    db.commit()
    db.refresh(strategy)
    return strategy


@router.delete("/{strategy_id}")
async def delete_strategy(
    strategy_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a strategy (soft delete)"""
    strategy = db.query(Strategy).filter(
        Strategy.id == strategy_id,
        Strategy.user_id == current_user.id
    ).first()
    
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    
    strategy.is_active = False
    db.commit()
    
    return {"message": "Strategy deleted successfully"}