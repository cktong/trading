# 🚀 Universal Crypto Backtesting Engine

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Hyperliquid](https://img.shields.io/badge/Hyperliquid-API-orange.svg)](https://hyperliquid.xyz)

A comprehensive cryptocurrency backtesting framework supporting **any crypto asset** including Bitcoin, Ethereum, SPDR, GLAM, and 200+ other coins with **both spot and futures** trading.

## ✨ Features

### 🌐 Universal Asset Support
- ✅ **Bitcoin (BTC)** - Most popular cryptocurrency
- ✅ **Ethereum (ETH)** - Second largest crypto  
- ✅ **Solana (SOL)** - High-performance blockchain
- ✅ **SPDR Token** - SPDR ETF token
- ✅ **GLAM Token** - GLAM project token
- ✅ **200+ other cryptocurrencies** on Hyperliquid

### 📊 Trading Capabilities
- ✅ **5 Pre-built Strategies**: SMA Crossover, RSI Mean Reversion, MACD Momentum, Bollinger Bands, Dual Momentum
- ✅ **Real Market Data**: Fetch live historical data from Hyperliquid API
- ✅ **Spot & Futures Support**: Long and short positions
- ✅ **Comprehensive Metrics**: Sharpe ratio, max drawdown, win rate, profit factor
- ✅ **Multi-Asset Comparison**: Compare performance across different cryptocurrencies
- ✅ **Strategy Optimization**: Test multiple parameter combinations

### 🛠️ Additional Features
- ✅ **Interactive Notebooks**: Jupyter notebooks for hands-on learning
- ✅ **Visualization Tools**: Detailed performance charts and analysis
- ✅ **24/7 Hosting Ready**: Complete deployment scripts for cloud servers
- ✅ **Pip Installable**: Easy installation as a Python package

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/cktong/crypto-backtest-engine.git
cd crypto-backtest-engine

# Install dependencies
pip install -r requirements.txt

# Or install as a package
pip install -e .
```

### Your First Backtest

**Test Bitcoin:**
```python
from core import CryptoBacktester

# Initialize for Bitcoin
bt = CryptoBacktester(asset_symbol="BTC", initial_capital=10000)

# Load real data from Hyperliquid
bt.load_data(days=30, interval="1h")
bt.calculate_indicators()

# Run SMA Crossover strategy with short selling
metrics = bt.run_strategy('sma_crossover', 
                         fast_period=20, 
                         slow_period=50, 
                         allow_short=True)

# View results
bt.print_performance_report(metrics)
bt.plot_results()
```

**Test SPDR Token:**
```python
# Just change the asset_symbol - everything else stays the same!
bt_spdr = CryptoBacktester(asset_symbol="SPDR", initial_capital=10000)
bt_spdr.load_data(days=30, interval="1h")
bt_spdr.calculate_indicators()
metrics_spdr = bt_spdr.run_strategy('sma_crossover', allow_short=True)
bt_spdr.print_performance_report(metrics_spdr)
```

**Test GLAM Token:**
```python
bt_glam = CryptoBacktester(asset_symbol="GLAM", initial_capital=10000)
bt_glam.load_data(days=30, interval="1h")
bt_glam.calculate_indicators()
metrics_glam = bt_glam.run_strategy('sma_crossover', allow_short=True)
bt_glam.print_performance_report(metrics_glam)
```

### Quick Examples

**Option 1: Quick Start Script**
```bash
python3 examples/quick_start.py
```

**Option 2: Multi-Asset Comparison**
```bash
python3 examples/multi_asset_comparison.py
```

**Option 3: Interactive Notebook**
```bash
jupyter notebook notebooks/01_quick_start.ipynb
```

## 🎯 Available Strategies

### 1. SMA Crossover
Trend-following strategy using moving average crossovers.
```python
bt.run_strategy('sma_crossover', fast_period=20, slow_period=50, allow_short=True)
```

### 2. RSI Mean Reversion
Buy oversold, sell overbought conditions.
```python
bt.run_strategy('rsi_mean_reversion', oversold=30, overbought=70, allow_short=True)
```

### 3. MACD Momentum
Momentum-based entries using MACD signals.
```python
bt.run_strategy('macd_momentum', allow_short=True)
```

### 4. Bollinger Bands
Volatility-based trading at band extremes.
```python
bt.run_strategy('bollinger_bands', allow_short=True)
```

### 5. Dual Momentum
Combined trend and momentum confirmation.
```python
bt.run_strategy('dual_momentum', allow_short=True)
```

## 📊 Supported Assets

### Major Cryptocurrencies
| Symbol | Name | Category | Exchanges |
|--------|------|----------|-----------|
| BTC | Bitcoin | Layer 1 | Hyperliquid, Binance, Coinbase |
| ETH | Ethereum | Layer 1 | Hyperliquid, Binance, Coinbase |
| SOL | Solana | Layer 1 | Hyperliquid, Binance, Coinbase |
| HYPE | Hyperliquid | Exchange Token | Hyperliquid |

### Tokens
| Symbol | Name | Category | Exchanges |
|--------|------|----------|-----------|
| SPDR | SPDR Token | Token | Hyperliquid |
| GLAM | GLAM Token | Token | Hyperliquid |

### Layer 2 Solutions
| Symbol | Name | Category | Exchanges |
|--------|------|----------|-----------|
| AVAX | Avalanche | Layer 1 | Hyperliquid, Binance |
| MATIC | Polygon | Layer 2 | Hyperliquid, Binance |
| OP | Optimism | Layer 2 | Hyperliquid, Binance |
| ARB | Arbitrum | Layer 2 | Hyperliquid, Binance |

**Plus 200+ other cryptocurrencies on Hyperliquid!**

To see all available assets:
```python
from config import list_available_assets, print_all_assets
print_all_assets()
```

## 💡 Multi-Asset Comparison

Compare performance across different cryptocurrencies:

```python
from core import CryptoBacktester

assets = ["BTC", "ETH", "SOL", "SPDR", "GLAM"]
results = {}

for asset in assets:
    bt = CryptoBacktester(asset_symbol=asset, initial_capital=10000)
    bt.load_data(days=30, interval="1h")
    bt.calculate_indicators()
    metrics = bt.run_strategy('sma_crossover', allow_short=True)
    results[asset] = metrics
    
# Compare results
for asset, metrics in results.items():
    print(f"{asset}: {metrics['total_return']:.2f}% return, "
          f"{metrics['win_rate']:.2f}% win rate")
```

## 📁 Project Structure

```
crypto-backtest-engine/
├── core/                      # Core backtesting engine
│   ├── __init__.py
│   └── backtest_engine.py     # CryptoBacktester class
│
├── data_sources/              # Data fetchers for exchanges
│   ├── __init__.py
│   ├── base_fetcher.py        # Abstract base class
│   └── hyperliquid_fetcher.py # Hyperliquid implementation
│
├── config/                    # Configuration files
│   ├── __init__.py
│   └── assets.py              # Asset configurations
│
├── examples/                  # Example scripts
│   ├── quick_start.py
│   └── multi_asset_comparison.py
│
├── notebooks/                 # Jupyter notebooks
│   └── 01_quick_start.ipynb
│
├── tests/                     # Unit tests
│   └── test_backtest_engine.py
│
├── docs/                      # Documentation
│   ├── QUICKSTART.md
│   ├── HYPERLIQUID_GUIDE.md
│   └── MULTI_ASSET_GUIDE.md
│
├── setup.py                   # Package setup
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

## 🔧 Advanced Usage

### Custom Asset Configuration

Add your own assets to `config/assets.py`:

```python
ASSET_CONFIG = {
    "YOUR_TOKEN": {
        "name": "Your Token",
        "exchanges": ["hyperliquid"],
        "default_commission": 0.002,
        "min_investment": 100,
        "description": "Your custom token"
    }
}
```

### Parameter Optimization

Find optimal strategy parameters:

```python
best_return = -float('inf')
best_params = None

for fast in [10, 20, 30]:
    for slow in [50, 100, 200]:
        bt = CryptoBacktester(asset_symbol="BTC")
        bt.load_data(days=90, interval="1h")
        bt.calculate_indicators()
        metrics = bt.run_strategy('sma_crossover', 
                                 fast_period=fast, 
                                 slow_period=slow)
        
        if metrics['total_return'] > best_return:
            best_return = metrics['total_return']
            best_params = (fast, slow)

print(f"Best parameters: SMA({best_params[0]}/{best_params[1]}) "
      f"with {best_return:.2f}% return")
```

## 📈 Supported Data

### Timeframes
- **1m, 3m, 5m, 15m, 30m** (short-term)
- **1h, 2h, 4h, 8h, 12h** (medium-term) ⭐ Recommended
- **1d, 3d, 1w, 1M** (long-term)

### Data Limits (Hyperliquid)
- Hyperliquid stores **5000 most recent candles** per interval
- 1h candles: ~7 months history
- 4h candles: ~2.3 years history
- 1d candles: ~13.7 years history

## 🌐 24/7 Hosting

Deploy your backtesting system to run continuously:

```bash
# Quick deploy to DigitalOcean
bash server_setup.sh

# Access Jupyter remotely
# Open browser: http://YOUR_SERVER_IP:8888
```

**Complete guides:**
- [HOSTING_QUICKSTART.md](HOSTING_QUICKSTART.md) - 30-minute setup
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - All hosting options

## ⚠️ Important Notes

### Backtesting Limitations
Backtests don't account for:
- Slippage (price movement during order execution)
- Liquidity issues (large orders may not fill)
- Latency delays
- Market impact

### Risk Disclaimer
**Past performance ≠ future results**

This software is for **educational purposes only**. Always:
- Start with small capital
- Use stop losses in live trading
- Monitor performance regularly
- Do your own research

## 🤝 Contributing

Contributions welcome! To add support for new exchanges or assets:

1. Fork the repository
2. Create `data_sources/your_exchange_fetcher.py` inheriting from `BaseDataFetcher`
3. Add asset configs to `config/assets.py`
4. Submit a pull request

## 📝 License

MIT License - See LICENSE file for details

## 🔗 Links

- **Repository**: https://github.com/cktong/crypto-backtest-engine
- **Hyperliquid**: https://hyperliquid.xyz
- **Documentation**: https://hyperliquid.gitbook.io/hyperliquid-docs/

## 📧 Contact

- **GitHub**: [@cktong](https://github.com/cktong)
- **Issues**: [Report bugs](https://github.com/cktong/crypto-backtest-engine/issues)

## 🎉 Getting Started

1. **Clone the repository**: `git clone https://github.com/cktong/crypto-backtest-engine.git`
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Run quick start**: `python3 examples/quick_start.py`
4. **Try SPDR/GLAM**: Just change `asset_symbol="SPDR"` or `asset_symbol="GLAM"`!
5. **Deploy to cloud** (optional): Follow [HOSTING_QUICKSTART.md](HOSTING_QUICKSTART.md)

Happy backtesting across all markets! 📈🚀

---

**⭐ If you find this useful, please star the repository!**

**💡 Pro Tip**: Different assets perform differently with the same strategy. Always test multiple assets and strategies to find what works best for your trading style!
