#!/usr/bin/env python3
"""
Test script for SmartInvest Bot API
"""

import asyncio
import sys
import os

# Add the workspace to Python path
sys.path.insert(0, '/workspace')

from backend.services.market_data import MarketDataService
from backend.services.strategy_service import StrategyService
from strategies.technical_strategies import MovingAverageStrategy, RSIStrategy
from strategies.momentum_strategy import MomentumStrategy


async def test_market_data():
    """Test market data service"""
    print("🔍 Testing Market Data Service...")
    
    market_service = MarketDataService()
    
    # Test getting current price
    print("  Getting current price for AAPL...")
    price = await market_service.get_current_price("AAPL")
    print(f"  AAPL current price: ${price}")
    
    # Test getting multiple prices
    print("  Getting prices for multiple stocks...")
    symbols = ["AAPL", "GOOGL", "MSFT"]
    prices = await market_service.get_multiple_prices(symbols)
    for symbol, price in prices.items():
        print(f"  {symbol}: ${price}")
    
    # Test historical data
    print("  Getting historical data for AAPL...")
    data = await market_service.get_historical_data("AAPL", period="1mo")
    if data is not None:
        print(f"  Retrieved {len(data)} days of historical data")
        print(f"  Latest close price: ${data['Close'].iloc[-1]:.2f}")
    
    # Test technical indicators
    if data is not None:
        print("  Calculating technical indicators...")
        data_with_indicators = market_service.calculate_technical_indicators(data)
        latest = data_with_indicators.iloc[-1]
        print(f"  RSI: {latest.get('RSI', 'N/A'):.2f}")
        print(f"  MACD: {latest.get('MACD', 'N/A'):.4f}")
        print(f"  SMA_20: ${latest.get('SMA_20', 'N/A'):.2f}")
    
    print("✅ Market Data Service test completed\n")


async def test_strategies():
    """Test investment strategies"""
    print("🤖 Testing Investment Strategies...")
    
    strategy_service = StrategyService()
    market_service = MarketDataService()
    
    # Test available strategies
    print("  Available strategies:")
    strategies_info = strategy_service.get_available_strategies()
    for name, info in strategies_info.items():
        print(f"    - {info['name']} ({name})")
    
    # Test creating strategies
    print("  Creating Moving Average strategy...")
    ma_strategy = strategy_service.create_strategy('moving_average', {
        'short_window': 10,
        'long_window': 30
    })
    
    print("  Creating RSI strategy...")
    rsi_strategy = strategy_service.create_strategy('rsi', {
        'oversold_threshold': 30,
        'overbought_threshold': 70
    })
    
    # Test strategy execution with sample data
    print("  Testing strategy execution...")
    symbols = ["AAPL"]
    
    # Get historical data
    data = await market_service.get_historical_data("AAPL", period="3mo")
    if data is not None:
        # Calculate indicators
        data = market_service.calculate_technical_indicators(data)
        
        # Test MA strategy
        if ma_strategy:
            print("    Executing Moving Average strategy...")
            ma_signals = ma_strategy.generate_signals(data, "AAPL")
            print(f"    Generated {len(ma_signals)} MA signals")
            
            if ma_signals:
                latest_signal = ma_signals[-1]
                print(f"    Latest MA signal: {latest_signal.signal.value} at ${latest_signal.price:.2f}")
        
        # Test RSI strategy
        if rsi_strategy:
            print("    Executing RSI strategy...")
            rsi_signals = rsi_strategy.generate_signals(data, "AAPL")
            print(f"    Generated {len(rsi_signals)} RSI signals")
            
            if rsi_signals:
                latest_signal = rsi_signals[-1]
                print(f"    Latest RSI signal: {latest_signal.signal.value} at ${latest_signal.price:.2f}")
    
    print("✅ Investment Strategies test completed\n")


async def test_backtesting():
    """Test strategy backtesting"""
    print("📈 Testing Strategy Backtesting...")
    
    strategy_service = StrategyService()
    
    # Create a simple momentum strategy
    momentum_strategy = MomentumStrategy({
        'lookback_period': 20,
        'momentum_threshold': 0.05
    })
    
    # Test backtesting
    from datetime import datetime, timedelta
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    print(f"  Backtesting momentum strategy from {start_date.date()} to {end_date.date()}")
    
    results = await strategy_service.backtest_strategy(
        momentum_strategy,
        ["AAPL"],
        start_date,
        end_date,
        initial_capital=10000.0
    )
    
    print(f"  Initial Capital: ${results['initial_capital']:,.2f}")
    print(f"  Final Value: ${results['final_value']:,.2f}")
    print(f"  Total Return: ${results['total_return']:,.2f} ({results['total_return_percentage']:.2f}%)")
    print(f"  Total Trades: {results['total_trades']}")
    print(f"  Win Rate: {results['win_rate']:.1f}%")
    
    print("✅ Strategy Backtesting test completed\n")


async def main():
    """Run all tests"""
    print("🚀 SmartInvest Bot - Test Suite")
    print("=" * 50)
    
    try:
        await test_market_data()
        await test_strategies()
        await test_backtesting()
        
        print("🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())