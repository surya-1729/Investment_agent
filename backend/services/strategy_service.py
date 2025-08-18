"""
Strategy service for managing and executing investment strategies
"""

import asyncio
from typing import Dict, List, Optional, Any, Type
import pandas as pd
from datetime import datetime, timedelta
from loguru import logger
from sqlalchemy.orm import Session

from backend.services.market_data import MarketDataService
from strategies.base_strategy import BaseStrategy, TradingSignal
from strategies.technical_strategies import MovingAverageStrategy, RSIStrategy, MACDStrategy
from strategies.momentum_strategy import MomentumStrategy


class StrategyService:
    """Service for managing and executing investment strategies"""
    
    def __init__(self):
        self.market_service = MarketDataService()
        self.available_strategies = self._register_strategies()
    
    def _register_strategies(self) -> Dict[str, Type[BaseStrategy]]:
        """Register available strategy classes"""
        return {
            'moving_average': MovingAverageStrategy,
            'rsi': RSIStrategy,
            'macd': MACDStrategy,
            'momentum': MomentumStrategy
        }
    
    def get_available_strategies(self) -> Dict[str, Dict[str, Any]]:
        """Get information about available strategies"""
        strategies_info = {}
        
        for name, strategy_class in self.available_strategies.items():
            # Create a temporary instance to get default parameters
            temp_strategy = strategy_class()
            strategies_info[name] = {
                'name': temp_strategy.name,
                'class_name': strategy_class.__name__,
                'description': strategy_class.__doc__,
                'default_parameters': temp_strategy.parameters,
                'required_indicators': temp_strategy.get_required_indicators()
            }
        
        return strategies_info
    
    def create_strategy(self, strategy_type: str, parameters: Dict[str, Any] = None) -> Optional[BaseStrategy]:
        """Create a strategy instance"""
        if strategy_type not in self.available_strategies:
            logger.error(f"Unknown strategy type: {strategy_type}")
            return None
        
        try:
            strategy_class = self.available_strategies[strategy_type]
            strategy = strategy_class(parameters)
            return strategy
        except Exception as e:
            logger.error(f"Error creating strategy {strategy_type}: {e}")
            return None
    
    async def execute_strategy(
        self, 
        strategy: BaseStrategy, 
        symbols: List[str],
        period: str = "6mo",
        interval: str = "1d"
    ) -> Dict[str, List[TradingSignal]]:
        """
        Execute a strategy on multiple symbols
        
        Args:
            strategy: Strategy instance to execute
            symbols: List of stock symbols
            period: Data period to analyze
            interval: Data interval
            
        Returns:
            Dictionary mapping symbols to their generated signals
        """
        results = {}
        
        for symbol in symbols:
            try:
                # Get historical data
                data = await self.market_service.get_historical_data(symbol, period, interval)
                if data is None or data.empty:
                    logger.warning(f"No data available for {symbol}")
                    results[symbol] = []
                    continue
                
                # Calculate technical indicators
                data = self.market_service.calculate_technical_indicators(data)
                
                # Generate signals
                signals = strategy.generate_signals(data, symbol)
                results[symbol] = signals
                
                logger.info(f"Generated {len(signals)} signals for {symbol}")
                
            except Exception as e:
                logger.error(f"Error executing strategy for {symbol}: {e}")
                results[symbol] = []
        
        return results
    
    async def backtest_strategy(
        self,
        strategy: BaseStrategy,
        symbols: List[str],
        start_date: datetime,
        end_date: datetime,
        initial_capital: float = 10000.0
    ) -> Dict[str, Any]:
        """
        Backtest a strategy over a historical period
        
        Args:
            strategy: Strategy to backtest
            symbols: List of symbols to trade
            start_date: Backtest start date
            end_date: Backtest end date
            initial_capital: Starting capital
            
        Returns:
            Backtest results with performance metrics
        """
        try:
            # Calculate period for data fetching
            days_diff = (end_date - start_date).days
            if days_diff <= 30:
                period = "1mo"
            elif days_diff <= 90:
                period = "3mo"
            elif days_diff <= 180:
                period = "6mo"
            elif days_diff <= 365:
                period = "1y"
            else:
                period = "2y"
            
            # Execute strategy to get signals
            all_signals = await self.execute_strategy(strategy, symbols, period)
            
            # Simulate trading based on signals
            portfolio_value = initial_capital
            cash = initial_capital
            positions = {}
            trades = []
            portfolio_history = []
            
            # Collect all signals and sort by timestamp
            all_signals_list = []
            for symbol, signals in all_signals.items():
                for signal in signals:
                    if signal.timestamp and start_date <= signal.timestamp <= end_date:
                        all_signals_list.append((symbol, signal))
            
            # Sort signals by timestamp
            all_signals_list.sort(key=lambda x: x[1].timestamp)
            
            # Process signals chronologically
            for symbol, signal in all_signals_list:
                position_size = strategy.calculate_position_size(portfolio_value, signal.confidence)
                
                if signal.signal.value == 'buy' and cash >= position_size:
                    # Buy signal
                    shares = position_size / signal.price
                    positions[symbol] = positions.get(symbol, 0) + shares
                    cash -= position_size
                    
                    trades.append({
                        'symbol': symbol,
                        'action': 'buy',
                        'shares': shares,
                        'price': signal.price,
                        'value': position_size,
                        'timestamp': signal.timestamp,
                        'confidence': signal.confidence
                    })
                    
                elif signal.signal.value == 'sell' and symbol in positions and positions[symbol] > 0:
                    # Sell signal
                    shares_to_sell = positions[symbol]
                    sell_value = shares_to_sell * signal.price
                    cash += sell_value
                    positions[symbol] = 0
                    
                    trades.append({
                        'symbol': symbol,
                        'action': 'sell',
                        'shares': shares_to_sell,
                        'price': signal.price,
                        'value': sell_value,
                        'timestamp': signal.timestamp,
                        'confidence': signal.confidence
                    })
                
                # Update portfolio value
                portfolio_value = cash
                for pos_symbol, shares in positions.items():
                    if shares > 0:
                        # Get current price (use signal price as approximation)
                        current_price = signal.price if pos_symbol == symbol else signal.price
                        portfolio_value += shares * current_price
                
                portfolio_history.append({
                    'timestamp': signal.timestamp,
                    'portfolio_value': portfolio_value,
                    'cash': cash
                })
            
            # Calculate performance metrics
            total_return = portfolio_value - initial_capital
            total_return_pct = (total_return / initial_capital) * 100
            
            winning_trades = len([t for t in trades if self._is_winning_trade(t, trades)])
            total_trades = len(trades)
            win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
            
            return {
                'initial_capital': initial_capital,
                'final_value': portfolio_value,
                'total_return': total_return,
                'total_return_percentage': total_return_pct,
                'total_trades': total_trades,
                'winning_trades': winning_trades,
                'losing_trades': total_trades - winning_trades,
                'win_rate': win_rate,
                'trades': trades,
                'portfolio_history': portfolio_history,
                'strategy_info': strategy.get_strategy_info()
            }
            
        except Exception as e:
            logger.error(f"Error during backtesting: {e}")
            return {
                'error': str(e),
                'initial_capital': initial_capital,
                'final_value': initial_capital,
                'total_return': 0,
                'total_return_percentage': 0
            }
    
    def _is_winning_trade(self, trade: Dict[str, Any], all_trades: List[Dict[str, Any]]) -> bool:
        """Determine if a trade was profitable (simplified logic)"""
        if trade['action'] != 'sell':
            return False
        
        # Find corresponding buy trade for the same symbol
        symbol = trade['symbol']
        sell_time = trade['timestamp']
        
        # Look for the most recent buy trade before this sell
        buy_trades = [
            t for t in all_trades 
            if t['symbol'] == symbol and t['action'] == 'buy' and t['timestamp'] < sell_time
        ]
        
        if not buy_trades:
            return False
        
        # Get the most recent buy trade
        recent_buy = max(buy_trades, key=lambda x: x['timestamp'])
        
        # Compare prices
        return trade['price'] > recent_buy['price']
    
    async def get_current_signals(
        self,
        strategy: BaseStrategy,
        symbols: List[str]
    ) -> Dict[str, List[TradingSignal]]:
        """
        Get current trading signals for given symbols
        """
        # Use recent data for current analysis
        return await self.execute_strategy(strategy, symbols, period="3mo", interval="1d")
    
    def validate_strategy_parameters(self, strategy_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate strategy parameters and return validation results
        """
        if strategy_type not in self.available_strategies:
            return {
                'valid': False,
                'errors': [f'Unknown strategy type: {strategy_type}']
            }
        
        errors = []
        warnings = []
        
        try:
            # Try to create strategy with parameters
            strategy = self.create_strategy(strategy_type, parameters)
            if strategy is None:
                errors.append('Failed to create strategy with provided parameters')
            
        except Exception as e:
            errors.append(f'Parameter validation error: {str(e)}')
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }