# 🤖 SmartInvest Bot

An intelligent investment bot application that analyzes market data, executes trading strategies, and manages portfolios automatically.

![SmartInvest Bot](https://img.shields.io/badge/Status-Beta-yellow)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![React](https://img.shields.io/badge/React-18+-blue)

## 🌟 Features

- 📊 **Real-time Market Data**: Integration with Yahoo Finance and Alpha Vantage APIs
- 🤖 **Automated Trading Strategies**: Technical analysis, momentum, and mean reversion strategies
- 📈 **Portfolio Management**: Track performance, allocation, and rebalancing suggestions
- ⚡ **Backtesting Engine**: Test strategies on historical data
- 🎯 **Risk Management**: Stop-loss, take-profit, and position sizing
- 📱 **Modern Web Dashboard**: Beautiful React interface with real-time charts
- 🔒 **Secure Authentication**: JWT-based user authentication
- 🐳 **Docker Support**: Easy deployment with Docker containers

## 🏗️ Architecture

```
SmartInvest Bot/
├── backend/           # FastAPI backend
│   ├── api/          # REST API endpoints
│   ├── core/         # Configuration and database
│   ├── models/       # SQLAlchemy database models
│   ├── schemas/      # Pydantic data validation
│   └── services/     # Business logic services
├── frontend/         # React TypeScript frontend
├── strategies/       # Investment strategy implementations
├── data/            # Data storage and models
├── utils/           # Utility functions
└── tests/           # Test files
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 16+
- PostgreSQL (optional, SQLite used by default)
- Redis (for background tasks)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd smartinvest-bot
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

4. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

### Running the Application

#### Option 1: Quick Start (Backend Only)
```bash
python start_app.py
```

#### Option 2: Full Stack Development
```bash
# Terminal 1: Start backend
python start_app.py

# Terminal 2: Start frontend
cd frontend
npm start
```

#### Option 3: Docker (Recommended for Production)
```bash
docker-compose up
```

### Testing the Application

Run the test suite to verify everything works:
```bash
python test_app.py
```

## 📊 API Endpoints

### Market Data
- `GET /api/v1/market/price/{symbol}` - Get current price
- `POST /api/v1/market/prices` - Get multiple prices
- `GET /api/v1/market/historical/{symbol}` - Get historical data
- `GET /api/v1/market/technical/{symbol}` - Get technical indicators

### Portfolio Management
- `GET /api/v1/portfolios/` - List user portfolios
- `POST /api/v1/portfolios/` - Create new portfolio
- `GET /api/v1/portfolios/{id}` - Get portfolio details
- `PUT /api/v1/portfolios/{id}` - Update portfolio

### Investment Strategies
- `GET /api/v1/strategies/` - List user strategies
- `POST /api/v1/strategies/` - Create new strategy
- `GET /api/v1/strategies/{id}` - Get strategy details

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user info

## 🎯 Investment Strategies

### Built-in Strategies

1. **Moving Average Crossover**
   - Buy when short MA crosses above long MA
   - Sell when short MA crosses below long MA
   - Configurable periods (default: 20/50)

2. **RSI Mean Reversion**
   - Buy when RSI < 30 (oversold)
   - Sell when RSI > 70 (overbought)
   - Configurable thresholds

3. **MACD Strategy**
   - Buy when MACD crosses above signal line
   - Sell when MACD crosses below signal line
   - Volume confirmation available

4. **Momentum Strategy**
   - Buy on strong positive momentum
   - Sell on strong negative momentum
   - Configurable lookback periods

### Creating Custom Strategies

```python
from strategies.base_strategy import BaseStrategy, TradingSignal, SignalType

class MyStrategy(BaseStrategy):
    def __init__(self, parameters=None):
        super().__init__("My Custom Strategy", parameters)
    
    def get_required_indicators(self):
        return ['SMA_20', 'RSI']
    
    def generate_signals(self, data, symbol):
        signals = []
        # Your strategy logic here
        return signals
```

## 📈 Dashboard Features

### Main Dashboard
- Portfolio performance overview
- Real-time market data
- Strategy performance metrics
- Asset allocation charts

### Portfolio Management
- Multiple portfolio support
- Performance tracking
- Rebalancing suggestions
- Risk metrics

### Strategy Management
- Strategy creation and editing
- Backtesting capabilities
- Performance analytics
- Parameter optimization

## 🔧 Configuration

### Environment Variables

```bash
# API Keys
ALPHA_VANTAGE_API_KEY=your_key_here
POLYGON_API_KEY=your_key_here

# Database
DATABASE_URL=postgresql://user:pass@localhost/smartinvest

# Security
SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Trading
PAPER_TRADING=True
INITIAL_BALANCE=10000.00
```

### Strategy Parameters

Each strategy can be configured with custom parameters:

```python
# Moving Average Strategy
{
    "short_window": 20,
    "long_window": 50,
    "min_data_points": 60
}

# RSI Strategy
{
    "rsi_period": 14,
    "oversold_threshold": 30,
    "overbought_threshold": 70
}
```

## 🧪 Testing

### Unit Tests
```bash
pytest tests/
```

### Integration Tests
```bash
python test_app.py
```

### Strategy Backtesting
```bash
python -c "
from strategies.technical_strategies import MovingAverageStrategy
from backend.services.strategy_service import StrategyService
import asyncio

async def test():
    service = StrategyService()
    strategy = MovingAverageStrategy()
    results = await service.backtest_strategy(
        strategy, ['AAPL'], 
        start_date='2023-01-01', 
        end_date='2023-12-31'
    )
    print(f'Return: {results[\"total_return_percentage\"]:.2f}%')

asyncio.run(test())
"
```

## 🚀 Deployment

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build

# Scale services
docker-compose up --scale app=3
```

### Manual Deployment
```bash
# Install dependencies
pip install -r requirements.txt

# Set up database
alembic upgrade head

# Start with Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.main:app
```

## 📚 API Documentation

Once the application is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This software is for educational and research purposes only. Trading and investing carry significant financial risks. The authors are not responsible for any financial losses incurred through the use of this software. Always consult with a qualified financial advisor before making investment decisions.

## 🆘 Support

- 📧 Email: support@smartinvestbot.com
- 💬 Discord: [Join our community](https://discord.gg/smartinvestbot)
- 📖 Documentation: [Full documentation](https://docs.smartinvestbot.com)
- 🐛 Issues: [GitHub Issues](https://github.com/smartinvestbot/issues)

## 🗺️ Roadmap

### Version 1.1
- [ ] Machine learning-based strategies
- [ ] Options trading support
- [ ] Advanced risk metrics
- [ ] Mobile app

### Version 1.2
- [ ] Cryptocurrency support
- [ ] Social trading features
- [ ] Advanced charting tools
- [ ] Paper trading competitions

### Version 2.0
- [ ] Multi-broker integration
- [ ] Advanced portfolio optimization
- [ ] Sentiment analysis
- [ ] Automated reporting

---

Made with ❤️ by the SmartInvest Bot team