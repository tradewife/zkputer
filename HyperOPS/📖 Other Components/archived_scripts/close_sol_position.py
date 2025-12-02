#!/usr/bin/env python3
"""
Close SOL Short Position
Market order to exit
"""

import asyncio
import sys
sys.path.insert(0, '/home/kt/ZKputer/HyperOPS/📊 Core Trading System')
from trading_module import TradingConfig, ExtendedTrader, OrderSpec

async def close_sol():
    config = TradingConfig.from_file('/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json')
    trader = ExtendedTrader(config)
    await trader.initialize()
    
    # Check current position
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
    
    print(f"Current SOL Position:")
    print(f"  Size: {sol_pos.side.upper()} {sol_pos.size}")
    print(f"  Entry: ${sol_pos.entry_price:.2f}")
    print(f"  Mark: ${sol_pos.mark_price:.2f}")
    print(f"  PnL: ${sol_pos.unrealized_pnl:.2f}")
    print(f"\n🔄 Closing position with market order...")
    
    # Close with market order (buy to close short)
    close_order = OrderSpec(
        symbol="SOL-USD",
        side="buy",  # Buy to close short
        order_type="market",
        size=abs(sol_pos.size),
        price=sol_pos.mark_price,
        reduce_only=True
    )
    
    res = await trader.place_order(close_order)
    
    if res.get("status") == "ok":
        print(f"\n✅ SOL Position CLOSED")
        print(f"   Final PnL: ${sol_pos.unrealized_pnl:.2f}")
    else:
        print(f"\n❌ Failed to close: {res.get('error')}")
    
    await trader.cleanup()

asyncio.run(close_sol())
