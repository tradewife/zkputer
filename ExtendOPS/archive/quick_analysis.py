#!/usr/bin/env python3
"""
Quick market check and $1000 setup analysis
"""

import asyncio
import sys
import os

sys.path.append("/home/kt/ZKputer/ExtendOPS/📊 Core Trading System")
from extended_executor import ExtendedExecutor

async def main():
    executor = ExtendedExecutor()
    if not await executor.initialize():
        return

    #Get account
    balance = await executor.trading_client.account.get_balance()
    equity = float(balance.data.equity)
    
    print(f"\n💰 ACCOUNT: ${equity:.2f}")
    print(f"📊 TARGET NOTIONAL: $1,000")
    print(f"⚡ REQUIRED LEVERAGE: ~{1000/equity:.1f}x\n")
    
    # Get market data
    markets = await executor.trading_client.markets_info.get_markets()
    
    print("📊 MARKET PRICES (Real-Time)\n")
    
    key_markets = {
        "BTC-USD": {"type": "Major", "min_lev": 10},
        "ETH-USD": {"type": "Major", "min_lev": 10},
        "SOL-USD": {"type": "Alt", "min_lev": 10},
        "HYPE-USD": {"type": "Alt", "min_lev": 10},
        "ADA-USD": {"type": "Alt", "min_lev": 10}
    }
    
    results = []
    for market_data in markets.data:
        if market_data.name in key_markets:
            stats = market_data.market_stats
            
            price = float(stats.last_price)
            funding = float(stats.funding_rate) * 100
            vol_24h = float(stats.daily_volume)
            
            results.append({
                "market": market_data.name,
                "price": price,
                "funding": funding,
                "volume": vol_24h
            })
            
            # Calculate size for $1000 exposure
            size_for_1000 = 1000 / price
            
            print(f"{market_data.name}:")
            print(f"  Price: ${price:,.2f}")
            print(f"  Funding: {funding:.4f}%")
            print(f"  24h Vol: ${vol_24h/1e6:.1f}M")
            print(f"  For $1000: {size_for_1000:.4f} contracts @ ~{1000/equity:.0f}x leverage")
            print()
    
    # Analysis
    print("\n🎯 SETUP ANALYSIS:")
    print("=" * 50)
    
    # Find best setup based on funding and momentum
    for r in results:
        if r["market"] == "BTC-USD":
            if r["price"] > 92000:
                print(f"✅ BTC: Bullish momentum (${r['price']:,.0f})")
                print(f"   → Long bias if holds $92k support")
        
        if r["market"] == "ADA-USD":
            if r["funding"] < -0.001:
                print(f"✅ ADA: Negative funding ({r['funding']:.4f}%)")
                print(f"   → Short opportunity (arbitrage)")
        
        if r["market"] == "ETH-USD":
            if 3000 < r["price"] < 3100:
                print(f"✅ ETH: Range-bound (${r['price']:,.0f})")
                print(f"   → Mean reversion potential")

if __name__ == "__main__":
    asyncio.run(main())
