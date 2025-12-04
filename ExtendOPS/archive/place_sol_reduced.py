#!/usr/bin/env python3
"""
Place SOL Short with Reduced Size
Adjusted for $55 available balance
"""

import asyncio
import sys
sys.path.insert(0, '/home/kt/ZKputer/HyperOPS/📊 Core Trading System')

from trading_module import TradingConfig, ExtendedTrader, OrderSpec

async def place_sol_reduced():
    config = TradingConfig.from_file(
        "/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json"
    )
    
    trader = ExtendedTrader(config)
    if not await trader.initialize():
        print("Failed to initialize")
        return

    print("🚀 Placing SOL-USD Short (Reduced Size)...")
    print("   Available Balance: $55.15")
    print("   Target Notional: ~$545 @ 10x = $54.50 margin")
    
    # 4.0 SOL @ $136.50 = $546 notional / 10x = $54.60 margin (fits!)
    sol_order = OrderSpec(
        symbol="SOL-USD",
        side="sell",
        order_type="limit",
        size=4.0,
        price=136.50,
        post_only=True,
        stop_loss_price=140.00,
        take_profit_price=132.00
    )
    
    res = await trader.place_order(sol_order)
    
    if res.get("status") == "ok":
        print(f"✅ SOL Short Placed: 4.0 @ $136.50")
        print(f"   Order ID: {res['order_id']}")
        print(f"   SL: $140 | TP: $132")
        print(f"   Risk: ~$14 | Profit: ~$18")
    else:
        print(f"❌ Failed: {res.get('error')}")

    await trader.cleanup()

if __name__ == "__main__":
    asyncio.run(place_sol_reduced())
