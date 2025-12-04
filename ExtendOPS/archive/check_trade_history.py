#!/usr/bin/env python3
"""
Check recent trade history and position changes
"""

import asyncio
import sys
import os

sys.path.append(os.path.dirname(__file__))
from extended_executor import ExtendedExecutor

async def main():
    executor = ExtendedExecutor()
    if not await executor.initialize():
        return

    # Get positions history
    print("\n📊 RECENT POSITION HISTORY")
    try:
        positions_history = await executor.trading_client.account.get_positions_history()
        
        # Show last 5 closed positions
        for pos in positions_history.data[:5]:
            pnl = float(pos.realised_pnl) if hasattr(pos, 'realised_pnl') else 0
            pnl_emoji = "🟢" if pnl >= 0 else "🔴"
            print(f"{pos.market}: {pos.side} | Size: {pos.size}")
            print(f"  Entry: ${pos.open_price} | Exit: ${getattr(pos, 'close_price', 'N/A')}")
            print(f"  PnL: {pnl_emoji} ${pnl:.2f}")
            print()
    except Exception as e:
        print(f"❌ Failed to get position history: {e}")

    # Get order history
    print("\n📝 RECENT ORDER HISTORY")
    try:
        orders_history = await executor.trading_client.account.get_orders_history(limit=10)
        
        for order in orders_history.data:
            print(f"{order.market}: {order.side} {order.qty} @ ${order.price}")
            print(f"  Status: {order.status} | Type: {order.type}")
            if hasattr(order, 'filled_qty') and order.filled_qty:
                print(f"  Filled: {order.filled_qty}")
            print()
    except Exception as e:
        print(f"❌ Failed to get order history: {e}")

if __name__ == "__main__":
    asyncio.run(main())
