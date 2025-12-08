# ⚡ Quick Reference Guide

## 🚀 Instant Start Commands

### Test Bitcoin
```bash
cd /home/user/webapp
python3 -c "
from core import CryptoBacktester
bt = CryptoBacktester(asset_symbol='BTC', initial_capital=10000)
bt.load_data(days=30, interval='1h')
bt.calculate_indicators()
metrics = bt.run_strategy('sma_crossover', allow_short=True)
bt.print_performance_report(metrics)
"
```

### Test SPDR
```bash
cd /home/user/webapp
python3 -c "
from core import CryptoBacktester
bt = CryptoBacktester(asset_symbol='SPDR', initial_capital=10000)
bt.load_data(days=30, interval='1h')
bt.calculate_indicators()
metrics = bt.run_strategy('sma_crossover', allow_short=True)
bt.print_performance_report(metrics)
"
```

### Test GLAM
```bash
cd /home/user/webapp
python3 -c "
from core import CryptoBacktester
bt = CryptoBacktester(asset_symbol='GLAM', initial_capital=10000)
bt.load_data(days=30, interval='1h')
bt.calculate_indicators()
metrics = bt.run_strategy('sma_crossover', allow_short=True)
bt.print_performance_report(metrics)
"
```

### Run Pre-built Examples
```bash
# Quick comparison of BTC, SPDR, GLAM
python3 examples/quick_start.py

# Full multi-asset analysis
python3 examples/multi_asset_comparison.py
```

---

## 📝 Code Snippets

### Basic Usage
```python
from core import CryptoBacktester

# Initialize for any asset
bt = CryptoBacktester(asset_symbol="SPDR", initial_capital=10000)

# Load data
bt.load_data(days=30, interval="1h")

# Calculate indicators
bt.calculate_indicators()

# Run strategy
metrics = bt.run_strategy('sma_crossover', allow_short=True)

# Print results
bt.print_performance_report(metrics)
```

### Compare Multiple Assets
```python
from core import CryptoBacktester

assets = ["BTC", "ETH", "SPDR", "GLAM"]

for asset in assets:
    bt = CryptoBacktester(asset_symbol=asset, initial_capital=10000)
    bt.load_data(days=30, interval="1h")
    bt.calculate_indicators()
    metrics = bt.run_strategy('sma_crossover', allow_short=True)
    print(f"{asset}: {metrics['total_return']:.2f}%")
```

### Test All Strategies
```python
from core import CryptoBacktester

strategies = ['sma_crossover', 'rsi_mean_reversion', 'macd_momentum', 
              'bollinger_bands', 'dual_momentum']

bt = CryptoBacktester(asset_symbol="SPDR", initial_capital=10000)
bt.load_data(days=30, interval="1h")
bt.calculate_indicators()

for strategy in strategies:
    metrics = bt.run_strategy(strategy, allow_short=True)
    print(f"{strategy}: {metrics['total_return']:.2f}%")
```

---

## 🔧 Configuration

### View All Available Assets
```python
from config import print_all_assets
print_all_assets()
```

### Get Asset Info
```python
from config import get_asset_config, print_asset_info

# Get config dictionary
config = get_asset_config("SPDR")
print(config)

# Print formatted info
print_asset_info("SPDR")
```

### List Assets by Category
```python
from config import get_assets_by_category

layer1 = get_assets_by_category("layer1")
tokens = get_assets_by_category("token")
print(f"Layer 1: {layer1}")
print(f"Tokens: {tokens}")
```

---

## 🎯 Supported Strategies

### 1. SMA Crossover
```python
metrics = bt.run_strategy('sma_crossover', 
                         fast_period=20, 
                         slow_period=50, 
                         allow_short=True)
```

### 2. RSI Mean Reversion
```python
metrics = bt.run_strategy('rsi_mean_reversion', 
                         oversold=30, 
                         overbought=70, 
                         allow_short=True)
```

### 3. MACD Momentum
```python
metrics = bt.run_strategy('macd_momentum', 
                         allow_short=True)
```

### 4. Bollinger Bands
```python
metrics = bt.run_strategy('bollinger_bands', 
                         allow_short=True)
```

### 5. Dual Momentum
```python
metrics = bt.run_strategy('dual_momentum', 
                         allow_short=True)
```

---

## 📊 Key Files Location

### Core Engine
- `core/backtest_engine.py` - Main CryptoBacktester class

### Data Fetchers
- `data_sources/base_fetcher.py` - Abstract base class
- `data_sources/hyperliquid_fetcher.py` - Hyperliquid implementation

### Configuration
- `config/assets.py` - All supported assets
- `config/assets.py` - Asset and exchange configs

### Examples
- `examples/quick_start.py` - Quick test of BTC, SPDR, GLAM
- `examples/multi_asset_comparison.py` - Full comparison tool

### Old Files (Backward Compatible)
- `bitcoin_backtest.py` - Original (still works)
- `hyperliquid_data_fetcher.py` - Original (still works)
- `backtest_with_hyperliquid.py` - Original example

---

## 🔗 Important Links

### Repository
- **Current**: https://github.com/cktong/trading
- **Recommended**: https://github.com/cktong/crypto-backtest-engine

### Pull Request
- https://github.com/cktong/trading/pull/1

### Documentation
- `README.md` - Main documentation
- `REFACTORING_SUMMARY.md` - What changed
- `NAMING_AND_DEPLOYMENT_GUIDE.md` - Rename guide
- `QUICK_REFERENCE.md` - This file

---

## 💡 Common Tasks

### Add a New Asset
Edit `config/assets.py`:
```python
ASSET_CONFIG["YOUR_TOKEN"] = {
    "name": "Your Token",
    "full_name": "Your Token Name",
    "exchanges": ["hyperliquid"],
    "default_commission": 0.002,
    "min_investment": 100,
    "description": "Your token description",
    "category": "token",
    "icon": "🪙"
}
```

### Test with Custom Data
```python
import pandas as pd
from core import CryptoBacktester

# Load your CSV
df = pd.read_csv('your_data.csv')

# Use it
bt = CryptoBacktester(asset_symbol="CUSTOM", initial_capital=10000)
bt.load_data(data=df, use_real_data=False)
bt.calculate_indicators()
metrics = bt.run_strategy('sma_crossover', allow_short=True)
```

### Export Trade History
```python
bt = CryptoBacktester(asset_symbol="SPDR", initial_capital=10000)
bt.load_data(days=30, interval="1h")
bt.calculate_indicators()
metrics = bt.run_strategy('sma_crossover', allow_short=True)

# Export to CSV
bt.export_trades('spdr_trades.csv')
```

---

## ⚙️ Git Commands

### Check Status
```bash
cd /home/user/webapp
git status
git log --oneline -5
```

### Pull Latest
```bash
git fetch origin
git pull origin main
```

### Switch Branches
```bash
# View branches
git branch -a

# Switch to feature branch
git checkout feature/multi-asset-support

# Back to main
git checkout main
```

---

## 🐛 Troubleshooting

### Import Errors
```python
# If you get import errors, add path
import sys
sys.path.insert(0, '/home/user/webapp')
from core import CryptoBacktester
```

### No Data Fetched
```python
# Test data fetcher directly
from data_sources import HyperliquidDataFetcher

fetcher = HyperliquidDataFetcher()
df = fetcher.fetch_for_backtest(coin="SPDR", interval="1h", days=7)
print(df.head())
```

### Asset Not Found
```python
# Check if asset exists
from config import list_available_assets, get_asset_config

# List all
assets = list_available_assets()
print(assets)

# Check specific
config = get_asset_config("SPDR")
print(config)
```

---

## 📈 Performance Tips

### Optimal Settings
```python
# Good balance of speed and data
bt.load_data(days=30, interval="1h")

# For quick tests
bt.load_data(days=7, interval="1h")

# For comprehensive analysis
bt.load_data(days=90, interval="4h")
```

### Memory Management
```python
# Process one asset at a time for large datasets
for asset in ["BTC", "ETH", "SPDR", "GLAM"]:
    bt = CryptoBacktester(asset_symbol=asset)
    # ... process
    del bt  # Free memory
```

---

## ✅ Checklist

### First Time Setup
- [ ] Clone repository
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Test Bitcoin: `python3 examples/quick_start.py`
- [ ] Test SPDR/GLAM: examples run automatically

### Daily Development
- [ ] Pull latest: `git pull origin main`
- [ ] Test your changes
- [ ] Commit: `git add . && git commit -m "message"`
- [ ] Push: `git push origin branch-name`

### Before Deployment
- [ ] Test all examples
- [ ] Check documentation is updated
- [ ] Verify all imports work
- [ ] Run quick backtest on each asset

---

## 🎉 Success!

You now have a universal cryptocurrency backtesting engine ready for:
- ✅ Bitcoin (BTC)
- ✅ Ethereum (ETH)
- ✅ SPDR Token
- ✅ GLAM Token
- ✅ 200+ other cryptocurrencies

**Quick Test**: `python3 examples/quick_start.py`

**Full Analysis**: `python3 examples/multi_asset_comparison.py`

**Questions?** Check `README.md` or `REFACTORING_SUMMARY.md`
