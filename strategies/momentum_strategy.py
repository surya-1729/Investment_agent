"""
Momentum-based investment strategy
"""

from typing import Dict, List, Any
import pandas as pd
import numpy as np

from .base_strategy import BaseStrategy, TradingSignal, SignalType


class MomentumStrategy(BaseStrategy):
    """
    Momentum Strategy based on price and volume momentum
    Buys stocks showing strong upward momentum
    Sells stocks showing strong downward momentum
    """
    
    def __init__(self, parameters: Dict[str, Any] = None):
        default_params = {
            'lookback_period': 20,
            'momentum_threshold': 0.05,  # 5% momentum threshold
            'volume_confirmation': True,
            'min_data_points': 30
        }
        if parameters:
            default_params.update(parameters)
        
        super().__init__("Momentum Strategy", default_params)
    
    def get_required_indicators(self) -> List[str]:
        return ['Volume_SMA']  # We'll calculate momentum internally
    
    def generate_signals(self, data: pd.DataFrame, symbol: str) -> List[TradingSignal]:
        """Generate signals based on price and volume momentum"""
        if not self.validate_data(data):
            return []
        
        # Calculate momentum indicators
        data = self._calculate_momentum_indicators(data)
        
        signals = []
        lookback = self.parameters['lookback_period']
        threshold = self.parameters['momentum_threshold']
        
        for i in range(lookback, len(data)):
            current_price = data.iloc[i]['Close']
            price_momentum = data.iloc[i]['Price_Momentum']
            volume_momentum = data.iloc[i]['Volume_Momentum']
            
            # Buy signal: Strong positive momentum
            if price_momentum > threshold:
                confidence = self._calculate_momentum_confidence(data, i, 'buy')
                
                # Volume confirmation if enabled
                if self.parameters['volume_confirmation'] and volume_momentum <= 1.0:
                    confidence *= 0.7  # Reduce confidence without volume confirmation
                
                signal = TradingSignal(
                    symbol=symbol,
                    signal=SignalType.BUY,
                    confidence=confidence,
                    price=current_price,
                    timestamp=data.index[i] if hasattr(data.index[i], 'to_pydatetime') else None,
                    reason=f"Strong positive momentum ({price_momentum:.2%})",
                    metadata={
                        'price_momentum': price_momentum,
                        'volume_momentum': volume_momentum,
                        'momentum_strength': self._get_momentum_strength(price_momentum)
                    }
                )
                signals.append(signal)
            
            # Sell signal: Strong negative momentum
            elif price_momentum < -threshold:
                confidence = self._calculate_momentum_confidence(data, i, 'sell')
                
                # Volume confirmation if enabled
                if self.parameters['volume_confirmation'] and volume_momentum <= 1.0:
                    confidence *= 0.7  # Reduce confidence without volume confirmation
                
                signal = TradingSignal(
                    symbol=symbol,
                    signal=SignalType.SELL,
                    confidence=confidence,
                    price=current_price,
                    timestamp=data.index[i] if hasattr(data.index[i], 'to_pydatetime') else None,
                    reason=f"Strong negative momentum ({price_momentum:.2%})",
                    metadata={
                        'price_momentum': price_momentum,
                        'volume_momentum': volume_momentum,
                        'momentum_strength': self._get_momentum_strength(abs(price_momentum))
                    }
                )
                signals.append(signal)
        
        return signals
    
    def _calculate_momentum_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate momentum indicators"""
        lookback = self.parameters['lookback_period']
        
        # Price momentum (rate of change)
        data['Price_Momentum'] = data['Close'].pct_change(periods=lookback)
        
        # Volume momentum (current volume vs average)
        data['Volume_Momentum'] = data['Volume'] / data['Volume_SMA']
        
        # Price velocity (acceleration)
        data['Price_Velocity'] = data['Close'].diff().rolling(window=5).mean()
        
        # Relative strength vs market (if available)
        # This would require market index data - simplified for now
        data['Relative_Strength'] = data['Price_Momentum']  # Placeholder
        
        return data
    
    def _calculate_momentum_confidence(self, data: pd.DataFrame, idx: int, signal_type: str) -> float:
        """Calculate confidence based on momentum strength and consistency"""
        try:
            price_momentum = abs(data.iloc[idx]['Price_Momentum'])
            volume_momentum = data.iloc[idx]['Volume_Momentum']
            
            # Base confidence based on momentum strength
            if price_momentum > 0.15:  # 15%+ momentum
                confidence = 0.9
            elif price_momentum > 0.10:  # 10%+ momentum
                confidence = 0.8
            elif price_momentum > 0.07:  # 7%+ momentum
                confidence = 0.7
            else:
                confidence = 0.6
            
            # Adjust for volume confirmation
            if volume_momentum > 1.5:
                confidence += 0.1
            elif volume_momentum < 0.8:
                confidence -= 0.1
            
            # Check momentum consistency over last few periods
            consistency_score = self._check_momentum_consistency(data, idx)
            confidence += consistency_score * 0.1
            
            return min(max(confidence, 0.1), 1.0)
        except:
            return 0.6
    
    def _check_momentum_consistency(self, data: pd.DataFrame, idx: int) -> float:
        """Check how consistent the momentum has been over recent periods"""
        try:
            # Look at last 5 periods
            recent_momentum = []
            for i in range(max(0, idx-4), idx+1):
                if i < len(data):
                    momentum = data.iloc[i]['Price_Momentum']
                    if not pd.isna(momentum):
                        recent_momentum.append(momentum)
            
            if len(recent_momentum) < 3:
                return 0.0
            
            # Calculate consistency (lower standard deviation = more consistent)
            std_dev = np.std(recent_momentum)
            mean_momentum = np.mean(recent_momentum)
            
            if std_dev == 0:
                return 1.0  # Perfect consistency
            
            # Normalize consistency score (0 to 1)
            consistency = max(0, 1 - (std_dev / abs(mean_momentum)))
            return min(consistency, 1.0)
        except:
            return 0.0
    
    def _get_momentum_strength(self, momentum: float) -> str:
        """Classify momentum strength"""
        if momentum > 0.20:
            return "Very Strong"
        elif momentum > 0.15:
            return "Strong"
        elif momentum > 0.10:
            return "Moderate"
        elif momentum > 0.05:
            return "Weak"
        else:
            return "Very Weak"