#!/usr/bin/env python3
"""
Get Extended market data for daily routine
"""

import asyncio
import json
import sys
sys.path.insert(0, '/home/kt/ZKputer/HyperOPS/📊 Core Trading System')

from trading_module import TradingConfig, ExtendedTrader
from datetime import datetime

async def get_daily_market_data():
    """Fetch Extended market data for daily analysis"""
    
    # Load config
    config = TradingConfig.from_file(
        "/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json"
    )
    
    trader = ExtendedTrader(config)
    await trader.initialize()
    
    print(f"📊 EXTENDED MARKET DATA - {datetime.now().strftime('%Y-%m-%d %H:%M %Z')}")
    print("=" * 80)
    
    # Get account state
    account = await trader.get_account_state()
    print(f"\n💰 Account Status:")
    print(f"   Equity: ${account['equity']:.2f}")
    print(f"   Available: ${account['available_balance']:.2f}")
    print(f"   Max Risk/Trade: ${account['equity'] * 0.20:.2f} (20%)")
    
    # Get all markets
    print(f"\n📈 Fetching market data...")
    all_markets = await trader.get_market_data()
    
    # Filter for volume and OI
    filtered_markets = {}
    for symbol, data in all_markets.items():
        if data['daily_volume'] and data['daily_volume'] > 500000:  # $500K min volume
            filtered_markets[symbol] = data
    
    # Sort by volume
    sorted_markets = sorted(
        filtered_markets.items(),
        key=lambda x: x[1]['daily_volume'] or 0,
        reverse=True
    )
    
    print(f"\n🔝 Top 20 Markets by Volume (Min $500K/24h):")
    print(f"{'Symbol':<15} {'Mark Price':<15} {'24h Volume':<18} {'OI':<18} {'Funding%':<12}")
    print("-" * 80)
    
    for i, (symbol, data) in enumerate(sorted_markets[:20]):
        mark_price = f"${data['mark_price']:.6f}" if data['mark_price'] else "N/A"
        volume = f"${data['daily_volume']/1e6:.2f}M" if data['daily_volume'] else "N/A"
        oi = f"${data['open_interest']/1e6:.2f}M" if data['open_interest'] else "N/A"
        funding = f"{data['funding_rate']*100:.4f}%" if data['funding_rate'] else "N/A"
        
        print(f"{symbol:<15} {mark_price:<15} {volume:<18} {oi:<18} {funding:<12}")
    
    # Focus assets
    focus_symbols = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'XRP-USD', 'AVAX-USD']
    print(f"\n⭐ Core Focus Assets:")
    print(f"{'Symbol':<12} {'Last Price':<15} {'Funding%':<12} {'24h Vol':<15} {'OI':<15}")
    print("-" * 70)
    
    for symbol in focus_symbols:
        if symbol in all_markets:
            data = all_markets[symbol]
            price = f"${data['last_price']:.2f}" if data.get('last_price') else "N/A"
            funding = f"{data['funding_rate']*100:.4f}%" if data.get('funding_rate') else "N/A"
            volume = f"${data['daily_volume']/1e6:.1f}M" if data.get('daily_volume') else "N/A"
            oi = f"${data['open_interest']/1e6:.1f}M" if data.get('open_interest') else "N/A"
            
            print(f"{symbol:<12} {price:<15} {funding:<12} {volume:<15} {oi:<15}")
    
    # Check for extreme funding
    print(f"\n⚡ Funding Extremes (>±0.05%):")
    extreme_funding = []
    for symbol, data in all_markets.items():
        if data.get('funding_rate'):
            if abs(data['funding_rate']) > 0.0005:  # 0.05%
                extreme_funding.append((symbol, data['funding_rate'], data.get('daily_volume', 0)))
    
    extreme_funding.sort(key=lambda x: abs(x[1]), reverse=True)
    
    if extreme_funding:
        for symbol, funding, volume in extreme_funding[:10]:
            vol_str = f"${volume/1e6:.1f}M" if volume else "N/A"
            print(f"   {symbol:<15} {funding*100:+.4f}%  (Vol: {vol_str})")
    else:
        print(f"   No extreme funding rates found")
    
    # Cleanup
    await trader.cleanup()
    
    # Return data for further analysis
    return {
        'account': account,
        'all_markets': all_markets,
        'top_volume': sorted_markets[:20],
        'extreme_funding': extreme_funding
    }

if __name__ == "__main__":
    data = asyncio.run(get_daily_market_data())
