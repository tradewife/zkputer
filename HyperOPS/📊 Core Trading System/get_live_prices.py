#!/usr/bin/env python3
"""
Get REAL-TIME Extended market prices NOW
"""
import asyncio
import json
import sys
from datetime import datetime
sys.path.insert(0, '/home/kt/ZKputer/HyperOPS/📊 Core Trading System')

from trading_module import TradingConfig, ExtendedTrader

async def get_live_prices():
    config = TradingConfig.from_file(
        "/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json"
    )
    
    trader = ExtendedTrader(config)
    await trader.initialize()
    
    print(f"🔴 LIVE PRICES - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Get real-time data
    focus = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'XRP-USD', 'HYPE-USD']
    markets = await trader.get_market_data(focus)
    
    for symbol in focus:
        if symbol in markets:
            data = markets[symbol]
            last = data.get('last_price', 0)
            mark = data.get('mark_price', 0)
            funding = data.get('funding_rate', 0)
            vol = data.get('daily_volume', 0)
            
            print(f"{symbol:12} Last: ${last:>12.2f} | Mark: ${mark:>12.2f} | Fund: {funding*100:>+7.4f}% | Vol: ${vol/1e6:>6.1f}M")
    
    await trader.cleanup()

if __name__ == "__main__":
    asyncio.run(get_live_prices())
