#!/usr/bin/env python3
"""
Place Conservative AVAX Order
Smaller size, no post-only to ensure execution
"""

import asyncio
import sys
sys.path.insert(0, '/home/kt/ZKputer/HyperOPS/📊 Core Trading System')

from trading_module import TradingConfig, ExtendedTrader, OrderSpec

async def place_avax_conservative():
    config = TradingConfig.from_file(
        "/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json"
    )
    
    trader = ExtendedTrader(config)
    if not await trader.initialize():
        print("Failed to initialize")
        return

    print("🚀 Placing AVAX-USD Long (Conservative)...")
    account = await trader.get_account_state()
    print(f"   Available: ${account['available_balance']:.2f}")
    
    # Very conservative sizing
    # Available: $27.72
    # Try 15 AVAX = $210 notional / 10x = $21 margin (safe buffer)
    
    avax_order = OrderSpec(
        symbol="AVAX-USD",
        side="buy",
        order_type="limit",
        size=15.0,
        price=14.05,  # Slightly above market to ensure fill
        post_only=False,  # Allow taker to ensure execution
        stop_loss_price=13.30,
        take_profit_price=15.00
    )
    
    print(f"   Size: 15 AVAX @ $14.05")
    print(f"   Notional: ~$211 @ 10x = ~$21 margin")
    print(f"   SL: $13.30 | TP: $15.00")
    print(f"   Risk: ~$11.25 | Profit: ~$14.25")
    
    res = await trader.place_order(avax_order)
    
    if res.get("status") == "ok":
        print(f"\n✅ AVAX Long Placed!")
        print(f"   Order ID: {res['order_id']}")
    else:
        print(f"\n❌ Failed: {res.get('error')}")
        
    # Double check it's there
    await asyncio.sleep(1)
    orders = await trader.get_open_orders()
    print(f"\n📋 Verification - Open orders: {len(orders)}")
    for o in orders:
        print(f"   {o['symbol']} {o['side'].upper()} {o['size']}")

    await trader.cleanup()

if __name__ == "__main__":
    asyncio.run(place_avax_conservative())
