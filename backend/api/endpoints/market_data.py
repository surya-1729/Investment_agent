"""
Market data API endpoints
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
import pandas as pd

from backend.services.market_data import MarketDataService

router = APIRouter()
market_service = MarketDataService()


@router.get("/price/{symbol}")
async def get_current_price(symbol: str):
    """Get current price for a symbol"""
    price = await market_service.get_current_price(symbol.upper())
    if price is None:
        raise HTTPException(status_code=404, detail=f"Price not found for symbol {symbol}")
    
    return {
        "symbol": symbol.upper(),
        "price": price,
        "timestamp": pd.Timestamp.now().isoformat()
    }


@router.post("/prices")
async def get_multiple_prices(symbols: List[str]):
    """Get current prices for multiple symbols"""
    symbols_upper = [s.upper() for s in symbols]
    prices = await market_service.get_multiple_prices(symbols_upper)
    
    return {
        "prices": prices,
        "timestamp": pd.Timestamp.now().isoformat()
    }


@router.get("/historical/{symbol}")
async def get_historical_data(
    symbol: str,
    period: str = Query("1y", description="Period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)"),
    interval: str = Query("1d", description="Interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)")
):
    """Get historical data for a symbol"""
    data = await market_service.get_historical_data(symbol.upper(), period, interval)
    if data is None:
        raise HTTPException(status_code=404, detail=f"Historical data not found for symbol {symbol}")
    
    # Convert DataFrame to dict for JSON response
    data_dict = data.reset_index().to_dict('records')
    
    return {
        "symbol": symbol.upper(),
        "period": period,
        "interval": interval,
        "data": data_dict
    }


@router.get("/info/{symbol}")
async def get_stock_info(symbol: str):
    """Get comprehensive stock information"""
    info = await market_service.get_stock_info(symbol.upper())
    if info is None:
        raise HTTPException(status_code=404, detail=f"Stock info not found for symbol {symbol}")
    
    return info


@router.get("/search")
async def search_symbols(q: str = Query(..., description="Search query for stock symbols")):
    """Search for stock symbols"""
    results = await market_service.search_symbols(q)
    return {"query": q, "results": results}


@router.get("/indices")
async def get_market_indices():
    """Get current prices for major market indices"""
    indices = await market_service.get_market_indices()
    return {
        "indices": indices,
        "timestamp": pd.Timestamp.now().isoformat()
    }


@router.get("/crypto")
async def get_crypto_prices(symbols: List[str] = Query(..., description="Cryptocurrency symbols")):
    """Get cryptocurrency prices"""
    prices = await market_service.get_crypto_prices(symbols)
    return {
        "crypto_prices": prices,
        "timestamp": pd.Timestamp.now().isoformat()
    }


@router.get("/technical/{symbol}")
async def get_technical_indicators(
    symbol: str,
    period: str = Query("6mo", description="Period for technical analysis"),
    interval: str = Query("1d", description="Data interval")
):
    """Get technical indicators for a symbol"""
    # Get historical data
    data = await market_service.get_historical_data(symbol.upper(), period, interval)
    if data is None:
        raise HTTPException(status_code=404, detail=f"Data not found for symbol {symbol}")
    
    # Calculate technical indicators
    data_with_indicators = market_service.calculate_technical_indicators(data)
    
    # Get latest values
    latest = data_with_indicators.iloc[-1]
    
    return {
        "symbol": symbol.upper(),
        "current_price": latest['Close'],
        "indicators": {
            "sma_20": latest.get('SMA_20'),
            "sma_50": latest.get('SMA_50'),
            "sma_200": latest.get('SMA_200'),
            "rsi": latest.get('RSI'),
            "macd": latest.get('MACD'),
            "macd_signal": latest.get('MACD_Signal'),
            "bb_upper": latest.get('BB_Upper'),
            "bb_middle": latest.get('BB_Middle'),
            "bb_lower": latest.get('BB_Lower')
        },
        "timestamp": pd.Timestamp.now().isoformat()
    }