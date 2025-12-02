#!/usr/bin/env python3
"""
Cancel All Open Orders
Checks for open limit orders and cancels them.
"""

import asyncio
import sys
import logging

# Add current directory to path
sys.path.insert(0, '/home/kt/ZKputer/HyperOPS/📊 Core Trading System')

from trading_module import TradingConfig, ExtendedTrader

# Configure logging
logging.basicConfig(level=logging.INFO)

async def cancel_all():
    # Load config
    config = TradingConfig.from_file(
        "/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json"
    )
    
    trader = ExtendedTrader(config)
    if not await trader.initialize():
        print("Failed to initialize trader")
        return

    print("🛑 CHECKING FOR OPEN ORDERS...")
    
    # Get all open orders
    open_orders = await trader.get_open_orders()
    
    if not open_orders:
        print("✅ No open orders found.")
    else:
        print(f"⚠️ Found {len(open_orders)} open orders:")
        for order in open_orders:
            print(f"   - ID: {order['id']} | {order['symbol']} {order['side'].upper()} {order['size']} @ ${order['price']}")
            
        print("\n🗑️ Cancelling all orders...")
        for order in open_orders:
            result = await trader.cancel_order(order['id'])
            if result.get('status') == 'ok':
                print(f"   ✅ Cancelled Order ID: {order['id']}")
            else:
                print(f"   ❌ Failed to cancel Order ID: {order['id']} - {result.get('error')}")

    await trader.cleanup()

if __name__ == "__main__":
    asyncio.run(cancel_all())
