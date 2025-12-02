#!/usr/bin/env python3
"""
Close SOL Short - Fixed Precision
"""

import asyncio
import sys
sys.path.insert(0, '/home/kt/ZKputer/HyperOPS/📊 Core Trading System')
from trading_module import TradingConfig, ExtendedTrader, OrderSpec

async def close_sol_fixed():
    config = TradingConfig.from_file('/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json')
    trader = ExtendedTrader(config)
    await trader.initialize()
    
    positions = await trader.get_positions()
    sol_pos = None
    for p in positions:
        if p.symbol == "SOL-USD":
            sol_pos = p
            break
    
    if not sol_pos:
        print("❌ No SOL position found")
        await trader.cleanup()
        return
    
    print(f"SOL Position:")
    print(f"  Entry: ${sol_pos.entry_price:.2f}")
    print(f"  Mark: ${sol_pos.mark_price:.2f}")
    print(f"  PnL: ${sol_pos.unrealized_pnl:.2f} ✅")
    print(f"\n🔄 Closing with market order...")
    
    # Market order with NO price parameter for IOC
    close_order = OrderSpec(
        symbol="SOL-USD",
        side="buy",
        order_type="market",
        size=abs(sol_pos.size),
        # price=None for market orders
        reduce_only=True
    )
    
    res = await trader.place_order(close_order)
    
    if res.get("status") == "ok":
        print(f"\n🎉 SOL SHORT CLOSED!")
        print(f"   Profit: +${sol_pos.unrealized_pnl:.2f}")
        print(f"   Trade: SHORT {sol_pos.size} @ ${sol_pos.entry_price:.2f} → ${sol_pos.mark_price:.2f}")
    else:
        print(f"\n❌ Failed: {res.get('error')}")
    
    await trader.cleanup()

asyncio.run(close_sol_fixed())
