#!/usr/bin/env python3
"""
Execute SOL Short and AVAX Long Trades
Based on Daily Trading Brief 2025-11-30 (Revision 2)
"""

import asyncio
import sys
import logging
from decimal import Decimal

# Add current directory to path
sys.path.insert(0, '/home/kt/ZKputer/HyperOPS/📊 Core Trading System')

from trading_module import TradingConfig, ExtendedTrader, OrderSpec

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def execute_trades():
    # Load config
    config = TradingConfig.from_file(
        "/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json"
    )
    
    trader = ExtendedTrader(config)
    if not await trader.initialize():
        print("Failed to initialize trader")
        return

    print("🚀 EXECUTING DAILY TRADES (SOL & AVAX)...")
    print("=" * 80)
    
    # --- TRADE 1: SOL-USD SHORT ---
    # Entry: $138.00 (Limit)
    # Stop: $141.50 (Stop Market)
    # TP1: $132.00
    # TP2: $128.00
    # Size: 1.5 SOL
    
    print("\n1️⃣ Placing SOL-USD Short Orders...")
    
    # Main Entry Order
    sol_entry = OrderSpec(
        symbol="SOL-USD",
        side="sell",
        order_type="limit",
        size=1.5,
        price=138.00,
        post_only=True
    )
    
    res_sol = await trader.place_order(sol_entry)
    if res_sol.get("status") == "ok":
        print(f"✅ SOL Short Entry Placed: 1.5 @ $138.00 | ID: {res_sol['order_id']}")
        
        # Place Stop Loss (Separate Order)
        sol_stop = OrderSpec(
            symbol="SOL-USD",
            side="buy", # Buy to close short
            order_type="stop_loss",
            size=1.5,
            stop_loss_price=141.50, # Trigger Price
            reduce_only=True
        )
        res_sol_stop = await trader.place_order(sol_stop)
        if res_sol_stop.get("status") == "ok":
             print(f"   🛡️ SOL Stop Loss Placed @ $141.50")
        else:
             print(f"   ❌ SOL Stop Loss Failed: {res_sol_stop.get('error')}")

        # Place TP1 (50%)
        sol_tp1 = OrderSpec(
            symbol="SOL-USD",
            side="buy",
            order_type="take_profit",
            size=0.75,
            take_profit_price=132.00,
            reduce_only=True
        )
        res_sol_tp1 = await trader.place_order(sol_tp1)
        if res_sol_tp1.get("status") == "ok":
             print(f"   🎯 SOL TP1 Placed @ $132.00")
        else:
             print(f"   ❌ SOL TP1 Failed: {res_sol_tp1.get('error')}")

        # Place TP2 (50%)
        sol_tp2 = OrderSpec(
            symbol="SOL-USD",
            side="buy",
            order_type="take_profit",
            size=0.75,
            take_profit_price=128.00,
            reduce_only=True
        )
        res_sol_tp2 = await trader.place_order(sol_tp2)
        if res_sol_tp2.get("status") == "ok":
             print(f"   🎯 SOL TP2 Placed @ $128.00")
        else:
             print(f"   ❌ SOL TP2 Failed: {res_sol_tp2.get('error')}")

    else:
        print(f"❌ SOL Short Entry Failed: {res_sol.get('error')}")


    # --- TRADE 2: AVAX-USD LONG ---
    # Entry: $14.05 (Limit)
    # Stop: $13.50 (Stop Market)
    # TP1: $14.80
    # TP2: $15.50
    # Size: 15 AVAX
    
    print("\n2️⃣ Placing AVAX-USD Long Orders...")
    
    # Main Entry Order
    avax_entry = OrderSpec(
        symbol="AVAX-USD",
        side="buy",
        order_type="limit",
        size=15.0,
        price=14.05,
        post_only=True
    )
    
    res_avax = await trader.place_order(avax_entry)
    if res_avax.get("status") == "ok":
        print(f"✅ AVAX Long Entry Placed: 15.0 @ $14.05 | ID: {res_avax['order_id']}")
        
        # Place Stop Loss (Separate Order)
        avax_stop = OrderSpec(
            symbol="AVAX-USD",
            side="sell", # Sell to close long
            order_type="stop_loss",
            size=15.0,
            stop_loss_price=13.50, # Trigger Price
            reduce_only=True
        )
        res_avax_stop = await trader.place_order(avax_stop)
        if res_avax_stop.get("status") == "ok":
             print(f"   🛡️ AVAX Stop Loss Placed @ $13.50")
        else:
             print(f"   ❌ AVAX Stop Loss Failed: {res_avax_stop.get('error')}")

        # Place TP1 (50%)
        avax_tp1 = OrderSpec(
            symbol="AVAX-USD",
            side="sell",
            order_type="take_profit",
            size=7.5,
            take_profit_price=14.80,
            reduce_only=True
        )
        res_avax_tp1 = await trader.place_order(avax_tp1)
        if res_avax_tp1.get("status") == "ok":
             print(f"   🎯 AVAX TP1 Placed @ $14.80")
        else:
             print(f"   ❌ AVAX TP1 Failed: {res_avax_tp1.get('error')}")

        # Place TP2 (50%)
        avax_tp2 = OrderSpec(
            symbol="AVAX-USD",
            side="sell",
            order_type="take_profit",
            size=7.5,
            take_profit_price=15.50,
            reduce_only=True
        )
        res_avax_tp2 = await trader.place_order(avax_tp2)
        if res_avax_tp2.get("status") == "ok":
             print(f"   🎯 AVAX TP2 Placed @ $15.50")
        else:
             print(f"   ❌ AVAX TP2 Failed: {res_avax_tp2.get('error')}")

    else:
        print(f"❌ AVAX Long Entry Failed: {res_avax.get('error')}")

    await trader.cleanup()

if __name__ == "__main__":
    asyncio.run(execute_trades())
