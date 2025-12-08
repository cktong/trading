"""
Asset Configuration System
===========================
Configuration for different cryptocurrency assets supported by the backtesting engine.

Author: AI Assistant
Date: 2025
"""

from typing import Dict, List, Optional


# Comprehensive asset configuration
ASSET_CONFIG = {
    "BTC": {
        "name": "Bitcoin",
        "full_name": "Bitcoin",
        "exchanges": ["hyperliquid", "binance", "coinbase", "kraken"],
        "default_commission": 0.001,
        "min_investment": 100,
        "description": "The world's first and most popular cryptocurrency",
        "category": "layer1",
        "icon": "₿"
    },
    "ETH": {
        "name": "Ethereum",
        "full_name": "Ethereum",
        "exchanges": ["hyperliquid", "binance", "coinbase", "kraken"],
        "default_commission": 0.001,
        "min_investment": 50,
        "description": "Leading smart contract platform",
        "category": "layer1",
        "icon": "Ξ"
    },
    "SOL": {
        "name": "Solana",
        "full_name": "Solana",
        "exchanges": ["hyperliquid", "binance", "coinbase"],
        "default_commission": 0.001,
        "min_investment": 20,
        "description": "High-performance blockchain for DeFi and NFTs",
        "category": "layer1",
        "icon": "◎"
    },
    "HYPE": {
        "name": "Hyperliquid",
        "full_name": "Hyperliquid",
        "exchanges": ["hyperliquid"],
        "default_commission": 0.001,
        "min_investment": 10,
        "description": "Hyperliquid native token",
        "category": "exchange_token",
        "icon": "⚡"
    },
    "SPDR": {
        "name": "SPDR",
        "full_name": "SPDR Token",
        "exchanges": ["hyperliquid"],
        "default_commission": 0.002,
        "min_investment": 100,
        "description": "SPDR trading token",
        "category": "token",
        "icon": "🕷️"
    },
    "GLAM": {
        "name": "GLAM",
        "full_name": "GLAM Token",
        "exchanges": ["hyperliquid"],
        "default_commission": 0.002,
        "min_investment": 50,
        "description": "GLAM project token",
        "category": "token",
        "icon": "✨"
    },
    "AVAX": {
        "name": "Avalanche",
        "full_name": "Avalanche",
        "exchanges": ["hyperliquid", "binance", "coinbase"],
        "default_commission": 0.001,
        "min_investment": 30,
        "description": "Fast and scalable blockchain platform",
        "category": "layer1",
        "icon": "🔺"
    },
    "MATIC": {
        "name": "Polygon",
        "full_name": "Polygon (MATIC)",
        "exchanges": ["hyperliquid", "binance", "coinbase"],
        "default_commission": 0.001,
        "min_investment": 10,
        "description": "Ethereum scaling solution",
        "category": "layer2",
        "icon": "⬡"
    },
    "OP": {
        "name": "Optimism",
        "full_name": "Optimism",
        "exchanges": ["hyperliquid", "binance", "coinbase"],
        "default_commission": 0.001,
        "min_investment": 20,
        "description": "Ethereum layer 2 scaling solution",
        "category": "layer2",
        "icon": "🔴"
    },
    "ARB": {
        "name": "Arbitrum",
        "full_name": "Arbitrum",
        "exchanges": ["hyperliquid", "binance", "coinbase"],
        "default_commission": 0.001,
        "min_investment": 20,
        "description": "Ethereum layer 2 scaling solution",
        "category": "layer2",
        "icon": "🔵"
    }
}


def get_asset_config(symbol: str) -> Dict:
    """
    Get configuration for a specific asset.
    
    Args:
        symbol: Asset symbol (e.g., "BTC", "ETH", "SPDR")
        
    Returns:
        Dictionary with asset configuration, defaults to BTC config if not found
    """
    symbol = symbol.upper()
    
    if symbol in ASSET_CONFIG:
        return ASSET_CONFIG[symbol].copy()
    else:
        # Return a default configuration for unknown assets
        return {
            "name": symbol,
            "full_name": symbol,
            "exchanges": ["hyperliquid"],
            "default_commission": 0.001,
            "min_investment": 100,
            "description": f"{symbol} cryptocurrency",
            "category": "unknown",
            "icon": "💎"
        }


def get_asset_name(symbol: str) -> str:
    """
    Get display name for an asset.
    
    Args:
        symbol: Asset symbol
        
    Returns:
        Human-readable asset name
    """
    config = get_asset_config(symbol)
    return config["name"]


def get_asset_commission(symbol: str) -> float:
    """
    Get default commission rate for an asset.
    
    Args:
        symbol: Asset symbol
        
    Returns:
        Default commission rate (e.g., 0.001 = 0.1%)
    """
    config = get_asset_config(symbol)
    return config["default_commission"]


def list_available_assets() -> List[str]:
    """
    Get list of all configured assets.
    
    Returns:
        List of asset symbols
    """
    return sorted(ASSET_CONFIG.keys())


def get_assets_by_category(category: str) -> List[str]:
    """
    Get assets filtered by category.
    
    Args:
        category: Category name (e.g., "layer1", "layer2", "token")
        
    Returns:
        List of asset symbols in that category
    """
    return [
        symbol for symbol, config in ASSET_CONFIG.items()
        if config.get("category") == category
    ]


def get_assets_by_exchange(exchange: str) -> List[str]:
    """
    Get assets available on a specific exchange.
    
    Args:
        exchange: Exchange name (e.g., "hyperliquid", "binance")
        
    Returns:
        List of asset symbols available on that exchange
    """
    exchange = exchange.lower()
    return [
        symbol for symbol, config in ASSET_CONFIG.items()
        if exchange in config.get("exchanges", [])
    ]


def print_asset_info(symbol: str):
    """
    Print detailed information about an asset.
    
    Args:
        symbol: Asset symbol
    """
    config = get_asset_config(symbol)
    
    print(f"\n{'='*60}")
    print(f"{config['icon']} {config['full_name']} ({symbol})")
    print(f"{'='*60}")
    print(f"Description:      {config['description']}")
    print(f"Category:         {config['category']}")
    print(f"Exchanges:        {', '.join(config['exchanges'])}")
    print(f"Commission:       {config['default_commission']*100:.2f}%")
    print(f"Min Investment:   ${config['min_investment']}")
    print(f"{'='*60}\n")


def print_all_assets():
    """Print information about all configured assets."""
    print("\n" + "="*60)
    print("SUPPORTED CRYPTOCURRENCIES")
    print("="*60)
    
    for category in ["layer1", "layer2", "exchange_token", "token"]:
        assets = get_assets_by_category(category)
        if assets:
            print(f"\n{category.upper().replace('_', ' ')}:")
            for symbol in assets:
                config = ASSET_CONFIG[symbol]
                print(f"  {config['icon']} {symbol:6s} - {config['name']}")
    
    print(f"\n{'='*60}")
    print(f"Total Assets: {len(ASSET_CONFIG)}")
    print(f"{'='*60}\n")


# Exchange configuration
EXCHANGE_CONFIG = {
    "hyperliquid": {
        "name": "Hyperliquid",
        "api_url": "https://api.hyperliquid.xyz/info",
        "max_candles": 5000,
        "supported_intervals": ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "8h", "12h", "1d", "3d", "1w", "1M"],
        "rate_limit": 2,  # requests per second
        "requires_auth": False
    },
    "binance": {
        "name": "Binance",
        "api_url": "https://api.binance.com",
        "max_candles": 1000,
        "supported_intervals": ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"],
        "rate_limit": 10,
        "requires_auth": False
    },
    "coinbase": {
        "name": "Coinbase",
        "api_url": "https://api.exchange.coinbase.com",
        "max_candles": 300,
        "supported_intervals": ["1m", "5m", "15m", "1h", "6h", "1d"],
        "rate_limit": 3,
        "requires_auth": False
    }
}


def get_exchange_config(exchange: str) -> Dict:
    """
    Get configuration for a specific exchange.
    
    Args:
        exchange: Exchange name
        
    Returns:
        Dictionary with exchange configuration
    """
    exchange = exchange.lower()
    return EXCHANGE_CONFIG.get(exchange, EXCHANGE_CONFIG["hyperliquid"])


if __name__ == "__main__":
    # Demo usage
    print_all_assets()
    
    # Print details for specific assets
    for symbol in ["BTC", "SPDR", "GLAM"]:
        print_asset_info(symbol)
