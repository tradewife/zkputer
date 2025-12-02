#!/usr/bin/env python3
"""
Execute SOL Short and AVAX Long - Conservative Sizing
Adjusted for $83 account balance
"""

import asyncio
import sys
sys.path.insert(0, '/home/kt/ZKputer/HyperOPS/📊 Core Trading System')

from trading_module import TradingConfig, ExtendedTrader, OrderSpec

async def execute_conservative():
    config = TradingConfig.from_file(
        "/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json"
    )
    
    trader = ExtendedTrader(config)
    if not await trader.initialize():
        print("Failed to initialize trader")
        return

    print("🚀 EXECUTING SOL & AVAX TRADES (Conservative Sizing)")
    print("=" * 80)
    print("Account: $83 | Max Risk: ~$16.60/trade (20%)")
    
    # TRADE 1: SOL SHORT
    # Entry: $136.50, Stop: $140.00, Risk: $3.50/unit
    # Max size: $16.60 / $3.50 = 4.74 SOL
    # Conservative: 4.5 SOL (~$614 notional @ 10x = $61.40 margin)
    sol_order = OrderSpec(
        symbol="SOL-USD",
        side="sell",
        order_type="limit",
        size=4.5,
        price=136.50,
        post_only=True,
        stop_loss_price=140.00,
        take_profit_price=132.00
    )
    
    print("\n1️⃣ SOL-USD Short: 4.5 @ $136.50...")
    print(f"   Notional: ~$614 | Margin @ 10x: ~$61")
    print(f"   SL: $140 | Risk: ~$15.75")
    res_sol = await trader.place_order(sol_order)
    if res_sol.get("status") == "ok":
        print(f"✅ SOL Short Placed Successfully")
    else:
        print(f"❌ SOL Short Failed: {res_sol.get('error')}")

    await asyncio.sleep(1)

    # TRADE 2: AVAX LONG
    # Entry: $14.00, Stop: $13.30, Risk: $0.70/unit
    # Max size: $16.60 / $0.70 = 23.7 AVAX
    # Conservative: 20 AVAX (~$280 notional @ 10x = $28 margin)
    avax_order = OrderSpec(
        symbol="AVAX-USD",
        side="buy",
        order_type="limit",
        size=20.0,
        price=14.00,
        post_only=True,
        stop_loss_price=13.30,
        take_profit_price=15.00
    )
    
    print("\n2️⃣ AVAX-USD Long: 20 @ $14.00...")
    print(f"   Notional: ~$280 | Margin @ 10x: ~$28")
    print(f"   SL: $13.30 | Risk: ~$14")
    res_avax = await trader.place_order(avax_order)
    if res_avax.get("status") == "ok":
        print(f"✅ AVAX Long Placed Successfully")
    else:
        print(f"❌ AVAX Long Failed: {res_avax.get('error')}")

    await trader.cleanup()
    
    print("\n" + "=" * 80)
    print("✅ Execution Attempt Complete")

if __name__ == "__main__":
    asyncio.run(execute_conservative())
