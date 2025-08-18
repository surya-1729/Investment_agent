#!/usr/bin/env python3
"""
SmartInvest Bot - Demo Script
Demonstrates the core functionality without external dependencies
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
import sys
import os

# Add workspace to path
sys.path.insert(0, '/workspace')

def demo_project_structure():
    """Show the project structure"""
    print("🏗️  SmartInvest Bot - Project Structure")
    print("=" * 50)
    
    structure = {
        "backend/": {
            "main.py": "FastAPI application entry point",
            "core/": {
                "config.py": "Application configuration",
                "database.py": "Database setup and connections"
            },
            "models/": {
                "user.py": "User authentication model",
                "portfolio.py": "Portfolio management model", 
                "asset.py": "Asset holdings model",
                "transaction.py": "Trading transactions model",
                "strategy.py": "Investment strategies model"
            },
            "api/endpoints/": {
                "auth.py": "Authentication endpoints",
                "market_data.py": "Market data API",
                "portfolio.py": "Portfolio management API",
                "strategies.py": "Strategy management API"
            },
            "services/": {
                "market_data.py": "Market data integration",
                "auth_service.py": "User authentication",
                "portfolio_service.py": "Portfolio calculations",
                "strategy_service.py": "Strategy execution"
            }
        },
        "frontend/": {
            "src/": {
                "App.tsx": "Main React application",
                "App.css": "Modern UI styling"
            }
        },
        "strategies/": {
            "base_strategy.py": "Base strategy interface",
            "technical_strategies.py": "MA, RSI, MACD strategies",
            "momentum_strategy.py": "Momentum-based strategy"
        }
    }
    
    def print_structure(struct, indent=0):
        for key, value in struct.items():
            print("  " * indent + f"📁 {key}" if key.endswith('/') else "  " * indent + f"📄 {key}")
            if isinstance(value, dict):
                print_structure(value, indent + 1)
            else:
                print("  " * (indent + 1) + f"   └─ {value}")
    
    print_structure(structure)
    print()

def demo_strategies():
    """Demonstrate the strategy system"""
    print("🤖 Investment Strategies Demo")
    print("=" * 30)
    
    # Mock data for demonstration
    mock_data = {
        'AAPL': {
            'price': 185.25,
            'sma_20': 182.50,
            'sma_50': 178.90,
            'rsi': 65.5,
            'macd': 0.45,
            'volume': 45000000
        },
        'GOOGL': {
            'price': 142.50,
            'sma_20': 145.20,
            'sma_50': 148.10,
            'rsi': 35.2,
            'volume': 28000000
        }
    }
    
    strategies = [
        {
            'name': 'Moving Average Crossover',
            'type': 'technical',
            'description': 'Buy when short MA crosses above long MA',
            'parameters': {'short_window': 20, 'long_window': 50},
            'signals': []
        },
        {
            'name': 'RSI Mean Reversion',
            'type': 'technical', 
            'description': 'Buy oversold, sell overbought conditions',
            'parameters': {'oversold': 30, 'overbought': 70},
            'signals': []
        },
        {
            'name': 'Momentum Strategy',
            'type': 'momentum',
            'description': 'Follow price momentum trends',
            'parameters': {'lookback': 20, 'threshold': 0.05},
            'signals': []
        }
    ]
    
    # Simulate strategy signals
    for symbol, data in mock_data.items():
        # MA Strategy
        if data['sma_20'] > data['sma_50']:
            strategies[0]['signals'].append({
                'symbol': symbol,
                'signal': 'BUY',
                'price': data['price'],
                'confidence': 0.75,
                'reason': f"SMA20 (${data['sma_20']}) > SMA50 (${data['sma_50']})"
            })
        
        # RSI Strategy
        if data['rsi'] < 40:
            strategies[1]['signals'].append({
                'symbol': symbol,
                'signal': 'BUY',
                'price': data['price'],
                'confidence': 0.68,
                'reason': f"RSI oversold at {data['rsi']}"
            })
    
    # Display strategies
    for strategy in strategies:
        print(f"📊 {strategy['name']}")
        print(f"   Type: {strategy['type']}")
        print(f"   Description: {strategy['description']}")
        print(f"   Parameters: {strategy['parameters']}")
        
        if strategy['signals']:
            print("   Recent Signals:")
            for signal in strategy['signals']:
                print(f"     • {signal['signal']} {signal['symbol']} at ${signal['price']:.2f}")
                print(f"       Confidence: {signal['confidence']:.0%} - {signal['reason']}")
        else:
            print("   No active signals")
        print()

def demo_portfolio():
    """Demonstrate portfolio management"""
    print("💼 Portfolio Management Demo")
    print("=" * 30)
    
    portfolio = {
        'name': 'Tech Growth Portfolio',
        'total_value': 105000,
        'cash_balance': 5000,
        'invested_amount': 100000,
        'total_return': 15000,
        'return_percentage': 17.65,
        'holdings': [
            {'symbol': 'AAPL', 'shares': 100, 'avg_cost': 150.00, 'current_price': 185.25, 'allocation': 35.5},
            {'symbol': 'GOOGL', 'shares': 75, 'avg_cost': 120.00, 'current_price': 142.50, 'allocation': 25.8},
            {'symbol': 'MSFT', 'shares': 50, 'avg_cost': 300.00, 'current_price': 378.90, 'allocation': 36.2},
            {'symbol': 'TSLA', 'shares': 10, 'avg_cost': 200.00, 'current_price': 248.75, 'allocation': 2.5}
        ]
    }
    
    print(f"Portfolio: {portfolio['name']}")
    print(f"Total Value: ${portfolio['total_value']:,}")
    print(f"Total Return: ${portfolio['total_return']:,} ({portfolio['return_percentage']:.2f}%)")
    print(f"Cash Balance: ${portfolio['cash_balance']:,}")
    print()
    
    print("Holdings:")
    for holding in portfolio['holdings']:
        market_value = holding['shares'] * holding['current_price']
        unrealized_gain = market_value - (holding['shares'] * holding['avg_cost'])
        gain_pct = (unrealized_gain / (holding['shares'] * holding['avg_cost'])) * 100
        
        print(f"  {holding['symbol']:6} | {holding['shares']:3} shares | "
              f"${holding['current_price']:7.2f} | ${market_value:8,.0f} | "
              f"{gain_pct:+6.1f}% | {holding['allocation']:4.1f}%")
    
    print()

def demo_api_endpoints():
    """Show available API endpoints"""
    print("🌐 API Endpoints")
    print("=" * 20)
    
    endpoints = {
        "Authentication": [
            "POST /api/v1/auth/register - Register new user",
            "POST /api/v1/auth/login - User login",
            "GET  /api/v1/auth/me - Get current user"
        ],
        "Market Data": [
            "GET  /api/v1/market/price/{symbol} - Current price",
            "POST /api/v1/market/prices - Multiple prices",
            "GET  /api/v1/market/historical/{symbol} - Historical data",
            "GET  /api/v1/market/technical/{symbol} - Technical indicators"
        ],
        "Portfolios": [
            "GET  /api/v1/portfolios/ - List portfolios",
            "POST /api/v1/portfolios/ - Create portfolio",
            "GET  /api/v1/portfolios/{id} - Portfolio details",
            "PUT  /api/v1/portfolios/{id} - Update portfolio"
        ],
        "Strategies": [
            "GET  /api/v1/strategies/ - List strategies",
            "POST /api/v1/strategies/ - Create strategy",
            "GET  /api/v1/strategies/{id} - Strategy details",
            "PUT  /api/v1/strategies/{id} - Update strategy"
        ]
    }
    
    for category, endpoint_list in endpoints.items():
        print(f"📂 {category}")
        for endpoint in endpoint_list:
            print(f"   {endpoint}")
        print()

def demo_features():
    """Highlight key features"""
    print("✨ Key Features")
    print("=" * 20)
    
    features = [
        "📊 Real-time market data integration",
        "🤖 Automated investment strategies",
        "📈 Portfolio performance tracking", 
        "⚡ Strategy backtesting engine",
        "🎯 Risk management tools",
        "📱 Modern React dashboard",
        "🔒 JWT authentication",
        "🐳 Docker deployment ready",
        "📚 Comprehensive API documentation",
        "🧪 Full test suite"
    ]
    
    for feature in features:
        print(f"  {feature}")
    print()

def main():
    """Run the demo"""
    print("🚀 SmartInvest Bot - Complete Demo")
    print("🤖 Intelligent Investment Management Platform")
    print("=" * 60)
    print()
    
    demo_project_structure()
    demo_strategies()
    demo_portfolio()
    demo_api_endpoints()
    demo_features()
    
    print("🎯 Next Steps:")
    print("  1. Install dependencies: pip install -r requirements.txt")
    print("  2. Set up environment: cp .env.example .env")
    print("  3. Start backend: python start_app.py")
    print("  4. Start frontend: cd frontend && npm start")
    print("  5. Visit: http://localhost:3000")
    print()
    print("📚 Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print()
    print("🎉 SmartInvest Bot is ready for intelligent investing!")

if __name__ == "__main__":
    main()