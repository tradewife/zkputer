#!/usr/bin/env python3
"""
Extended Market Data Fetcher
Get market prices, funding rates, OI, volume from Extended API
"""

import asyncio
import sys
import os
from typing import List, Dict, Optional

sys.path.append(os.path.dirname(__file__))
from extended_executor import ExtendedExecutor


async def get_market_data(markets: Optional[List[str]] = None) -> List[Dict]:
    """
    Get market data from Extended API
    
    Args:
        markets: List of market names (e.g. ["BTC-USD", "ETH-USD"])
                If None, gets data for default key markets
    
    Returns:
        List of dicts with market data
    """
    if markets is None:
        markets = ["BTC-USD", "ETH-USD", "SOL-USD", "HYPE-USD", "ADA-USD"]
    
    executor = ExtendedExecutor()
    if not await executor.initialize():
        return []
    
    try:
        all_markets = await executor.trading_client.markets_info.get_markets()
        
        results = []
        for market_data in all_markets.data:
            if market_data.name in markets:
                stats = market_data.market_stats
                
                results.append({
                    "market": market_data.name,
                    "price": float(stats.last_price),
                    "mark_price": float(stats.mark_price),
                    "funding_rate": float(stats.funding_rate) * 100,  # Convert to %
                    "volume_24h": float(stats.daily_volume),
                    "open_interest": float(stats.open_interest),
                })
        
        return results
    
    except Exception as e:
        print(f"❌ Failed to get market data: {e}")
        return []


async def print_market_snapshot():
    """Print formatted market snapshot"""
    data = await get_market_data()
    
    if not data:
        return
    
    print("\n📊 EXTENDED MARKET SNAPSHOT\n")
    
    for market in data:
        print(f"{market['market']}:")
        print(f"  Price: ${market['price']:,.2f}")
        print(f"  Mark: ${market['mark_price']:,.2f}")
        print(f"  Funding: {market['funding_rate']:.4f}%")
        print(f"  24h Vol: ${market['volume_24h'] / 1e6:.1f}M")
        print(f"  OI: ${market['open_interest'] / 1e6:.1f}M")
        print()


if __name__ == "__main__":
    asyncio.run(print_market_snapshot())
