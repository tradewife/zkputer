#!/usr/bin/env python3
"""
Close SOL with LIMIT order at market price
Workaround for precision issues
"""

import asyncio
import sys
from decimal import Decimal
sys.path.insert(0, '/home/kt/ZKputer/HyperOPS/📊 Core Trading System')
from trading_module import TradingConfig, ExtendedTrader, OrderSpec

async def close_sol_limit():
    config = TradingConfig.from_file('/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json')
    trader = ExtendedTrader(config)
    await trader.initialize()
    
    # Get position
    positions = await trader.get_positions()
    sol_pos = None
    for p in positions:
        if p.symbol == "SOL-USD":
            sol_pos = p
            break
    
    if not sol_pos:
        print("No SOL position found")
        await trader.cleanup()
        return
    
    print(f"SOL SHORT: {sol_pos.size} @ ${sol_pos.entry_price:.2f}")
    print(f"Mark: ${sol_pos.mark_price:.2f}")
    print(f"PnL: +${sol_pos.unrealized_pnl:.2f} 🎉\n")
    
    # Use LIMIT order slightly above market to ensure fill
    # SOL precision is typically 2 decimals
    close_price = round(sol_pos.mark_price + 0.50, 2)  # Add 50 cents slippage
    
    print(f"Placing LIMIT BUY @ ${close_price} to close...")
    
    close_order = OrderSpec(
        symbol="SOL-USD",
        side="buy",
        order_type="limit",
        size=abs(sol_pos.size),
        price=close_price,
        reduce_only=True,
        post_only=False  # Allow taker
    )
    
    res = await trader.place_order(close_order)
    
    if res.get("status") == "ok":
        print(f"✅ CLOSE ORDER PLACED!")
        print(f"   Order ID: {res['order_id']}")
        print(f"   Should fill immediately and lock in ~+${sol_pos.unrealized_pnl:.2f} profit")
    else:
        print(f"❌ Failed: {res.get('error')}")
    
    await trader.cleanup()

asyncio.run(close_sol_limit())
