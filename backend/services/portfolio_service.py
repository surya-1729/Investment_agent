"""
Portfolio service for managing portfolios and calculating performance metrics
"""

from typing import Dict, List, Optional, Any
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from loguru import logger

from backend.models.portfolio import Portfolio
from backend.models.asset import Asset
from backend.models.transaction import Transaction
from backend.services.market_data import MarketDataService


class PortfolioService:
    """Service for portfolio management and performance calculations"""
    
    def __init__(self):
        self.market_service = MarketDataService()
    
    async def update_portfolio_values(self, db: Session, portfolio_id: int) -> Portfolio:
        """
        Update portfolio values with current market prices
        """
        portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
        if not portfolio:
            raise ValueError(f"Portfolio {portfolio_id} not found")
        
        # Get all assets in portfolio
        assets = db.query(Asset).filter(
            Asset.portfolio_id == portfolio_id,
            Asset.is_active == True,
            Asset.quantity > 0
        ).all()
        
        if not assets:
            # Portfolio has no assets, just update with cash balance
            portfolio.total_value = portfolio.cash_balance
            portfolio.invested_amount = 0.0
            db.commit()
            return portfolio
        
        # Get current prices for all symbols
        symbols = [asset.symbol for asset in assets]
        current_prices = await self.market_service.get_multiple_prices(symbols)
        
        total_market_value = 0.0
        total_invested = 0.0
        total_unrealized_gain_loss = 0.0
        
        # Update each asset
        for asset in assets:
            current_price = current_prices.get(asset.symbol)
            if current_price:
                asset.current_price = current_price
                asset.market_value = asset.quantity * current_price
                asset.unrealized_gain_loss = asset.market_value - (asset.quantity * asset.average_cost)
                
                if asset.quantity * asset.average_cost > 0:
                    asset.unrealized_gain_loss_percentage = (
                        asset.unrealized_gain_loss / (asset.quantity * asset.average_cost) * 100
                    )
                
                asset.last_price_update = datetime.utcnow()
                
                total_market_value += asset.market_value
                total_invested += asset.quantity * asset.average_cost
                total_unrealized_gain_loss += asset.unrealized_gain_loss
        
        # Update portfolio totals
        portfolio.invested_amount = total_invested
        portfolio.total_value = portfolio.cash_balance + total_market_value
        portfolio.total_return = total_unrealized_gain_loss
        
        if total_invested > 0:
            portfolio.total_return_percentage = (total_unrealized_gain_loss / total_invested) * 100
        
        # Update asset allocations
        for asset in assets:
            if portfolio.total_value > 0:
                asset.current_allocation = (asset.market_value / portfolio.total_value) * 100
        
        db.commit()
        return portfolio
    
    async def calculate_portfolio_metrics(self, db: Session, portfolio_id: int) -> Dict[str, Any]:
        """
        Calculate comprehensive portfolio performance metrics
        """
        portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
        if not portfolio:
            raise ValueError(f"Portfolio {portfolio_id} not found")
        
        # Update current values first
        portfolio = await self.update_portfolio_values(db, portfolio_id)
        
        # Get historical transactions for performance calculation
        transactions = db.query(Transaction).filter(
            Transaction.portfolio_id == portfolio_id,
            Transaction.status == "executed"
        ).order_by(Transaction.executed_at).all()
        
        # Calculate time-weighted return and other metrics
        metrics = await self._calculate_advanced_metrics(portfolio, transactions)
        
        return {
            'portfolio_id': portfolio_id,
            'total_value': portfolio.total_value,
            'cash_balance': portfolio.cash_balance,
            'invested_amount': portfolio.invested_amount,
            'total_return': portfolio.total_return,
            'total_return_percentage': portfolio.total_return_percentage,
            'daily_return': portfolio.daily_return,
            'metrics': metrics
        }
    
    async def _calculate_advanced_metrics(self, portfolio: Portfolio, transactions: List[Transaction]) -> Dict[str, Any]:
        """
        Calculate advanced portfolio metrics like Sharpe ratio, beta, etc.
        """
        try:
            # For now, return basic metrics
            # In a full implementation, you would calculate these based on historical data
            return {
                'sharpe_ratio': portfolio.sharpe_ratio,
                'beta': portfolio.beta,
                'max_drawdown': portfolio.max_drawdown,
                'volatility': portfolio.volatility,
                'total_trades': len(transactions),
                'win_rate': self._calculate_win_rate(transactions)
            }
        except Exception as e:
            logger.error(f"Error calculating advanced metrics: {e}")
            return {}
    
    def _calculate_win_rate(self, transactions: List[Transaction]) -> float:
        """
        Calculate win rate from transactions
        """
        sell_transactions = [t for t in transactions if t.transaction_type == 'sell']
        if not sell_transactions:
            return 0.0
        
        # Simplified win rate calculation
        # In practice, you'd match buy/sell pairs and compare prices
        profitable_trades = 0
        for transaction in sell_transactions:
            # This is a simplified approach
            # You would need to find corresponding buy transactions and calculate P&L
            if transaction.total_return and transaction.total_return > 0:
                profitable_trades += 1
        
        return (profitable_trades / len(sell_transactions)) * 100 if sell_transactions else 0.0
    
    async def suggest_rebalancing(self, db: Session, portfolio_id: int) -> Dict[str, Any]:
        """
        Suggest portfolio rebalancing based on target allocations
        """
        portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
        if not portfolio:
            raise ValueError(f"Portfolio {portfolio_id} not found")
        
        # Update current values
        await self.update_portfolio_values(db, portfolio_id)
        
        # Get assets with target allocations
        assets = db.query(Asset).filter(
            Asset.portfolio_id == portfolio_id,
            Asset.is_active == True
        ).all()
        
        suggestions = []
        total_deviation = 0.0
        
        for asset in assets:
            if asset.target_allocation > 0:
                deviation = asset.current_allocation - asset.target_allocation
                abs_deviation = abs(deviation)
                
                if abs_deviation > portfolio.rebalance_threshold:
                    target_value = (asset.target_allocation / 100) * portfolio.total_value
                    current_value = asset.market_value
                    adjustment_needed = target_value - current_value
                    
                    suggestions.append({
                        'symbol': asset.symbol,
                        'current_allocation': asset.current_allocation,
                        'target_allocation': asset.target_allocation,
                        'deviation': deviation,
                        'current_value': current_value,
                        'target_value': target_value,
                        'adjustment_needed': adjustment_needed,
                        'action': 'buy' if adjustment_needed > 0 else 'sell',
                        'shares_to_trade': abs(adjustment_needed / asset.current_price) if asset.current_price > 0 else 0
                    })
                
                total_deviation += abs_deviation
        
        needs_rebalancing = total_deviation > portfolio.rebalance_threshold
        
        return {
            'needs_rebalancing': needs_rebalancing,
            'total_deviation': total_deviation,
            'threshold': portfolio.rebalance_threshold,
            'suggestions': suggestions,
            'estimated_cost': self._estimate_rebalancing_cost(suggestions)
        }
    
    def _estimate_rebalancing_cost(self, suggestions: List[Dict[str, Any]]) -> float:
        """
        Estimate the cost of rebalancing (simplified)
        """
        # Simplified cost calculation - in practice you'd include:
        # - Trading fees
        # - Bid-ask spreads
        # - Market impact
        total_trade_value = sum(abs(s['adjustment_needed']) for s in suggestions)
        estimated_fee_rate = 0.001  # 0.1% fee estimate
        return total_trade_value * estimated_fee_rate
    
    async def get_portfolio_performance_history(
        self, 
        db: Session, 
        portfolio_id: int, 
        days: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Get portfolio performance history (simplified version)
        """
        # In a full implementation, you would store daily portfolio values
        # For now, return current snapshot
        portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
        if not portfolio:
            return []
        
        # This is a placeholder - in practice you'd have historical data
        return [{
            'date': datetime.utcnow().isoformat(),
            'total_value': portfolio.total_value,
            'return': portfolio.total_return,
            'return_percentage': portfolio.total_return_percentage
        }]