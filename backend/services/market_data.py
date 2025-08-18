"""
Market Data Service for fetching real-time and historical market data
"""

import yfinance as yf
import pandas as pd
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import asyncio
import httpx
from loguru import logger

from backend.core.config import settings


class MarketDataService:
    """Service for fetching market data from various sources"""
    
    def __init__(self):
        self.alpha_vantage_key = settings.ALPHA_VANTAGE_API_KEY
        self.alpha_vantage_base_url = "https://www.alphavantage.co/query"
    
    async def get_current_price(self, symbol: str) -> Optional[float]:
        """
        Get current price for a symbol using Yahoo Finance
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            current_price = info.get('currentPrice') or info.get('regularMarketPrice')
            return float(current_price) if current_price else None
        except Exception as e:
            logger.error(f"Error fetching current price for {symbol}: {e}")
            return None
    
    async def get_multiple_prices(self, symbols: List[str]) -> Dict[str, float]:
        """
        Get current prices for multiple symbols
        """
        prices = {}
        tasks = []
        
        for symbol in symbols:
            tasks.append(self.get_current_price(symbol))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error fetching price for {symbols[i]}: {result}")
                prices[symbols[i]] = None
            else:
                prices[symbols[i]] = result
        
        return prices
    
    async def get_historical_data(
        self, 
        symbol: str, 
        period: str = "1y",
        interval: str = "1d"
    ) -> Optional[pd.DataFrame]:
        """
        Get historical data for a symbol
        
        Args:
            symbol: Stock symbol
            period: Period to fetch (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
        """
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period, interval=interval)
            return hist if not hist.empty else None
        except Exception as e:
            logger.error(f"Error fetching historical data for {symbol}: {e}")
            return None
    
    async def get_stock_info(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Get comprehensive stock information
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                'symbol': symbol,
                'name': info.get('longName', ''),
                'sector': info.get('sector', ''),
                'industry': info.get('industry', ''),
                'country': info.get('country', ''),
                'currency': info.get('currency', 'USD'),
                'exchange': info.get('exchange', ''),
                'market_cap': info.get('marketCap'),
                'pe_ratio': info.get('trailingPE'),
                'dividend_yield': info.get('dividendYield'),
                'beta': info.get('beta'),
                'fifty_two_week_high': info.get('fiftyTwoWeekHigh'),
                'fifty_two_week_low': info.get('fiftyTwoWeekLow'),
                'volume': info.get('volume'),
                'avg_volume': info.get('averageVolume'),
                'current_price': info.get('currentPrice') or info.get('regularMarketPrice')
            }
        except Exception as e:
            logger.error(f"Error fetching stock info for {symbol}: {e}")
            return None
    
    async def search_symbols(self, query: str) -> List[Dict[str, str]]:
        """
        Search for stock symbols using Alpha Vantage (if API key available)
        """
        if not self.alpha_vantage_key:
            logger.warning("Alpha Vantage API key not configured")
            return []
        
        try:
            async with httpx.AsyncClient() as client:
                params = {
                    'function': 'SYMBOL_SEARCH',
                    'keywords': query,
                    'apikey': self.alpha_vantage_key
                }
                
                response = await client.get(self.alpha_vantage_base_url, params=params)
                data = response.json()
                
                matches = data.get('bestMatches', [])
                results = []
                
                for match in matches[:10]:  # Limit to top 10 results
                    results.append({
                        'symbol': match.get('1. symbol', ''),
                        'name': match.get('2. name', ''),
                        'type': match.get('3. type', ''),
                        'region': match.get('4. region', ''),
                        'currency': match.get('8. currency', '')
                    })
                
                return results
        except Exception as e:
            logger.error(f"Error searching symbols for query '{query}': {e}")
            return []
    
    async def get_market_indices(self) -> Dict[str, float]:
        """
        Get current prices for major market indices
        """
        indices = {
            'S&P 500': '^GSPC',
            'Dow Jones': '^DJI',
            'NASDAQ': '^IXIC',
            'Russell 2000': '^RUT',
            'VIX': '^VIX'
        }
        
        prices = {}
        for name, symbol in indices.items():
            price = await self.get_current_price(symbol)
            prices[name] = price
        
        return prices
    
    async def get_crypto_prices(self, symbols: List[str]) -> Dict[str, float]:
        """
        Get cryptocurrency prices (using Yahoo Finance with -USD suffix)
        """
        crypto_symbols = [f"{symbol}-USD" for symbol in symbols]
        prices = await self.get_multiple_prices(crypto_symbols)
        
        # Remove -USD suffix from keys
        cleaned_prices = {}
        for symbol, price in prices.items():
            clean_symbol = symbol.replace('-USD', '')
            cleaned_prices[clean_symbol] = price
        
        return cleaned_prices
    
    def calculate_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate basic technical indicators
        """
        if df is None or df.empty:
            return df
        
        try:
            # Simple Moving Averages
            df['SMA_20'] = df['Close'].rolling(window=20).mean()
            df['SMA_50'] = df['Close'].rolling(window=50).mean()
            df['SMA_200'] = df['Close'].rolling(window=200).mean()
            
            # Exponential Moving Averages
            df['EMA_12'] = df['Close'].ewm(span=12).mean()
            df['EMA_26'] = df['Close'].ewm(span=26).mean()
            
            # MACD
            df['MACD'] = df['EMA_12'] - df['EMA_26']
            df['MACD_Signal'] = df['MACD'].ewm(span=9).mean()
            df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
            
            # RSI
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))
            
            # Bollinger Bands
            df['BB_Middle'] = df['Close'].rolling(window=20).mean()
            bb_std = df['Close'].rolling(window=20).std()
            df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
            df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
            
            # Volume indicators
            df['Volume_SMA'] = df['Volume'].rolling(window=20).mean()
            
            return df
        except Exception as e:
            logger.error(f"Error calculating technical indicators: {e}")
            return df