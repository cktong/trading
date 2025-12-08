"""
Cryptocurrency Backtesting Engine with Futures Support
================================================
A comprehensive backtesting framework for cryptocurrency trading strategies
supporting both spot and futures (short) positions.

Author: AI Assistant
Date: 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class CryptoBacktester:
    """
    Main backtesting engine for cryptocurrency trading strategies.
    Supports both spot (long) and futures (short) positions.
    """
    
    def __init__(self, asset_symbol: str = "BTC", initial_capital: float = 10000.0, 
                 commission: float = None):
        """
        Initialize the backtester.
        
        Args:
            asset_symbol: Cryptocurrency symbol (e.g., "BTC", "ETH", "SPDR", "GLAM")
            initial_capital: Starting capital in USD
            commission: Trading commission rate (0.001 = 0.1%). If None, uses asset default.
        """
        self.asset_symbol = asset_symbol.upper()
        self.initial_capital = initial_capital
        
        # Get asset configuration
        try:
            import sys
            sys.path.insert(0, '/home/user/webapp')
            from config.assets import get_asset_config, get_asset_name
            self.asset_config = get_asset_config(self.asset_symbol)
            self.asset_name = get_asset_name(self.asset_symbol)
        except:
            self.asset_config = {'default_commission': 0.001}
            self.asset_name = self.asset_symbol
        
        # Set commission
        self.commission = commission if commission is not None else self.asset_config.get('default_commission', 0.001)
        
        self.trades = []
        self.portfolio_history = []
        self.positions = []  # Current open positions
        
    def load_data(self, data: pd.DataFrame = None, days: int = 365, 
                  coin: str = "BTC", interval: str = "1d", 
                  use_real_data: bool = True) -> pd.DataFrame:
        """
        Load Bitcoin price data. Automatically fetches real Hyperliquid data by default.
        
        Args:
            data: DataFrame with columns ['timestamp', 'open', 'high', 'low', 'close', 'volume']
            days: Number of days to fetch/generate
            coin: Trading pair for Hyperliquid (default: "BTC")
            interval: Candle interval (default: "1d" for daily)
            use_real_data: If True, fetch real Hyperliquid data (default: True)
            
        Returns:
            DataFrame with OHLCV data
        """
        if data is not None:
            self.data = data.copy()
            self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
        elif use_real_data:
            # Try to fetch real Hyperliquid data
            try:
                from hyperliquid_data_fetcher import HyperliquidDataFetcher
                
                print(f"📡 Fetching real {coin} data from Hyperliquid...")
                fetcher = HyperliquidDataFetcher()
                self.data = fetcher.fetch_bitcoin_for_backtest(
                    interval=interval, 
                    days_back=days
                )
                
                if self.data.empty:
                    print("⚠️  Failed to fetch Hyperliquid data, using synthetic data instead...")
                    self.data = self._generate_synthetic_data(days)
                else:
                    print(f"✅ Using real Hyperliquid data ({len(self.data)} candles)")
                    
            except ImportError:
                print("⚠️  hyperliquid_data_fetcher not found, using synthetic data...")
                self.data = self._generate_synthetic_data(days)
            except Exception as e:
                print(f"⚠️  Error fetching Hyperliquid data: {e}")
                print("    Using synthetic data instead...")
                self.data = self._generate_synthetic_data(days)
        else:
            # Generate synthetic data if explicitly requested
            print("🎲 Using synthetic data (for testing)...")
            self.data = self._generate_synthetic_data(days)
            
        self.data = self.data.sort_values('timestamp').reset_index(drop=True)
        return self.data
    
    def _generate_synthetic_data(self, days: int) -> pd.DataFrame:
        """Generate synthetic Bitcoin price data for testing."""
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        
        # Start from a realistic Bitcoin price
        base_price = 40000
        returns = np.random.normal(0.001, 0.03, days)  # 0.1% daily return, 3% volatility
        prices = base_price * np.exp(np.cumsum(returns))
        
        # Create OHLCV data
        return pd.DataFrame({
            'timestamp': dates,
            'open': prices * (1 + np.random.uniform(-0.01, 0.01, days)),
            'high': prices * (1 + np.random.uniform(0.005, 0.02, days)),
            'low': prices * (1 + np.random.uniform(-0.02, -0.005, days)),
            'close': prices,
            'volume': np.random.uniform(1000, 10000, days)
        })
    
    def calculate_indicators(self):
        """Calculate technical indicators for the loaded data."""
        df = self.data
        
        # Simple Moving Averages
        df['sma_20'] = df['close'].rolling(window=20).mean()
        df['sma_50'] = df['close'].rolling(window=50).mean()
        df['sma_200'] = df['close'].rolling(window=200).mean()
        
        # Exponential Moving Averages
        df['ema_12'] = df['close'].ewm(span=12, adjust=False).mean()
        df['ema_26'] = df['close'].ewm(span=26, adjust=False).mean()
        
        # MACD
        df['macd'] = df['ema_12'] - df['ema_26']
        df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
        df['macd_hist'] = df['macd'] - df['macd_signal']
        
        # RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # Bollinger Bands
        df['bb_middle'] = df['close'].rolling(window=20).mean()
        bb_std = df['close'].rolling(window=20).std()
        df['bb_upper'] = df['bb_middle'] + (bb_std * 2)
        df['bb_lower'] = df['bb_middle'] - (bb_std * 2)
        
        # ATR (Average True Range)
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        df['atr'] = true_range.rolling(14).mean()
        
        self.data = df
        return df
    
    def execute_trade(self, idx: int, action: str, price: float, quantity: float, 
                     position_type: str = 'spot'):
        """
        Execute a trade (buy/sell/short/cover).
        
        Args:
            idx: Index in the dataframe
            action: 'buy', 'sell', 'short', or 'cover'
            price: Execution price
            quantity: Number of units of the cryptocurrency
            position_type: 'spot' for long positions, 'futures' for short positions
        """
        commission_cost = price * quantity * self.commission
        
        trade = {
            'timestamp': self.data.iloc[idx]['timestamp'],
            'action': action,
            'price': price,
            'quantity': quantity,
            'position_type': position_type,
            'commission': commission_cost,
            'total_cost': price * quantity + commission_cost if action in ['buy', 'short'] 
                         else price * quantity - commission_cost
        }
        
        self.trades.append(trade)
        
    def run_strategy(self, strategy_name: str = 'sma_crossover', **kwargs):
        """
        Run a backtesting strategy.
        
        Args:
            strategy_name: Name of strategy to run
            **kwargs: Strategy-specific parameters
        """
        self.trades = []
        self.positions = []
        
        if strategy_name == 'sma_crossover':
            self._strategy_sma_crossover(**kwargs)
        elif strategy_name == 'rsi_mean_reversion':
            self._strategy_rsi_mean_reversion(**kwargs)
        elif strategy_name == 'macd_momentum':
            self._strategy_macd_momentum(**kwargs)
        elif strategy_name == 'bollinger_bands':
            self._strategy_bollinger_bands(**kwargs)
        elif strategy_name == 'dual_momentum':
            self._strategy_dual_momentum(**kwargs)
        else:
            raise ValueError(f"Unknown strategy: {strategy_name}")
        
        return self.calculate_performance()
    
    def _strategy_sma_crossover(self, fast_period: int = 20, slow_period: int = 50,
                               allow_short: bool = True):
        """
        Simple Moving Average Crossover Strategy.
        Buy when fast SMA crosses above slow SMA.
        Sell/Short when fast SMA crosses below slow SMA.
        """
        df = self.data
        position = None  # None, 'long', or 'short'
        position_size = 0
        capital = self.initial_capital
        
        for i in range(max(fast_period, slow_period) + 1, len(df)):
            current_price = df.iloc[i]['close']
            fast_sma = df.iloc[i]['sma_20'] if fast_period == 20 else df.iloc[i]['sma_50']
            slow_sma = df.iloc[i]['sma_50'] if slow_period == 50 else df.iloc[i]['sma_200']
            
            prev_fast = df.iloc[i-1]['sma_20'] if fast_period == 20 else df.iloc[i-1]['sma_50']
            prev_slow = df.iloc[i-1]['sma_50'] if slow_period == 50 else df.iloc[i-1]['sma_200']
            
            if pd.isna(fast_sma) or pd.isna(slow_sma):
                continue
            
            # Buy signal (golden cross)
            if prev_fast <= prev_slow and fast_sma > slow_sma:
                if position == 'short':
                    # Cover short position
                    profit = (position_size * self.positions[-1]['entry_price']) - (position_size * current_price)
                    capital += profit
                    self.execute_trade(i, 'cover', current_price, position_size, 'futures')
                    self.positions[-1]['exit_price'] = current_price
                    self.positions[-1]['exit_idx'] = i
                    position = None
                    position_size = 0
                
                if position is None:
                    # Open long position
                    position_size = (capital * 0.95) / current_price  # Use 95% of capital
                    self.execute_trade(i, 'buy', current_price, position_size, 'spot')
                    self.positions.append({
                        'type': 'long',
                        'entry_idx': i,
                        'entry_price': current_price,
                        'size': position_size
                    })
                    position = 'long'
            
            # Sell signal (death cross)
            elif prev_fast >= prev_slow and fast_sma < slow_sma:
                if position == 'long':
                    # Close long position
                    profit = (position_size * current_price) - (position_size * self.positions[-1]['entry_price'])
                    capital += profit
                    self.execute_trade(i, 'sell', current_price, position_size, 'spot')
                    self.positions[-1]['exit_price'] = current_price
                    self.positions[-1]['exit_idx'] = i
                    position = None
                    position_size = 0
                
                if position is None and allow_short:
                    # Open short position
                    position_size = (capital * 0.95) / current_price
                    self.execute_trade(i, 'short', current_price, position_size, 'futures')
                    self.positions.append({
                        'type': 'short',
                        'entry_idx': i,
                        'entry_price': current_price,
                        'size': position_size
                    })
                    position = 'short'
        
        # Close any remaining position at the end
        if position is not None:
            final_price = df.iloc[-1]['close']
            if position == 'long':
                self.execute_trade(len(df)-1, 'sell', final_price, position_size, 'spot')
            else:
                self.execute_trade(len(df)-1, 'cover', final_price, position_size, 'futures')
            self.positions[-1]['exit_price'] = final_price
            self.positions[-1]['exit_idx'] = len(df)-1
    
    def _strategy_rsi_mean_reversion(self, oversold: int = 30, overbought: int = 70,
                                    allow_short: bool = True):
        """
        RSI Mean Reversion Strategy.
        Buy when RSI < oversold threshold.
        Sell/Short when RSI > overbought threshold.
        """
        df = self.data
        position = None
        position_size = 0
        capital = self.initial_capital
        
        for i in range(15, len(df)):
            current_price = df.iloc[i]['close']
            rsi = df.iloc[i]['rsi']
            
            if pd.isna(rsi):
                continue
            
            # Buy signal (oversold)
            if rsi < oversold and position is None:
                position_size = (capital * 0.95) / current_price
                self.execute_trade(i, 'buy', current_price, position_size, 'spot')
                self.positions.append({
                    'type': 'long',
                    'entry_idx': i,
                    'entry_price': current_price,
                    'size': position_size
                })
                position = 'long'
            
            # Sell signal (overbought)
            elif rsi > overbought:
                if position == 'long':
                    profit = (position_size * current_price) - (position_size * self.positions[-1]['entry_price'])
                    capital += profit
                    self.execute_trade(i, 'sell', current_price, position_size, 'spot')
                    self.positions[-1]['exit_price'] = current_price
                    self.positions[-1]['exit_idx'] = i
                    position = None
                    position_size = 0
                
                if allow_short and position is None:
                    position_size = (capital * 0.95) / current_price
                    self.execute_trade(i, 'short', current_price, position_size, 'futures')
                    self.positions.append({
                        'type': 'short',
                        'entry_idx': i,
                        'entry_price': current_price,
                        'size': position_size
                    })
                    position = 'short'
            
            # Cover short when RSI normalizes
            elif position == 'short' and rsi < 50:
                profit = (position_size * self.positions[-1]['entry_price']) - (position_size * current_price)
                capital += profit
                self.execute_trade(i, 'cover', current_price, position_size, 'futures')
                self.positions[-1]['exit_price'] = current_price
                self.positions[-1]['exit_idx'] = i
                position = None
                position_size = 0
        
        # Close remaining position
        if position is not None:
            final_price = df.iloc[-1]['close']
            if position == 'long':
                self.execute_trade(len(df)-1, 'sell', final_price, position_size, 'spot')
            else:
                self.execute_trade(len(df)-1, 'cover', final_price, position_size, 'futures')
            self.positions[-1]['exit_price'] = final_price
            self.positions[-1]['exit_idx'] = len(df)-1
    
    def _strategy_macd_momentum(self, allow_short: bool = True):
        """
        MACD Momentum Strategy.
        Buy when MACD crosses above signal line.
        Sell/Short when MACD crosses below signal line.
        """
        df = self.data
        position = None
        position_size = 0
        capital = self.initial_capital
        
        for i in range(35, len(df)):
            current_price = df.iloc[i]['close']
            macd = df.iloc[i]['macd']
            macd_signal = df.iloc[i]['macd_signal']
            prev_macd = df.iloc[i-1]['macd']
            prev_signal = df.iloc[i-1]['macd_signal']
            
            if pd.isna(macd) or pd.isna(macd_signal):
                continue
            
            # Buy signal
            if prev_macd <= prev_signal and macd > macd_signal:
                if position == 'short':
                    profit = (position_size * self.positions[-1]['entry_price']) - (position_size * current_price)
                    capital += profit
                    self.execute_trade(i, 'cover', current_price, position_size, 'futures')
                    self.positions[-1]['exit_price'] = current_price
                    self.positions[-1]['exit_idx'] = i
                    position = None
                    position_size = 0
                
                if position is None:
                    position_size = (capital * 0.95) / current_price
                    self.execute_trade(i, 'buy', current_price, position_size, 'spot')
                    self.positions.append({
                        'type': 'long',
                        'entry_idx': i,
                        'entry_price': current_price,
                        'size': position_size
                    })
                    position = 'long'
            
            # Sell signal
            elif prev_macd >= prev_signal and macd < macd_signal:
                if position == 'long':
                    profit = (position_size * current_price) - (position_size * self.positions[-1]['entry_price'])
                    capital += profit
                    self.execute_trade(i, 'sell', current_price, position_size, 'spot')
                    self.positions[-1]['exit_price'] = current_price
                    self.positions[-1]['exit_idx'] = i
                    position = None
                    position_size = 0
                
                if position is None and allow_short:
                    position_size = (capital * 0.95) / current_price
                    self.execute_trade(i, 'short', current_price, position_size, 'futures')
                    self.positions.append({
                        'type': 'short',
                        'entry_idx': i,
                        'entry_price': current_price,
                        'size': position_size
                    })
                    position = 'short'
        
        if position is not None:
            final_price = df.iloc[-1]['close']
            if position == 'long':
                self.execute_trade(len(df)-1, 'sell', final_price, position_size, 'spot')
            else:
                self.execute_trade(len(df)-1, 'cover', final_price, position_size, 'futures')
            self.positions[-1]['exit_price'] = final_price
            self.positions[-1]['exit_idx'] = len(df)-1
    
    def _strategy_bollinger_bands(self, allow_short: bool = True):
        """
        Bollinger Bands Strategy.
        Buy when price touches lower band.
        Sell/Short when price touches upper band.
        """
        df = self.data
        position = None
        position_size = 0
        capital = self.initial_capital
        
        for i in range(21, len(df)):
            current_price = df.iloc[i]['close']
            bb_upper = df.iloc[i]['bb_upper']
            bb_lower = df.iloc[i]['bb_lower']
            bb_middle = df.iloc[i]['bb_middle']
            
            if pd.isna(bb_upper) or pd.isna(bb_lower):
                continue
            
            # Buy signal (price near lower band)
            if current_price <= bb_lower and position is None:
                position_size = (capital * 0.95) / current_price
                self.execute_trade(i, 'buy', current_price, position_size, 'spot')
                self.positions.append({
                    'type': 'long',
                    'entry_idx': i,
                    'entry_price': current_price,
                    'size': position_size
                })
                position = 'long'
            
            # Sell signal (price near upper band)
            elif current_price >= bb_upper:
                if position == 'long':
                    profit = (position_size * current_price) - (position_size * self.positions[-1]['entry_price'])
                    capital += profit
                    self.execute_trade(i, 'sell', current_price, position_size, 'spot')
                    self.positions[-1]['exit_price'] = current_price
                    self.positions[-1]['exit_idx'] = i
                    position = None
                    position_size = 0
                
                if allow_short and position is None:
                    position_size = (capital * 0.95) / current_price
                    self.execute_trade(i, 'short', current_price, position_size, 'futures')
                    self.positions.append({
                        'type': 'short',
                        'entry_idx': i,
                        'entry_price': current_price,
                        'size': position_size
                    })
                    position = 'short'
            
            # Cover short when price returns to middle band
            elif position == 'short' and current_price <= bb_middle:
                profit = (position_size * self.positions[-1]['entry_price']) - (position_size * current_price)
                capital += profit
                self.execute_trade(i, 'cover', current_price, position_size, 'futures')
                self.positions[-1]['exit_price'] = current_price
                self.positions[-1]['exit_idx'] = i
                position = None
                position_size = 0
        
        if position is not None:
            final_price = df.iloc[-1]['close']
            if position == 'long':
                self.execute_trade(len(df)-1, 'sell', final_price, position_size, 'spot')
            else:
                self.execute_trade(len(df)-1, 'cover', final_price, position_size, 'futures')
            self.positions[-1]['exit_price'] = final_price
            self.positions[-1]['exit_idx'] = len(df)-1
    
    def _strategy_dual_momentum(self, allow_short: bool = True):
        """
        Dual Momentum Strategy combining trend and mean reversion.
        Uses both SMA trend and RSI for confirmation.
        """
        df = self.data
        position = None
        position_size = 0
        capital = self.initial_capital
        
        for i in range(51, len(df)):
            current_price = df.iloc[i]['close']
            sma_20 = df.iloc[i]['sma_20']
            sma_50 = df.iloc[i]['sma_50']
            rsi = df.iloc[i]['rsi']
            
            if pd.isna(sma_20) or pd.isna(sma_50) or pd.isna(rsi):
                continue
            
            # Strong buy signal (uptrend + oversold)
            if current_price > sma_20 > sma_50 and rsi < 40 and position is None:
                position_size = (capital * 0.95) / current_price
                self.execute_trade(i, 'buy', current_price, position_size, 'spot')
                self.positions.append({
                    'type': 'long',
                    'entry_idx': i,
                    'entry_price': current_price,
                    'size': position_size
                })
                position = 'long'
            
            # Strong sell signal (downtrend + overbought)
            elif current_price < sma_20 < sma_50 and rsi > 60:
                if position == 'long':
                    profit = (position_size * current_price) - (position_size * self.positions[-1]['entry_price'])
                    capital += profit
                    self.execute_trade(i, 'sell', current_price, position_size, 'spot')
                    self.positions[-1]['exit_price'] = current_price
                    self.positions[-1]['exit_idx'] = i
                    position = None
                    position_size = 0
                
                if allow_short and position is None and rsi > 70:
                    position_size = (capital * 0.95) / current_price
                    self.execute_trade(i, 'short', current_price, position_size, 'futures')
                    self.positions.append({
                        'type': 'short',
                        'entry_idx': i,
                        'entry_price': current_price,
                        'size': position_size
                    })
                    position = 'short'
            
            # Exit short on trend reversal
            elif position == 'short' and (current_price > sma_20 or rsi < 45):
                profit = (position_size * self.positions[-1]['entry_price']) - (position_size * current_price)
                capital += profit
                self.execute_trade(i, 'cover', current_price, position_size, 'futures')
                self.positions[-1]['exit_price'] = current_price
                self.positions[-1]['exit_idx'] = i
                position = None
                position_size = 0
        
        if position is not None:
            final_price = df.iloc[-1]['close']
            if position == 'long':
                self.execute_trade(len(df)-1, 'sell', final_price, position_size, 'spot')
            else:
                self.execute_trade(len(df)-1, 'cover', final_price, position_size, 'futures')
            self.positions[-1]['exit_price'] = final_price
            self.positions[-1]['exit_idx'] = len(df)-1
    
    def calculate_performance(self) -> Dict:
        """Calculate comprehensive performance metrics."""
        if not self.trades or not self.positions:
            return {
                'initial_capital': self.initial_capital,
                'final_capital': self.initial_capital,
                'total_pnl': 0,
                'total_return': 0,
                'total_trades': 0,
                'long_trades': 0,
                'short_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0,
                'profit_factor': 0,
                'avg_trade': 0,
                'avg_win': 0,
                'avg_loss': 0,
                'max_drawdown': 0,
                'sharpe_ratio': 0,
                'total_commission': 0
            }
        
        # Calculate P&L for each closed position
        pnl_list = []
        for pos in self.positions:
            if 'exit_price' in pos:
                if pos['type'] == 'long':
                    pnl = (pos['exit_price'] - pos['entry_price']) * pos['size']
                else:  # short
                    pnl = (pos['entry_price'] - pos['exit_price']) * pos['size']
                
                # Subtract commissions
                commission_cost = (pos['entry_price'] + pos['exit_price']) * pos['size'] * self.commission
                pnl -= commission_cost
                pnl_list.append(pnl)
        
        total_pnl = sum(pnl_list)
        final_capital = self.initial_capital + total_pnl
        total_return = (final_capital - self.initial_capital) / self.initial_capital * 100
        
        # Win rate
        winning_trades = [p for p in pnl_list if p > 0]
        losing_trades = [p for p in pnl_list if p <= 0]
        win_rate = len(winning_trades) / len(pnl_list) * 100 if pnl_list else 0
        
        # Profit factor
        gross_profit = sum(winning_trades) if winning_trades else 0
        gross_loss = abs(sum(losing_trades)) if losing_trades else 1
        profit_factor = gross_profit / gross_loss if gross_loss != 0 else 0
        
        # Average trade
        avg_trade = np.mean(pnl_list) if pnl_list else 0
        avg_win = np.mean(winning_trades) if winning_trades else 0
        avg_loss = np.mean(losing_trades) if losing_trades else 0
        
        # Max drawdown
        portfolio_values = [self.initial_capital]
        cumulative_pnl = 0
        for pnl in pnl_list:
            cumulative_pnl += pnl
            portfolio_values.append(self.initial_capital + cumulative_pnl)
        
        peak = portfolio_values[0]
        max_dd = 0
        for value in portfolio_values:
            if value > peak:
                peak = value
            dd = (peak - value) / peak * 100
            if dd > max_dd:
                max_dd = dd
        
        # Sharpe ratio (annualized)
        if len(pnl_list) > 1:
            returns = np.array(pnl_list) / self.initial_capital
            sharpe = np.mean(returns) / np.std(returns) * np.sqrt(252) if np.std(returns) != 0 else 0
        else:
            sharpe = 0
        
        # Trade breakdown
        long_trades = sum(1 for pos in self.positions if pos['type'] == 'long')
        short_trades = sum(1 for pos in self.positions if pos['type'] == 'short')
        
        return {
            'initial_capital': self.initial_capital,
            'final_capital': final_capital,
            'total_pnl': total_pnl,
            'total_return': total_return,
            'total_trades': len(pnl_list),
            'long_trades': long_trades,
            'short_trades': short_trades,
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'avg_trade': avg_trade,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'max_drawdown': max_dd,
            'sharpe_ratio': sharpe,
            'total_commission': sum(t['commission'] for t in self.trades)
        }
    
    def plot_results(self, figsize=(15, 10)):
        """Visualize backtest results with multiple subplots."""
        fig, axes = plt.subplots(4, 1, figsize=figsize)
        
        # Plot 1: Price and positions
        ax1 = axes[0]
        ax1.plot(self.data['timestamp'], self.data['close'], label=f'{self.asset_symbol} Price', alpha=0.7)
        
        # Mark entry points
        for pos in self.positions:
            entry_time = self.data.iloc[pos['entry_idx']]['timestamp']
            entry_price = pos['entry_price']
            
            if pos['type'] == 'long':
                ax1.scatter(entry_time, entry_price, color='green', marker='^', 
                           s=100, label='Long Entry' if pos == self.positions[0] else '', zorder=5)
            else:
                ax1.scatter(entry_time, entry_price, color='red', marker='v', 
                           s=100, label='Short Entry' if pos == self.positions[0] else '', zorder=5)
            
            # Mark exit points
            if 'exit_price' in pos:
                exit_time = self.data.iloc[pos['exit_idx']]['timestamp']
                exit_price = pos['exit_price']
                ax1.scatter(exit_time, exit_price, color='blue', marker='x', 
                           s=100, label='Exit' if pos == self.positions[0] else '', zorder=5)
        
        ax1.set_title('Bitcoin Price and Trading Positions', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Price (USD)')
        ax1.legend(loc='best')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Portfolio value over time
        ax2 = axes[1]
        portfolio_values = [self.initial_capital]
        cumulative_pnl = 0
        timestamps = [self.data.iloc[0]['timestamp']]
        
        for pos in self.positions:
            if 'exit_price' in pos:
                if pos['type'] == 'long':
                    pnl = (pos['exit_price'] - pos['entry_price']) * pos['size']
                else:
                    pnl = (pos['entry_price'] - pos['exit_price']) * pos['size']
                
                commission = (pos['entry_price'] + pos['exit_price']) * pos['size'] * self.commission
                cumulative_pnl += (pnl - commission)
                
                portfolio_values.append(self.initial_capital + cumulative_pnl)
                timestamps.append(self.data.iloc[pos['exit_idx']]['timestamp'])
        
        ax2.plot(timestamps, portfolio_values, label='Portfolio Value', color='green', linewidth=2)
        ax2.axhline(y=self.initial_capital, color='gray', linestyle='--', label='Initial Capital')
        ax2.set_title('Portfolio Value Over Time', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Portfolio Value (USD)')
        ax2.legend(loc='best')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Technical indicators
        ax3 = axes[2]
        ax3.plot(self.data['timestamp'], self.data['rsi'], label='RSI', color='purple')
        ax3.axhline(y=70, color='red', linestyle='--', alpha=0.5, label='Overbought')
        ax3.axhline(y=30, color='green', linestyle='--', alpha=0.5, label='Oversold')
        ax3.set_title('RSI Indicator', fontsize=12, fontweight='bold')
        ax3.set_ylabel('RSI')
        ax3.legend(loc='best')
        ax3.grid(True, alpha=0.3)
        ax3.set_ylim([0, 100])
        
        # Plot 4: Trade P&L distribution
        ax4 = axes[3]
        pnl_list = []
        for pos in self.positions:
            if 'exit_price' in pos:
                if pos['type'] == 'long':
                    pnl = (pos['exit_price'] - pos['entry_price']) * pos['size']
                else:
                    pnl = (pos['entry_price'] - pos['exit_price']) * pos['size']
                commission = (pos['entry_price'] + pos['exit_price']) * pos['size'] * self.commission
                pnl_list.append(pnl - commission)
        
        colors = ['green' if p > 0 else 'red' for p in pnl_list]
        ax4.bar(range(len(pnl_list)), pnl_list, color=colors, alpha=0.7)
        ax4.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
        ax4.set_title('Individual Trade P&L', fontsize=12, fontweight='bold')
        ax4.set_xlabel('Trade Number')
        ax4.set_ylabel('P&L (USD)')
        ax4.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('/home/user/backtest_results.png', dpi=150, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def print_performance_report(self, metrics: Dict):
        """Print a detailed performance report."""
        print("\n" + "="*60)
        print("BITCOIN BACKTESTING PERFORMANCE REPORT")
        print("="*60)
        
        print("\n📊 CAPITAL & RETURNS")
        print(f"Initial Capital:        ${metrics['initial_capital']:,.2f}")
        print(f"Final Capital:          ${metrics['final_capital']:,.2f}")
        print(f"Total P&L:              ${metrics['total_pnl']:,.2f}")
        print(f"Total Return:           {metrics['total_return']:.2f}%")
        
        print("\n📈 TRADE STATISTICS")
        print(f"Total Trades:           {metrics['total_trades']}")
        print(f"Long Trades:            {metrics['long_trades']}")
        print(f"Short Trades:           {metrics['short_trades']}")
        print(f"Winning Trades:         {metrics['winning_trades']}")
        print(f"Losing Trades:          {metrics['losing_trades']}")
        print(f"Win Rate:               {metrics['win_rate']:.2f}%")
        
        print("\n💰 PROFIT METRICS")
        print(f"Profit Factor:          {metrics['profit_factor']:.2f}")
        print(f"Average Trade:          ${metrics['avg_trade']:,.2f}")
        print(f"Average Win:            ${metrics['avg_win']:,.2f}")
        print(f"Average Loss:           ${metrics['avg_loss']:,.2f}")
        
        print("\n⚠️  RISK METRICS")
        print(f"Max Drawdown:           {metrics['max_drawdown']:.2f}%")
        print(f"Sharpe Ratio:           {metrics['sharpe_ratio']:.2f}")
        print(f"Total Commission:       ${metrics['total_commission']:,.2f}")
        
        print("\n" + "="*60 + "\n")
    
    def export_trades(self, filename: str = '/home/user/trades.csv'):
        """Export trade history to CSV."""
        if self.trades:
            trades_df = pd.DataFrame(self.trades)
            trades_df.to_csv(filename, index=False)
            print(f"✅ Trades exported to {filename}")
        else:
            print("❌ No trades to export")


# Example usage and demo
def run_example():
    """Run example backtests with different strategies."""
    print("\n🚀 Cryptocurrency Backtesting Engine - Example Run\n")
    
    # Initialize backtester
    bt = CryptoBacktester(initial_capital=10000, commission=0.001)
    
    # Load data (automatically tries real Hyperliquid data first)
    print("📊 Loading Bitcoin price data...")
    bt.load_data(days=365, interval="1h", use_real_data=True)
    
    # Calculate indicators
    print("📈 Calculating technical indicators...")
    bt.calculate_indicators()
    
    # Test multiple strategies
    strategies = [
        ('sma_crossover', {'fast_period': 20, 'slow_period': 50, 'allow_short': True}),
        ('rsi_mean_reversion', {'oversold': 30, 'overbought': 70, 'allow_short': True}),
        ('macd_momentum', {'allow_short': True}),
        ('bollinger_bands', {'allow_short': True}),
        ('dual_momentum', {'allow_short': True})
    ]
    
    results = {}
    
    for strategy_name, params in strategies:
        print(f"\n🔄 Running {strategy_name.upper()} strategy...")
        bt_instance = CryptoBacktester(initial_capital=10000, commission=0.001)
        bt_instance.data = bt.data.copy()
        
        metrics = bt_instance.run_strategy(strategy_name, **params)
        results[strategy_name] = metrics
        
        bt_instance.print_performance_report(metrics)
    
    # Compare strategies
    print("\n" + "="*60)
    print("STRATEGY COMPARISON")
    print("="*60)
    print(f"{'Strategy':<25} {'Return':<12} {'Trades':<10} {'Win Rate':<12} {'Sharpe':<10}")
    print("-"*60)
    
    for strategy_name, metrics in results.items():
        print(f"{strategy_name:<25} {metrics['total_return']:>10.2f}% {metrics['total_trades']:>8} "
              f"{metrics['win_rate']:>10.2f}% {metrics['sharpe_ratio']:>10.2f}")
    
    print("="*60 + "\n")
    
    # Plot best performing strategy
    best_strategy = max(results.items(), key=lambda x: x[1]['total_return'])
    print(f"📊 Plotting results for best strategy: {best_strategy[0].upper()}")
    
    bt_best = CryptoBacktester(initial_capital=10000, commission=0.001)
    bt_best.data = bt.data.copy()
    bt_best.run_strategy(best_strategy[0], **dict(strategies[[s[0] for s in strategies].index(best_strategy[0])][1]))
    bt_best.plot_results()
    bt_best.export_trades()
    
    return bt_best, results


if __name__ == "__main__":
    # Run the example
    backtester, results = run_example()
    
    print("\n✨ Backtest complete! Check the generated plots and CSV files.")
    print("📁 Files created:")
    print("   - /home/user/backtest_results.png")
    print("   - /home/user/trades.csv")
