"""
Technical analysis based investment strategies
"""

from typing import Dict, List, Any
import pandas as pd
import numpy as np

from .base_strategy import BaseStrategy, TradingSignal, SignalType


class MovingAverageStrategy(BaseStrategy):
    """
    Simple Moving Average Crossover Strategy
    Generates buy signals when short MA crosses above long MA
    Generates sell signals when short MA crosses below long MA
    """
    
    def __init__(self, parameters: Dict[str, Any] = None):
        default_params = {
            'short_window': 20,
            'long_window': 50,
            'min_data_points': 60
        }
        if parameters:
            default_params.update(parameters)
        
        super().__init__("Moving Average Crossover", default_params)
    
    def get_required_indicators(self) -> List[str]:
        return [f'SMA_{self.parameters["short_window"]}', f'SMA_{self.parameters["long_window"]}']
    
    def generate_signals(self, data: pd.DataFrame, symbol: str) -> List[TradingSignal]:
        """Generate signals based on moving average crossover"""
        if not self.validate_data(data):
            return []
        
        signals = []
        short_ma = f'SMA_{self.parameters["short_window"]}'
        long_ma = f'SMA_{self.parameters["long_window"]}'
        
        # Calculate crossovers
        data['MA_Signal'] = 0
        data['MA_Signal'][self.parameters['short_window']:] = np.where(
            data[short_ma][self.parameters['short_window']:] > data[long_ma][self.parameters['short_window']:], 1, 0
        )
        data['MA_Position'] = data['MA_Signal'].diff()
        
        # Generate signals
        for idx in data.index:
            if pd.isna(data.loc[idx, 'MA_Position']):
                continue
                
            current_price = data.loc[idx, 'Close']
            
            if data.loc[idx, 'MA_Position'] == 1:  # Buy signal
                confidence = self._calculate_confidence(data, idx, 'buy')
                signal = TradingSignal(
                    symbol=symbol,
                    signal=SignalType.BUY,
                    confidence=confidence,
                    price=current_price,
                    timestamp=data.index[idx] if hasattr(data.index[idx], 'to_pydatetime') else None,
                    reason=f"Short MA ({short_ma}) crossed above Long MA ({long_ma})",
                    metadata={
                        'short_ma_value': data.loc[idx, short_ma],
                        'long_ma_value': data.loc[idx, long_ma]
                    }
                )
                signals.append(signal)
                
            elif data.loc[idx, 'MA_Position'] == -1:  # Sell signal
                confidence = self._calculate_confidence(data, idx, 'sell')
                signal = TradingSignal(
                    symbol=symbol,
                    signal=SignalType.SELL,
                    confidence=confidence,
                    price=current_price,
                    timestamp=data.index[idx] if hasattr(data.index[idx], 'to_pydatetime') else None,
                    reason=f"Short MA ({short_ma}) crossed below Long MA ({long_ma})",
                    metadata={
                        'short_ma_value': data.loc[idx, short_ma],
                        'long_ma_value': data.loc[idx, long_ma]
                    }
                )
                signals.append(signal)
        
        return signals
    
    def _calculate_confidence(self, data: pd.DataFrame, idx: int, signal_type: str) -> float:
        """Calculate confidence based on volume and price momentum"""
        try:
            # Volume confirmation
            avg_volume = data['Volume'].rolling(20).mean().loc[idx]
            current_volume = data.loc[idx, 'Volume']
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1.0
            
            # Price momentum
            price_change = (data.loc[idx, 'Close'] - data.loc[idx-5, 'Close']) / data.loc[idx-5, 'Close']
            
            # Base confidence
            confidence = 0.6
            
            # Adjust for volume (higher volume = higher confidence)
            if volume_ratio > 1.5:
                confidence += 0.2
            elif volume_ratio > 1.2:
                confidence += 0.1
            
            # Adjust for momentum alignment
            if signal_type == 'buy' and price_change > 0:
                confidence += 0.1
            elif signal_type == 'sell' and price_change < 0:
                confidence += 0.1
            
            return min(confidence, 1.0)
        except:
            return 0.6


class RSIStrategy(BaseStrategy):
    """
    RSI (Relative Strength Index) Strategy
    Generates buy signals when RSI is oversold (< 30)
    Generates sell signals when RSI is overbought (> 70)
    """
    
    def __init__(self, parameters: Dict[str, Any] = None):
        default_params = {
            'rsi_period': 14,
            'oversold_threshold': 30,
            'overbought_threshold': 70,
            'min_data_points': 50
        }
        if parameters:
            default_params.update(parameters)
        
        super().__init__("RSI Strategy", default_params)
    
    def get_required_indicators(self) -> List[str]:
        return ['RSI']
    
    def generate_signals(self, data: pd.DataFrame, symbol: str) -> List[TradingSignal]:
        """Generate signals based on RSI levels"""
        if not self.validate_data(data):
            return []
        
        signals = []
        oversold = self.parameters['oversold_threshold']
        overbought = self.parameters['overbought_threshold']
        
        for i in range(1, len(data)):
            current_rsi = data.iloc[i]['RSI']
            previous_rsi = data.iloc[i-1]['RSI']
            current_price = data.iloc[i]['Close']
            
            # Buy signal: RSI crosses above oversold level
            if previous_rsi <= oversold and current_rsi > oversold:
                confidence = self._calculate_rsi_confidence(current_rsi, 'buy')
                signal = TradingSignal(
                    symbol=symbol,
                    signal=SignalType.BUY,
                    confidence=confidence,
                    price=current_price,
                    timestamp=data.index[i] if hasattr(data.index[i], 'to_pydatetime') else None,
                    reason=f"RSI crossed above oversold level ({oversold})",
                    metadata={'rsi_value': current_rsi}
                )
                signals.append(signal)
            
            # Sell signal: RSI crosses below overbought level
            elif previous_rsi >= overbought and current_rsi < overbought:
                confidence = self._calculate_rsi_confidence(current_rsi, 'sell')
                signal = TradingSignal(
                    symbol=symbol,
                    signal=SignalType.SELL,
                    confidence=confidence,
                    price=current_price,
                    timestamp=data.index[i] if hasattr(data.index[i], 'to_pydatetime') else None,
                    reason=f"RSI crossed below overbought level ({overbought})",
                    metadata={'rsi_value': current_rsi}
                )
                signals.append(signal)
        
        return signals
    
    def _calculate_rsi_confidence(self, rsi_value: float, signal_type: str) -> float:
        """Calculate confidence based on how extreme the RSI value is"""
        if signal_type == 'buy':
            # More oversold = higher confidence
            if rsi_value < 20:
                return 0.9
            elif rsi_value < 25:
                return 0.8
            else:
                return 0.6
        else:  # sell
            # More overbought = higher confidence
            if rsi_value > 80:
                return 0.9
            elif rsi_value > 75:
                return 0.8
            else:
                return 0.6


class MACDStrategy(BaseStrategy):
    """
    MACD (Moving Average Convergence Divergence) Strategy
    Generates buy signals when MACD line crosses above signal line
    Generates sell signals when MACD line crosses below signal line
    """
    
    def __init__(self, parameters: Dict[str, Any] = None):
        default_params = {
            'fast_period': 12,
            'slow_period': 26,
            'signal_period': 9,
            'min_data_points': 50
        }
        if parameters:
            default_params.update(parameters)
        
        super().__init__("MACD Strategy", default_params)
    
    def get_required_indicators(self) -> List[str]:
        return ['MACD', 'MACD_Signal', 'MACD_Histogram']
    
    def generate_signals(self, data: pd.DataFrame, symbol: str) -> List[TradingSignal]:
        """Generate signals based on MACD crossovers"""
        if not self.validate_data(data):
            return []
        
        signals = []
        
        for i in range(1, len(data)):
            current_macd = data.iloc[i]['MACD']
            current_signal = data.iloc[i]['MACD_Signal']
            previous_macd = data.iloc[i-1]['MACD']
            previous_signal = data.iloc[i-1]['MACD_Signal']
            current_price = data.iloc[i]['Close']
            
            # Buy signal: MACD crosses above signal line
            if previous_macd <= previous_signal and current_macd > current_signal:
                confidence = self._calculate_macd_confidence(data, i, 'buy')
                signal = TradingSignal(
                    symbol=symbol,
                    signal=SignalType.BUY,
                    confidence=confidence,
                    price=current_price,
                    timestamp=data.index[i] if hasattr(data.index[i], 'to_pydatetime') else None,
                    reason="MACD crossed above signal line",
                    metadata={
                        'macd_value': current_macd,
                        'signal_value': current_signal,
                        'histogram': data.iloc[i]['MACD_Histogram']
                    }
                )
                signals.append(signal)
            
            # Sell signal: MACD crosses below signal line
            elif previous_macd >= previous_signal and current_macd < current_signal:
                confidence = self._calculate_macd_confidence(data, i, 'sell')
                signal = TradingSignal(
                    symbol=symbol,
                    signal=SignalType.SELL,
                    confidence=confidence,
                    price=current_price,
                    timestamp=data.index[i] if hasattr(data.index[i], 'to_pydatetime') else None,
                    reason="MACD crossed below signal line",
                    metadata={
                        'macd_value': current_macd,
                        'signal_value': current_signal,
                        'histogram': data.iloc[i]['MACD_Histogram']
                    }
                )
                signals.append(signal)
        
        return signals
    
    def _calculate_macd_confidence(self, data: pd.DataFrame, idx: int, signal_type: str) -> float:
        """Calculate confidence based on MACD histogram and trend strength"""
        try:
            histogram = data.iloc[idx]['MACD_Histogram']
            
            # Base confidence
            confidence = 0.6
            
            # Stronger histogram = higher confidence
            abs_histogram = abs(histogram)
            if abs_histogram > 0.5:
                confidence += 0.2
            elif abs_histogram > 0.2:
                confidence += 0.1
            
            # Check if MACD is above/below zero line for additional confirmation
            macd_value = data.iloc[idx]['MACD']
            if signal_type == 'buy' and macd_value > 0:
                confidence += 0.1
            elif signal_type == 'sell' and macd_value < 0:
                confidence += 0.1
            
            return min(confidence, 1.0)
        except:
            return 0.6