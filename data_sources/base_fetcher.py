"""
Base Data Fetcher
==================
Abstract base class for all cryptocurrency data fetchers.

Author: AI Assistant
Date: 2025
"""

from abc import ABC, abstractmethod
import pandas as pd
from typing import Optional, List, Dict
from datetime import datetime


class BaseDataFetcher(ABC):
    """
    Abstract base class for cryptocurrency data fetchers.
    
    All exchange-specific fetchers should inherit from this class
    and implement the required abstract methods.
    """
    
    def __init__(self, exchange_name: str):
        """
        Initialize the base data fetcher.
        
        Args:
            exchange_name: Name of the exchange (e.g., "hyperliquid", "binance")
        """
        self.exchange_name = exchange_name
        
    @abstractmethod
    def fetch_candles(self, 
                     coin: str,
                     interval: str,
                     start_time: Optional[int] = None,
                     end_time: Optional[int] = None,
                     max_candles: int = 5000) -> pd.DataFrame:
        """
        Fetch OHLCV candle data for a specific cryptocurrency.
        
        Args:
            coin: Trading pair symbol (e.g., "BTC", "ETH", "SPDR")
            interval: Candle interval (e.g., "1h", "4h", "1d")
            start_time: Start time in epoch milliseconds (optional)
            end_time: End time in epoch milliseconds (optional)
            max_candles: Maximum number of candles to fetch
            
        Returns:
            DataFrame with columns: timestamp, open, high, low, close, volume
        """
        pass
    
    @abstractmethod
    def get_available_coins(self) -> List[str]:
        """
        Get list of available trading pairs on this exchange.
        
        Returns:
            List of coin symbols (e.g., ["BTC", "ETH", "SOL"])
        """
        pass
    
    def fetch_for_backtest(self, 
                          coin: str,
                          interval: str = "1h",
                          days_back: int = 30) -> pd.DataFrame:
        """
        Fetch data formatted for backtesting (convenience method).
        
        Args:
            coin: Trading pair symbol
            interval: Candle interval
            days_back: Number of days to look back
            
        Returns:
            DataFrame ready for backtesting
        """
        from datetime import timedelta
        
        end_time = int(datetime.now().timestamp() * 1000)
        start_time = int((datetime.now() - timedelta(days=days_back)).timestamp() * 1000)
        
        return self.fetch_candles(coin, interval, start_time, end_time)
    
    def validate_interval(self, interval: str, supported_intervals: List[str]) -> bool:
        """
        Validate if the interval is supported by this exchange.
        
        Args:
            interval: Interval to validate
            supported_intervals: List of supported intervals
            
        Returns:
            True if valid, False otherwise
        """
        if interval not in supported_intervals:
            print(f"⚠️  Warning: Interval '{interval}' not in supported list: {supported_intervals}")
            return False
        return True
    
    def resample_to_daily(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Resample intraday data to daily candles.
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            DataFrame resampled to daily frequency
        """
        if df.empty:
            return df
        
        df_resampled = df.set_index('timestamp').resample('D').agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        }).dropna().reset_index()
        
        print(f"✅ Resampled to {len(df_resampled)} daily candles")
        
        return df_resampled
    
    def print_data_summary(self, df: pd.DataFrame, coin: str):
        """
        Print summary statistics for fetched data.
        
        Args:
            df: DataFrame with OHLCV data
            coin: Coin symbol
        """
        if df.empty:
            print("❌ No data to summarize")
            return
        
        print(f"\n📈 {coin} Data Summary ({self.exchange_name}):")
        print(f"   Candles:      {len(df)}")
        print(f"   Date range:   {df['timestamp'].min()} to {df['timestamp'].max()}")
        print(f"   First price:  ${df['close'].iloc[0]:,.2f}")
        print(f"   Last price:   ${df['close'].iloc[-1]:,.2f}")
        print(f"   Price change: {((df['close'].iloc[-1] / df['close'].iloc[0]) - 1) * 100:.2f}%")
        print(f"   Highest:      ${df['high'].max():,.2f}")
        print(f"   Lowest:       ${df['low'].min():,.2f}")
        print(f"   Avg volume:   {df['volume'].mean():.2f}")
    
    @staticmethod
    def interval_to_minutes(interval: str) -> int:
        """
        Convert interval string to minutes.
        
        Args:
            interval: Interval string (e.g., "1h", "4h", "1d")
            
        Returns:
            Number of minutes
        """
        interval_map = {
            "1m": 1,
            "3m": 3,
            "5m": 5,
            "15m": 15,
            "30m": 30,
            "1h": 60,
            "2h": 120,
            "4h": 240,
            "6h": 360,
            "8h": 480,
            "12h": 720,
            "1d": 1440,
            "3d": 4320,
            "1w": 10080,
            "1M": 43200  # Approximate
        }
        return interval_map.get(interval, 60)
    
    @staticmethod
    def calculate_max_days(max_candles: int, interval: str) -> float:
        """
        Calculate maximum days of history available.
        
        Args:
            max_candles: Maximum number of candles available
            interval: Candle interval
            
        Returns:
            Number of days of history
        """
        interval_minutes = BaseDataFetcher.interval_to_minutes(interval)
        return (max_candles * interval_minutes) / (60 * 24)


class DataFetcherError(Exception):
    """Custom exception for data fetcher errors."""
    pass
