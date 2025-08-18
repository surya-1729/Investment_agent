import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { TrendingUp, DollarSign, Target, Activity, BarChart3, Settings } from 'lucide-react';
import './App.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

interface MarketData {
  symbol: string;
  price: number;
  timestamp: string;
}

interface Portfolio {
  id: number;
  name: string;
  total_value: number;
  cash_balance: number;
  total_return: number;
  total_return_percentage: number;
}

interface Strategy {
  id: number;
  name: string;
  strategy_type: string;
  total_return_percentage: number;
  win_rate: number;
  is_active: boolean;
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

function App() {
  const [marketData, setMarketData] = useState<MarketData[]>([]);
  const [portfolios, setPortfolios] = useState<Portfolio[]>([]);
  const [strategies, setStrategies] = useState<Strategy[]>([]);
  const [selectedTab, setSelectedTab] = useState('dashboard');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchMarketData();
    // fetchPortfolios();
    // fetchStrategies();
  }, []);

  const fetchMarketData = async () => {
    try {
      const symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN'];
      const response = await axios.post(`${API_BASE_URL}/market/prices`, symbols);
      
      const marketDataArray = Object.entries(response.data.prices).map(([symbol, price]) => ({
        symbol,
        price: price as number,
        timestamp: response.data.timestamp
      }));
      
      setMarketData(marketDataArray);
    } catch (error) {
      console.error('Error fetching market data:', error);
      // Mock data for demo
      setMarketData([
        { symbol: 'AAPL', price: 185.25, timestamp: new Date().toISOString() },
        { symbol: 'GOOGL', price: 142.50, timestamp: new Date().toISOString() },
        { symbol: 'MSFT', price: 378.90, timestamp: new Date().toISOString() },
        { symbol: 'TSLA', price: 248.75, timestamp: new Date().toISOString() },
        { symbol: 'AMZN', price: 155.30, timestamp: new Date().toISOString() }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const mockPortfolioData = [
    { name: 'Tech Portfolio', value: 45000, return: 12.5 },
    { name: 'Dividend Portfolio', value: 32000, return: 8.3 },
    { name: 'Growth Portfolio', value: 28000, return: 18.7 }
  ];

  const mockPerformanceData = [
    { date: '2024-01', value: 10000 },
    { date: '2024-02', value: 10500 },
    { date: '2024-03', value: 11200 },
    { date: '2024-04', value: 10800 },
    { date: '2024-05', value: 12100 },
    { date: '2024-06', value: 12800 },
    { date: '2024-07', value: 13500 },
    { date: '2024-08', value: 13200 },
    { date: '2024-09', value: 14100 },
    { date: '2024-10', value: 14800 },
    { date: '2024-11', value: 15200 },
    { date: '2024-12', value: 15800 }
  ];

  const renderDashboard = () => (
    <div className="dashboard">
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">
            <DollarSign size={24} />
          </div>
          <div className="stat-content">
            <h3>Total Portfolio Value</h3>
            <p className="stat-value">$105,000</p>
            <p className="stat-change positive">+12.5% this month</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">
            <TrendingUp size={24} />
          </div>
          <div className="stat-content">
            <h3>Total Return</h3>
            <p className="stat-value">+$15,800</p>
            <p className="stat-change positive">+17.7% overall</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">
            <Target size={24} />
          </div>
          <div className="stat-content">
            <h3>Active Strategies</h3>
            <p className="stat-value">4</p>
            <p className="stat-change">2 profitable</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">
            <Activity size={24} />
          </div>
          <div className="stat-content">
            <h3>Win Rate</h3>
            <p className="stat-value">68.5%</p>
            <p className="stat-change positive">Above average</p>
          </div>
        </div>
      </div>

      <div className="charts-grid">
        <div className="chart-container">
          <h3>Portfolio Performance</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={mockPerformanceData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip formatter={(value) => [`$${value.toLocaleString()}`, 'Portfolio Value']} />
              <Legend />
              <Line type="monotone" dataKey="value" stroke="#0088FE" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-container">
          <h3>Portfolio Allocation</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={mockPortfolioData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: $${value.toLocaleString()}`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {mockPortfolioData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => [`$${value.toLocaleString()}`, 'Value']} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="market-data">
        <h3>Market Overview</h3>
        <div className="market-grid">
          {marketData.map((stock) => (
            <div key={stock.symbol} className="market-card">
              <h4>{stock.symbol}</h4>
              <p className="price">${stock.price.toFixed(2)}</p>
              <p className="change positive">+2.3%</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderStrategies = () => (
    <div className="strategies">
      <div className="section-header">
        <h2>Investment Strategies</h2>
        <button className="btn-primary">Create New Strategy</button>
      </div>
      
      <div className="strategies-grid">
        <div className="strategy-card">
          <h3>Moving Average Crossover</h3>
          <p>Technical strategy based on MA crossovers</p>
          <div className="strategy-stats">
            <span>Return: +15.2%</span>
            <span>Win Rate: 72%</span>
            <span>Active: Yes</span>
          </div>
          <div className="strategy-actions">
            <button className="btn-secondary">Backtest</button>
            <button className="btn-secondary">Edit</button>
          </div>
        </div>

        <div className="strategy-card">
          <h3>RSI Mean Reversion</h3>
          <p>Contrarian strategy using RSI indicators</p>
          <div className="strategy-stats">
            <span>Return: +8.7%</span>
            <span>Win Rate: 64%</span>
            <span>Active: Yes</span>
          </div>
          <div className="strategy-actions">
            <button className="btn-secondary">Backtest</button>
            <button className="btn-secondary">Edit</button>
          </div>
        </div>

        <div className="strategy-card">
          <h3>Momentum Strategy</h3>
          <p>Trend following based on price momentum</p>
          <div className="strategy-stats">
            <span>Return: +22.1%</span>
            <span>Win Rate: 59%</span>
            <span>Active: No</span>
          </div>
          <div className="strategy-actions">
            <button className="btn-secondary">Backtest</button>
            <button className="btn-secondary">Edit</button>
          </div>
        </div>
      </div>
    </div>
  );

  const renderPortfolios = () => (
    <div className="portfolios">
      <div className="section-header">
        <h2>My Portfolios</h2>
        <button className="btn-primary">Create Portfolio</button>
      </div>
      
      <div className="portfolios-list">
        {mockPortfolioData.map((portfolio, index) => (
          <div key={index} className="portfolio-card">
            <div className="portfolio-info">
              <h3>{portfolio.name}</h3>
              <p className="portfolio-value">${portfolio.value.toLocaleString()}</p>
              <p className={`portfolio-return ${portfolio.return > 0 ? 'positive' : 'negative'}`}>
                {portfolio.return > 0 ? '+' : ''}{portfolio.return}%
              </p>
            </div>
            <div className="portfolio-actions">
              <button className="btn-secondary">View Details</button>
              <button className="btn-secondary">Rebalance</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  if (isLoading) {
    return (
      <div className="loading">
        <div className="loading-spinner"></div>
        <p>Loading SmartInvest Bot...</p>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="app-header">
        <div className="header-content">
          <h1>🤖 SmartInvest Bot</h1>
          <p>Intelligent Investment Management</p>
        </div>
      </header>

      <nav className="app-nav">
        <button 
          className={selectedTab === 'dashboard' ? 'nav-btn active' : 'nav-btn'}
          onClick={() => setSelectedTab('dashboard')}
        >
          <BarChart3 size={20} />
          Dashboard
        </button>
        <button 
          className={selectedTab === 'portfolios' ? 'nav-btn active' : 'nav-btn'}
          onClick={() => setSelectedTab('portfolios')}
        >
          <DollarSign size={20} />
          Portfolios
        </button>
        <button 
          className={selectedTab === 'strategies' ? 'nav-btn active' : 'nav-btn'}
          onClick={() => setSelectedTab('strategies')}
        >
          <Target size={20} />
          Strategies
        </button>
        <button 
          className={selectedTab === 'settings' ? 'nav-btn active' : 'nav-btn'}
          onClick={() => setSelectedTab('settings')}
        >
          <Settings size={20} />
          Settings
        </button>
      </nav>

      <main className="app-main">
        {selectedTab === 'dashboard' && renderDashboard()}
        {selectedTab === 'portfolios' && renderPortfolios()}
        {selectedTab === 'strategies' && renderStrategies()}
        {selectedTab === 'settings' && (
          <div className="settings">
            <h2>Settings</h2>
            <p>Configuration options will be available here.</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;