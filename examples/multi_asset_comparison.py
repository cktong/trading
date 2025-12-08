#!/usr/bin/env python3
"""
Multi-Asset Comparison Example
===============================
Compare backtest performance across multiple cryptocurrencies.

Tests BTC, ETH, SOL, SPDR, and GLAM with the same strategy.
"""

import sys
sys.path.insert(0, '/home/user/webapp')

from core import CryptoBacktester
from data_sources import HyperliquidDataFetcher
import pandas as pd


def backtest_asset(asset, strategy='sma_crossover', interval="1h", days=30):
    """
    Backtest a single asset with a specific strategy.
    
    Args:
        asset: Cryptocurrency symbol
        strategy: Trading strategy name
        interval: Candle interval
        days: Historical data period
        
    Returns:
        metrics: Performance metrics dictionary
    """
    try:
        print(f"\n{'─'*70}")
        print(f"📊 Testing {asset}...")
        print(f"{'─'*70}")
        
        # Initialize backtester
        bt = CryptoBacktester(asset_symbol=asset, initial_capital=10000)
        
        # Load data
        bt.load_data(days=days, interval=interval, use_real_data=True)
        
        # Calculate indicators
        bt.calculate_indicators()
        
        # Run strategy
        metrics = bt.run_strategy(strategy, fast_period=20, slow_period=50, allow_short=True)
        
        # Add asset info to metrics
        metrics['asset'] = asset
        
        return metrics
        
    except Exception as e:
        print(f"⚠️  Error testing {asset}: {e}")
        return None


def compare_assets(assets, strategy='sma_crossover', interval="1h", days=30):
    """
    Compare multiple assets with the same strategy.
    
    Args:
        assets: List of cryptocurrency symbols
        strategy: Trading strategy name
        interval: Candle interval
        days: Historical data period
    """
    print("\n" + "="*70)
    print(f"🚀 MULTI-ASSET BACKTEST COMPARISON")
    print(f"   Strategy: {strategy.upper()}")
    print(f"   Interval: {interval}")
    print(f"   Period: {days} days")
    print("="*70)
    
    results = []
    
    for asset in assets:
        metrics = backtest_asset(asset, strategy, interval, days)
        if metrics:
            results.append(metrics)
    
    if not results:
        print("❌ No results to display")
        return
    
    # Display comparison table
    print("\n" + "="*70)
    print("📊 PERFORMANCE COMPARISON")
    print("="*70)
    print(f"{'Asset':<8} {'Return %':<12} {'Trades':<10} {'Win Rate %':<12} {'Sharpe':<10} {'Max DD %':<12}")
    print("-"*70)
    
    for metrics in results:
        print(f"{metrics['asset']:<8} "
              f"{metrics['total_return']:>10.2f}% "
              f"{metrics['total_trades']:>8} "
              f"{metrics['win_rate']:>10.2f}% "
              f"{metrics['sharpe_ratio']:>10.2f} "
              f"{metrics['max_drawdown']:>10.2f}%")
    
    print("="*70)
    
    # Find best performing asset
    best = max(results, key=lambda x: x['total_return'])
    worst = min(results, key=lambda x: x['total_return'])
    
    print(f"\n🏆 Best Performer: {best['asset']} with {best['total_return']:.2f}% return")
    print(f"📉 Worst Performer: {worst['asset']} with {worst['total_return']:.2f}% return")
    
    # Risk-adjusted best
    best_sharpe = max(results, key=lambda x: x['sharpe_ratio'])
    print(f"⚖️  Best Risk-Adjusted: {best_sharpe['asset']} with Sharpe Ratio of {best_sharpe['sharpe_ratio']:.2f}")
    
    return results


def test_all_strategies(asset="BTC", interval="1h", days=30):
    """
    Test all available strategies on a single asset.
    
    Args:
        asset: Cryptocurrency symbol
        interval: Candle interval
        days: Historical data period
    """
    print("\n" + "="*70)
    print(f"🔬 STRATEGY COMPARISON FOR {asset}")
    print("="*70)
    
    # Load data once
    bt = CryptoBacktester(asset_symbol=asset, initial_capital=10000)
    bt.load_data(days=days, interval=interval, use_real_data=True)
    bt.calculate_indicators()
    
    strategies = [
        ('sma_crossover', {'fast_period': 20, 'slow_period': 50}),
        ('rsi_mean_reversion', {'oversold': 30, 'overbought': 70}),
        ('macd_momentum', {}),
        ('bollinger_bands', {}),
        ('dual_momentum', {})
    ]
    
    results = []
    
    for strategy_name, params in strategies:
        print(f"\n🔄 Testing {strategy_name}...")
        bt_test = CryptoBacktester(asset_symbol=asset, initial_capital=10000)
        bt_test.data = bt.data.copy()
        
        metrics = bt_test.run_strategy(strategy_name, allow_short=True, **params)
        metrics['strategy'] = strategy_name
        results.append(metrics)
    
    # Display results
    print("\n" + "="*70)
    print(f"📊 STRATEGY PERFORMANCE FOR {asset}")
    print("="*70)
    print(f"{'Strategy':<25} {'Return %':<12} {'Win Rate %':<12} {'Sharpe':<10}")
    print("-"*70)
    
    for metrics in results:
        print(f"{metrics['strategy']:<25} "
              f"{metrics['total_return']:>10.2f}% "
              f"{metrics['win_rate']:>10.2f}% "
              f"{metrics['sharpe_ratio']:>10.2f}")
    
    print("="*70)
    
    best = max(results, key=lambda x: x['total_return'])
    print(f"\n🏆 Best Strategy: {best['strategy']} with {best['total_return']:.2f}% return")
    
    return results


if __name__ == "__main__":
    # Example 1: Compare multiple assets with same strategy
    print("\n🌟 EXAMPLE 1: Multi-Asset Comparison")
    assets_to_test = ["BTC", "ETH", "SOL", "SPDR", "GLAM"]
    asset_results = compare_assets(assets_to_test, strategy='sma_crossover', interval="1h", days=30)
    
    # Example 2: Compare all strategies on Bitcoin
    print("\n\n🌟 EXAMPLE 2: All Strategies on Bitcoin")
    strategy_results = test_all_strategies("BTC", interval="1h", days=30)
    
    # Example 3: Compare all strategies on SPDR
    print("\n\n🌟 EXAMPLE 3: All Strategies on SPDR")
    spdr_results = test_all_strategies("SPDR", interval="1h", days=30)
    
    print("\n✨ Multi-asset comparison complete!")
    print("\n💡 Key Insights:")
    print("   - Different assets perform differently with the same strategy")
    print("   - Different strategies work better for different market conditions")
    print("   - Risk-adjusted returns (Sharpe ratio) are often more important than raw returns")
