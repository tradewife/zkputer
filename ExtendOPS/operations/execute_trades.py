#!/usr/bin/env python3
"""
Execute Daily Trades - Dec 4, 2025
Executes BTC and HYPE setups with attached stops and TPs
"""
import asyncio
import sys
from decimal import Decimal

# Ensure we can import the executor
sys.path.insert(0, "/home/kt/ZKputer/ExtendOPS/core")
from executor import ExtendedExecutor

async def main():
    print("\n🚀 INITIALIZING TRADE EXECUTION...", flush=True)
    
    executor = ExtendedExecutor()
    if not await executor.initialize():
        print("❌ Failed to initialize executor", flush=True)
        return

    # --- TRADE 1: BTC-USD ---
    print("\n--------------------------------------------------", flush=True)
    print("1️⃣  EXECUTING BTC-USD SETUP (Liquidity Breakout)", flush=True)
    print("--------------------------------------------------", flush=True)
    
    btc_market = "BTC-USD"
    btc_size = 0.011
    btc_entry = 93000.0
    btc_stop = 91200.0
    btc_tp1 = 95500.0
    btc_tp2 = 98000.0
    
    # 1. Set Leverage
    print(f"⏳ Setting BTC Leverage to 10x...", flush=True)
    await executor.set_leverage(btc_market, 10)

    # 2. Place Entry Order (Limit)
    print(f"⏳ Placing BTC Entry: Buy {btc_size} @ ${btc_entry}", flush=True)
    btc_order = await executor.place_order(
        symbol=btc_market,
        side="buy",
        size=btc_size,
        price=btc_entry
    )
    
    if btc_order and btc_order["status"] == "success":
        print("✅ BTC Entry Placed!", flush=True)
        
        # 2. Place Stops & TPs
        print("⏳ Placing BTC Risk Orders...", flush=True)
        await executor.place_stop_tp_orders(
            market=btc_market,
            position_side="long",
            size=btc_size,
            stop_price=btc_stop,
            tp1_price=btc_tp1,
            tp2_price=btc_tp2
        )
    else:
        print("❌ BTC Entry Failed - Skipping Risk Orders", flush=True)

    # --- TRADE 2: HYPE-USD ---
    print("\n--------------------------------------------------", flush=True)
    print("2️⃣  EXECUTING HYPE-USD SETUP (Institutional Catalyst)", flush=True)
    print("--------------------------------------------------", flush=True)
    
    hype_market = "HYPE-USD"
    hype_size = 11.5
    hype_entry = 34.65 # Slightly above market for fill
    hype_stop = 32.80
    hype_tp1 = 37.35
    hype_tp2 = 40.50
    
    # 1. Set Leverage
    print(f"⏳ Setting HYPE Leverage to 4x...", flush=True)
    await executor.set_leverage(hype_market, 4)

    # 2. Place Entry Order (Marketable Limit)
    print(f"⏳ Placing HYPE Entry: Buy {hype_size} @ ${hype_entry}", flush=True)
    hype_order = await executor.place_order(
        symbol=hype_market,
        side="buy",
        size=hype_size,
        price=hype_entry
    )
    
    if hype_order and hype_order["status"] == "success":
        print("✅ HYPE Entry Placed!", flush=True)
        
        # 2. Place Stops & TPs
        print("⏳ Placing HYPE Risk Orders...", flush=True)
        await executor.place_stop_tp_orders(
            market=hype_market,
            position_side="long",
            size=hype_size,
            stop_price=hype_stop,
            tp1_price=hype_tp1,
            tp2_price=hype_tp2
        )
    else:
        print("❌ HYPE Entry Failed - Skipping Risk Orders", flush=True)

    print("\n✨ EXECUTION COMPLETE", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
