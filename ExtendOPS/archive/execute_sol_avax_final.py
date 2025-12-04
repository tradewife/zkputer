#!/usr/bin/env python3
"""
Execute SOL Short and AVAX Long with Integrated TP/SL
Final execution script with proper leverage and attached stop/targets
"""

import asyncio
import sys
sys.path.insert(0, '/home/kt/ZKputer/HyperOPS/📊 Core Trading System')

from trading_module import TradingConfig, ExtendedTrader, OrderSpec

async def execute_final():
    config = TradingConfig.from_file(
        "/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json"
    )
    
    trader = ExtendedTrader(config)
    if not await trader.initialize():
        print("Failed to initialize trader")
        return

    print("🚀 EXECUTING SOL & AVAX TRADES (Final)")
    print("=" * 80)
    
    # TRADE 1: SOL SHORT with integrated TP/SL
    sol_order = OrderSpec(
        symbol="SOL-USD",
        side="sell",
        order_type="limit",
        size=7.0,
        price=136.50,
        post_only=True,
        stop_loss_price=140.00,    # Attached SL
        take_profit_price=132.00   # Attached TP1 (will use 50% size)
    )
    
    print("\n1️⃣ SOL-USD Short (Entry + SL + TP)...")
    res_sol = await trader.place_order(sol_order)
    if res_sol.get("status") == "ok":
        print(f"✅ SOL Short Placed: 7.0 @ $136.50 | SL: $140 | TP: $132")
    else:
        print(f"❌ SOL Short Failed: {res_sol.get('error')}")

    # TRADE 2: AVAX LONG with integrated TP/SL
    avax_order = OrderSpec(
        symbol="AVAX-USD",
        side="buy",
        order_type="limit",
        size=65.0,
        price=14.00,
        post_only=True,
        stop_loss_price=13.30,     # Attached SL
        take_profit_price=15.00    # Attached TP1
    )
    
    print("\n2️⃣ AVAX-USD Long (Entry + SL + TP)...")
    res_avax = await trader.place_order(avax_order)
    if res_avax.get("status") == "ok":
        print(f"✅ AVAX Long Placed: 65.0 @ $14.00 | SL: $13.30 | TP: $15.00")
    else:
        print(f"❌ AVAX Long Failed: {res_avax.get('error')}")

    await trader.cleanup()
    
    print("\n" + "=" * 80)
    print("✅ Execution Complete - Check Extended UI for order status")

if __name__ == "__main__":
    asyncio.run(execute_final())
