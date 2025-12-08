"""
Core Backtesting Module
========================
Universal cryptocurrency backtesting engine and utilities.
"""

from .backtest_engine import CryptoBacktester

__all__ = ['CryptoBacktester']

# For backward compatibility, alias the old name
BitcoinBacktester = CryptoBacktester
