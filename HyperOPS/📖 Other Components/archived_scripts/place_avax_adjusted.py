#!/usr/bin/env python3
"""
Place Adjusted AVAX Long Order
Sized for $27.47 available margin
"""

import asyncio
import sys
sys.path.insert(0, '/home/kt/ZKputer/HyperOPS/📊 Core Trading System')

from trading_module import TradingConfig, ExtendedTrader, OrderSpec

async def place_avax_adjusted():
    config = TradingConfig.from_file(
        "/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json"
    )
    
    trader = ExtendedTrader(config)
    if not await trader.initialize():
        print("Failed to initialize")
        return

    print("🚀 Placing AVAX-USD Long (Adjusted Size)...")
    print("   Available Margin: $27.47")
    
    # Calculate max size:
    # $27 margin @ 10x = $270 notional
    # $270 / $14 = 19.28 AVAX
    # Conservative: 19 AVAX = $266 notional / 10x = $26.60 margin
    
    avax_order = OrderSpec(
        symbol="AVAX-USD",
        side="buy",
        order_type="limit",
        size=19.0,
        price=14.00,
        post_only=True,
        stop_loss_price=13.30,
        take_profit_price=15.00
    )
    
    print(f"   Size: 19 AVAX @ $14.00")
    print(f"   Notional: ~$266 @ 10x = ~$26.60 margin")
    print(f"   SL: $13.30 | TP: $15.00")
    print(f"   Risk: ~$13.30 | Profit: ~$19.00")
    
    res = await trader.place_order(avax_order)
    
    if res.get("status") == "ok":
        print(f"\n✅ AVAX Long Placed Successfully!")
        print(f"   Order ID: {res['order_id']}")
    else:
        print(f"\n❌ Failed: {res.get('error')}")

    await trader.cleanup()

if __name__ == "__main__":
    asyncio.run(place_avax_adjusted())
