#!/usr/bin/env python3
"""
Extended Account Manager
Get positions, orders, balance, and manage risk
"""

import asyncio
import sys
import os
from typing import List, Dict

sys.path.append(os.path.dirname(__file__))
from extended_executor import ExtendedExecutor


async def get_account_status() -> Dict:
    """
    Get complete account status
    
    Returns:
        Dict with balance, positions, orders
    """
    executor = ExtendedExecutor()
    if not await executor.initialize():
        return {}
    
    try:
        # Get balance
        balance = await executor.trading_client.account.get_balance()
        
        # Get positions
        positions = await executor.trading_client.account.get_positions()
        
        # Get orders
        orders = await executor.trading_client.account.get_open_orders()
        
        return {
            "equity": float(balance.data.equity),
            "available": float(balance.data.available_for_trade),
            "positions": [
                {
                    "market": pos.market,
                    "side": str(pos.side),
                    "size": float(pos.size),
                    "entry_price": float(pos.open_price),
                    "mark_price": float(pos.mark_price),
                    "pnl": float(pos.unrealised_pnl),
                    "leverage": float(pos.leverage)
                }
                for pos in positions.data
            ],
            "orders": [
                {
                    "market": order.market,
                    "side": str(order.side),
                    "type": str(order.type),
                    "size": float(order.qty),
                    "price": float(order.price),
                    "order_id": order.id
                }
                for order in orders.data
            ]
        }
    
    except Exception as e:
        print(f"❌ Failed to get account status: {e}")
        return {}


async def print_account_status():
    """Print formatted account status"""
    status = await get_account_status()
    
    if not status:
        return
    
    print("\n💰 ACCOUNT STATUS")
    print(f"Equity: ${status['equity']:.2f}")
    print(f"Available: ${status['available']:.2f}")
    print(f"Margin Used: ${status['equity'] - status['available']:.2f}")
    
    print(f"\n📊 OPEN POSITIONS ({len(status['positions'])})")
    for pos in status['positions']:
        pnl_emoji = "🟢" if pos['pnl'] >= 0 else "🔴"
        print(f"{pos['market']}: {pos['side']} {pos['size']} @ ${pos['entry_price']:.2f}")
        print(f"  PnL: {pnl_emoji} ${pos['pnl']:.2f} | Lev: {pos['leverage']:.0f}x | Mark: ${pos['mark_price']:.2f}")
    
    print(f"\n📝 OPEN ORDERS ({len(status['orders'])})")
    for order in status['orders']:
        print(f"{order['market']}: {order['side']} {order['size']} @ ${order['price']:.2f} ({order['type']})")


if __name__ == "__main__":
    asyncio.run(print_account_status())
