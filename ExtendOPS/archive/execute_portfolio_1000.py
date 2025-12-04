#!/usr/bin/env python3
"""
Execute $1000 Portfolio: BTC Long + ADA Short + HYPE Long
"""

import asyncio
import sys
import os
from decimal import Decimal

sys.path.append(os.path.dirname(__file__))
from extended_executor import ExtendedExecutor
from x10.perpetual.orders import OrderSide

async def main():
    print("🚀 Executing $1,000 Portfolio (3 Trades)")
    print("=" * 60)
    
    executor = ExtendedExecutor()
    if not await executor.initialize():
        return

    # Portfolio allocation
    trades = [
        {
            "name": "BTC Long",
            "market": "BTC-USD",
            "side": "buy",
            "notional": 400,
            "price": 92700,
            "size": 0.0043,  # $400 / $92,700
            "leverage": 10,
            "stop": 90500,
            "tp1": 94500,
            "tp2": 96000
        },
        {
            "name": "ADA Short",
            "market": "ADA-USD",
            "side": "sell",
            "notional": 400,
            "price": 0.4375,
            "size": 912,  # $400 / $0.4375, rounded to multiple of 24
            "leverage": 10,
            "stop": 0.4550,
            "tp1": 0.4250,
            "tp2": 0.4150
        },
        {
            "name": "HYPE Long",
            "market": "HYPE-USD",
            "side": "buy",
            "notional": 200,
            "price": 34.00,
            "size": 6,  # $200 / $34, rounded
            "leverage": 10,
            "stop": 32.50,
            "tp1": 36.00,
            "tp2": 38.00
        }
    ]
    
    print("\n📊 PORTFOLIO BREAKDOWN:")
    for t in trades:
        print(f"{t['name']}: ${t['notional']} @ {t['leverage']}x")
        print(f"  → {t['size']} {t['market']} {t['side'].upper()}")
    
    print("\n" + "=" * 60)
    print("⚙️ SETTING LEVERAGE...\n")
    
    # Set leverage for all markets
    for trade in trades:
        await executor.set_leverage(trade["market"], trade["leverage"])
        await asyncio.sleep(0.2)
    
    print("\n" + "=" * 60)
    print("📝 PLACING ENTRY ORDERS...\n")
    
    # Place entry orders
    results = []
    for trade in trades:
        result = await executor.place_order(
            market=trade["market"],
            side=trade["side"],
            size=trade["size"],
            price=trade["price"],
            leverage=None  # Already set
        )
        results.append({"trade": trade["name"], "result": result})
        await asyncio.sleep(0.5)
    
    print("\n" + "=" * 60)
    print("✅ ENTRY ORDERS COMPLETE\n")
    
    for r in results:
        if r["result"]:
            print(f"✅ {r['trade']}: Order ID {r['result']['order_id']}")
        else:
            print(f"❌ {r['trade']}: FAILED")
    
    print("\n" + "=" * 60)
    print("⚠️  STOP LOSS NOTE:")
    print("Manual stop management required to avoid limit order issue.")
    print("Monitor positions and close manually if:")
    print("  - BTC drops below $90,500")
    print("  - ADA rises above $0.4550")
    print("  - HYPE drops below $32.50")
    
    print("\n💡 Take Profit orders can be placed as limit orders (safe)")

if __name__ == "__main__":
    asyncio.run(main())
