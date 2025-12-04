#!/usr/bin/env python3
"""
Execute Daily Trades
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

    print("🚀 EXECUTING DAILY TRADES...")
    
    # --- TRADE 1: ETH-USD SHORT ---
    # ALREADY PLACED 0.20 ETH (Order 1A)
    # Skipping Order 1B to save margin for ZEC trade.
    
    # print("\n1️⃣ Placing ETH-USD Short Orders...")
    
    # # Order 1A (TP1) - ALREADY FILLED
    # # ...
    
    # # Order 1B (TP2) - SKIPPING due to margin limits
    # # ...


    # --- TRADE 2: ZEC-USD LONG ---
    # Entry: $452, Stop: $438
    # TP1: $465 (50%), TP2: $480 (50%)
    # Original Size: 1.4 ZEC -> Reduced to 1.0 ZEC (0.5 + 0.5) to fit 12x leverage cap.
    
    print("\n2️⃣ Placing ZEC-USD Long Orders (Reduced Size)...")
    
    # Order 2A (TP1)
    order_2a = OrderSpec(
        symbol="ZEC-USD",
        side="buy",
        order_type="limit",
        size=0.5,
        price=452.0,
        stop_loss_price=438.0,
        take_profit_price=465.0,
        post_only=True
    )
    
    res_2a = await trader.place_order(order_2a)
    if res_2a.get("status") == "ok":
        print(f"✅ ZEC Long 2A Placed: 0.5 @ $452 | Stop: $438 | TP: $465 | ID: {res_2a['order_id']}")
    else:
        print(f"❌ ZEC Long 2A Failed: {res_2a.get('error')}")

    # Order 2B (TP2)
    order_2b = OrderSpec(
        symbol="ZEC-USD",
        side="buy",
        order_type="limit",
        size=0.5,
        price=452.0,
        stop_loss_price=438.0,
        take_profit_price=480.0,
        post_only=True
    )
    
    res_2b = await trader.place_order(order_2b)
    if res_2b.get("status") == "ok":
        print(f"✅ ZEC Long 2B Placed: 0.5 @ $452 | Stop: $438 | TP: $480 | ID: {res_2b['order_id']}")
    else:
        print(f"❌ ZEC Long 2B Failed: {res_2b.get('error')}")

    await trader.cleanup()

if __name__ == "__main__":
    asyncio.run(execute_trades())
