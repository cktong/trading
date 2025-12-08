"""
Hyperliquid Data Fetcher
=========================
Fetch historical cryptocurrency price data from Hyperliquid API.

Author: AI Assistant
Date: 2025
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, List
import time

from .base_fetcher import BaseDataFetcher, DataFetcherError


class HyperliquidDataFetcher(BaseDataFetcher):
    """
    Fetch historical OHLCV data from Hyperliquid API.
    
    Hyperliquid provides candle data through their public info endpoint.
    Only the most recent 5000 candles are available per interval.
    """
    
    def __init__(self):
        """Initialize the Hyperliquid data fetcher."""
        super().__init__("hyperliquid")
        self.base_url = "https://api.hyperliquid.xyz/info"
        self.headers = {"Content-Type": "application/json"}
        self.max_candles = 5000
        self.supported_intervals = ["1m", "3m", "5m", "15m", "30m", "1h", 
                                    "2h", "4h", "8h", "12h", "1d", "3d", "1w", "1M"]
        
    def fetch_candles(self, 
                     coin: str = "BTC",
                     interval: str = "1h",
                     start_time: Optional[int] = None,
                     end_time: Optional[int] = None,
                     max_candles: int = 5000) -> pd.DataFrame:
        """
        Fetch candle data from Hyperliquid.
        
        Args:
            coin: Trading pair (e.g., "BTC", "ETH", "SOL", "SPDR", "GLAM")
            interval: Candle interval - "1m", "3m", "5m", "15m", "30m", "1h", 
                     "2h", "4h", "8h", "12h", "1d", "3d", "1w", "1M"
            start_time: Start time in epoch milliseconds (optional)
            end_time: End time in epoch milliseconds (optional)
            max_candles: Maximum number of candles to fetch (default 5000)
            
        Returns:
            DataFrame with columns: timestamp, open, high, low, close, volume
        """
        # Validate interval
        self.validate_interval(interval, self.supported_intervals)
        
        # If no end_time specified, use current time
        if end_time is None:
            end_time = int(datetime.now().timestamp() * 1000)
        
        # If no start_time specified, calculate based on interval and max_candles
        if start_time is None:
            interval_minutes = self.interval_to_minutes(interval)
            ms_per_candle = interval_minutes * 60 * 1000
            start_time = end_time - (max_candles * ms_per_candle)
        
        # Request body
        payload = {
            "type": "candleSnapshot",
            "req": {
                "coin": coin,
                "interval": interval,
                "startTime": start_time,
                "endTime": end_time
            }
        }
        
        try:
            response = requests.post(self.base_url, json=payload, headers=self.headers)
            response.raise_for_status()
            
            candles_data = response.json()
            
            if not candles_data:
                print(f"⚠️  No data returned for {coin} with interval {interval}")
                return pd.DataFrame()
            
            # Parse candle data
            candles = []
            for candle in candles_data:
                candles.append({
                    'timestamp': pd.to_datetime(candle['t'], unit='ms'),
                    'open': float(candle['o']),
                    'high': float(candle['h']),
                    'low': float(candle['l']),
                    'close': float(candle['c']),
                    'volume': float(candle['v'])
                })
            
            df = pd.DataFrame(candles)
            df = df.sort_values('timestamp').reset_index(drop=True)
            
            print(f"✅ Fetched {len(df)} candles for {coin} from Hyperliquid")
            print(f"   Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
            
            return df
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching data from Hyperliquid: {e}")
            raise DataFetcherError(f"Failed to fetch {coin} data: {e}")
    
    def get_available_coins(self) -> List[str]:
        """
        Get list of available trading pairs from Hyperliquid.
        
        Returns:
            List of coin symbols
        """
        payload = {
            "type": "meta"
        }
        
        try:
            response = requests.post(self.base_url, json=payload, headers=self.headers)
            response.raise_for_status()
            
            meta_data = response.json()
            coins = [asset['name'] for asset in meta_data['universe']]
            
            print(f"✅ Found {len(coins)} available coins on Hyperliquid")
            return coins
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching available coins: {e}")
            return []
    
    def fetch_for_backtest(self, 
                          coin: str = "BTC",
                          interval: str = "1h",
                          days_back: int = 30) -> pd.DataFrame:
        """
        Fetch cryptocurrency data formatted for the backtesting system.
        
        Args:
            coin: Trading pair (e.g., "BTC", "ETH", "SPDR", "GLAM")
            interval: Candle interval
            days_back: Number of days to look back
            
        Returns:
            DataFrame ready for CryptoBacktester
        """
        print(f"\n📊 Fetching {coin} data from Hyperliquid for backtesting...")
        print(f"   Interval: {interval}")
        print(f"   Days back: {days_back}")
        
        # Note: Hyperliquid only keeps 5000 recent candles
        # Calculate maximum days available for the interval
        max_days_available = self.calculate_max_days(self.max_candles, interval)
        
        if days_back > max_days_available:
            print(f"⚠️  Warning: Requested {days_back} days but only {max_days_available:.1f} days available")
            print(f"   Hyperliquid only stores the most recent {self.max_candles} candles")
            days_back = int(max_days_available)
        
        # Fetch the data
        df = self.fetch_candles(
            coin=coin,
            interval=interval,
            start_time=int((datetime.now() - timedelta(days=days_back)).timestamp() * 1000),
            end_time=int(datetime.now().timestamp() * 1000)
        )
        
        if df.empty:
            print("❌ No data fetched")
            return df
        
        # Print summary
        self.print_data_summary(df, coin)
        
        return df
    
    def fetch_multiple_intervals(self,
                                coin: str = "BTC",
                                intervals: List[str] = ["1h", "4h", "1d"],
                                days_back: int = 30) -> dict:
        """
        Fetch data for multiple intervals.
        
        Args:
            coin: Trading pair
            intervals: List of intervals to fetch
            days_back: Number of days to look back
            
        Returns:
            Dictionary with interval as key and DataFrame as value
        """
        end_time = int(datetime.now().timestamp() * 1000)
        start_time = int((datetime.now() - timedelta(days=days_back)).timestamp() * 1000)
        
        results = {}
        for interval in intervals:
            print(f"\nFetching {interval} candles for {coin}...")
            try:
                df = self.fetch_candles(coin, interval, start_time, end_time)
                if not df.empty:
                    results[interval] = df
            except DataFetcherError as e:
                print(f"⚠️  Skipping {interval}: {e}")
            time.sleep(0.5)  # Be nice to the API
        
        return results
    
    def fetch_multiple_coins(self,
                           coins: List[str] = ["BTC", "ETH", "SOL"],
                           interval: str = "1h",
                           days_back: int = 30) -> dict:
        """
        Fetch data for multiple cryptocurrencies.
        
        Args:
            coins: List of coin symbols (e.g., ["BTC", "SPDR", "GLAM"])
            interval: Candle interval
            days_back: Number of days to look back
            
        Returns:
            Dictionary with coin as key and DataFrame as value
        """
        results = {}
        for coin in coins:
            print(f"\n{'='*60}")
            print(f"Fetching {coin} data...")
            print(f"{'='*60}")
            try:
                df = self.fetch_for_backtest(coin, interval, days_back)
                if not df.empty:
                    results[coin] = df
            except DataFetcherError as e:
                print(f"⚠️  Skipping {coin}: {e}")
            time.sleep(0.5)  # Be nice to the API
        
        return results


def example_usage():
    """Example usage of the Hyperliquid data fetcher."""
    
    print("="*60)
    print("HYPERLIQUID DATA FETCHER - EXAMPLE USAGE")
    print("="*60)
    
    # Initialize fetcher
    fetcher = HyperliquidDataFetcher()
    
    # Example 1: Get available coins
    print("\n1. Fetching available trading pairs...")
    coins = fetcher.get_available_coins()
    if coins:
        print(f"   Sample coins: {coins[:15]}")
    
    # Example 2: Fetch Bitcoin hourly data
    print("\n2. Fetching Bitcoin 1-hour candles...")
    btc_hourly = fetcher.fetch_for_backtest(coin="BTC", interval="1h", days_back=30)
    
    if not btc_hourly.empty:
        print("\nFirst 5 rows:")
        print(btc_hourly.head())
    
    # Example 3: Fetch multiple intervals
    print("\n3. Fetching Bitcoin data at multiple intervals...")
    multi_data = fetcher.fetch_multiple_intervals(
        coin="BTC",
        intervals=["1h", "4h", "1d"],
        days_back=30
    )
    
    for interval, df in multi_data.items():
        print(f"\n{interval}: {len(df)} candles")
    
    # Example 4: Fetch SPDR and GLAM tokens
    print("\n4. Fetching data for SPDR and GLAM tokens...")
    token_data = fetcher.fetch_multiple_coins(
        coins=["SPDR", "GLAM", "HYPE"],
        interval="1h",
        days_back=30
    )
    
    for coin, df in token_data.items():
        if not df.empty:
            print(f"\n{coin}: {len(df)} candles")
            print(f"   Current price: ${df['close'].iloc[-1]:,.4f}")
    
    # Example 5: Fetch and resample to daily
    print("\n5. Fetching 1-hour data and resampling to daily...")
    btc_hourly = fetcher.fetch_candles(coin="BTC", interval="1h")
    if not btc_hourly.empty:
        btc_daily = fetcher.resample_to_daily(btc_hourly)
        print("\nDaily data (last 5 days):")
        print(btc_daily.tail())
    
    print("\n" + "="*60)
    print("Example complete!")
    print("="*60)


if __name__ == "__main__":
    example_usage()
