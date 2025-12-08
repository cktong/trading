#!/usr/bin/env python3
"""
Quick Start Example
===================
Simple example showing how to backtest cryptocurrency trading strategies.

This example works with any cryptocurrency: BTC, ETH, SOL, SPDR, GLAM, etc.
"""

import sys
sys.path.insert(0, '/home/user/webapp')

from core import CryptoBacktester
from data_sources import HyperliquidDataFetcher

def quick_backtest(asset="BTC", interval="1h", days=30):
    """
    Run a quick backtest for any cryptocurrency.
    
    Args:
        asset: Cryptocurrency symbol (e.g., "BTC", "ETH", "SPDR", "GLAM")
        interval: Candle interval (e.g., "1h", "4h", "1d")
        days: Number of days of historical data
    """
    print(f"\n{'='*70}")
    print(f"🚀 Quick Backtest: {asset}")
    print(f"{'='*70}\n")
    
    # Initialize backtester for the specific asset
    bt = CryptoBacktester(asset_symbol=asset, initial_capital=10000)
    
    # Load real data from Hyperliquid
    print(f"📊 Loading {asset} data...")
    bt.load_data(days=days, interval=interval, use_real_data=True)
    
    # Calculate technical indicators
    print("📈 Calculating technical indicators...")
    bt.calculate_indicators()
    
    # Run SMA Crossover strategy with short selling
    print(f"🔄 Running SMA Crossover strategy for {asset}...")
    metrics = bt.run_strategy('sma_crossover', 
                             fast_period=20, 
                             slow_period=50, 
                             allow_short=True)
    
    # Print results
    bt.print_performance_report(metrics)
    
    # Export trades
    bt.export_trades(f'/home/user/{asset}_trades.csv')
    
    return bt, metrics


if __name__ == "__main__":
    # Example 1: Bitcoin
    print("\n" + "="*70)
    print("Example 1: Bitcoin (BTC)")
    print("="*70)
    bt_btc, metrics_btc = quick_backtest("BTC", interval="1h", days=30)
    
    # Example 2: SPDR Token
    print("\n" + "="*70)
    print("Example 2: SPDR Token")
    print("="*70)
    bt_spdr, metrics_spdr = quick_backtest("SPDR", interval="1h", days=30)
    
    # Example 3: GLAM Token
    print("\n" + "="*70)
    print("Example 3: GLAM Token")
    print("="*70)
    bt_glam, metrics_glam = quick_backtest("GLAM", interval="1h", days=30)
    
    # Compare results
    print("\n" + "="*70)
    print("📊 PERFORMANCE COMPARISON")
    print("="*70)
    print(f"{'Asset':<10} {'Return':<15} {'Win Rate':<15} {'Sharpe Ratio':<15}")
    print("-"*70)
    print(f"{'BTC':<10} {metrics_btc['total_return']:>12.2f}%  {metrics_btc['win_rate']:>12.2f}%  {metrics_btc['sharpe_ratio']:>12.2f}")
    print(f"{'SPDR':<10} {metrics_spdr['total_return']:>12.2f}%  {metrics_spdr['win_rate']:>12.2f}%  {metrics_spdr['sharpe_ratio']:>12.2f}")
    print(f"{'GLAM':<10} {metrics_glam['total_return']:>12.2f}%  {metrics_glam['win_rate']:>12.2f}%  {metrics_glam['sharpe_ratio']:>12.2f}")
    print("="*70 + "\n")
    
    print("✨ Backtest complete! Check the generated CSV files for detailed trade history.")
