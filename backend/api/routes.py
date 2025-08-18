"""
Main API router that includes all endpoint routers
"""

from fastapi import APIRouter

from backend.api.endpoints import auth, market_data, portfolio, users, strategies

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(market_data.router, prefix="/market", tags=["market-data"])
api_router.include_router(portfolio.router, prefix="/portfolios", tags=["portfolios"])
api_router.include_router(strategies.router, prefix="/strategies", tags=["strategies"])