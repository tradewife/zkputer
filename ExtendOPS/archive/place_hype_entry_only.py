#!/usr/bin/env python3
"""
Place HYPE Long - Entry Only (No TP/SL)
"""

import asyncio
import sys
sys.path.insert(0, '/home/kt/ZKputer/HyperOPS/📊 Core Trading System')
from trading_module import TradingConfig, ExtendedTrader, OrderSpec

async def place_hype_entry():
    config = TradingConfig.from_file('/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json')
    trader = ExtendedTrader(config)
    await trader.initialize()
    
    # Get current HYPE price
    market_data = await trader.get_market_data(['HYPE-USD'])
    hype = market_data.get('HYPE-USD', {})
    mark = hype.get('mark_price', 31.00)
    
    print(f"HYPE Mark Price: ${mark:.2f}")
    
    # Place entry ONLY, no TP/SL
    entry_price = round(mark + 0.10, 2)  # Slightly above market
    size = 15.0
    
    print(f"\n🚀 Placing HYPE Long Entry ONLY")
    print(f"   Size: {size} @ ${entry_price}")
    print(f"   NO stop loss or take profit attached")
    
    entry_order = OrderSpec(
        symbol="HYPE-USD",
        side="buy",
        order_type="limit",
        size=size,
        price=entry_price,
        reduce_only=False,
        post_only=False
    )
    
    res = await trader.place_order(entry_order)
    
    if res.get("status") == "ok":
        print(f"\n✅ ENTRY PLACED")
        print(f"   Order ID: {res['order_id']}")
        print(f"   {size} HYPE @ ${entry_price}")
        print(f"\n⚠️ NAKED POSITION - Add stops manually after fill")
    else:
        print(f"\n❌ Failed: {res.get('error')}")
    
    await trader.cleanup()

asyncio.run(place_hype_entry())
