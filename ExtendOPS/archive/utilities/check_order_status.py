#!/usr/bin/env python3
"""
Check Open Orders and Positions
"""

import asyncio
import sys
sys.path.insert(0, '/home/kt/ZKputer/HyperOPS/📊 Core Trading System')

from trading_module import TradingConfig, ExtendedTrader

async def check_status():
    config = TradingConfig.from_file(
        "/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json"
    )
    
    trader = ExtendedTrader(config)
    if not await trader.initialize():
        print("Failed to initialize")
        return

    print("=" * 80)
    print("📋 OPEN ORDERS:")
    print("=" * 80)
    orders = await trader.get_open_orders()
    if orders:
        for o in orders:
            print(f"  Order ID: {o['id']}")
            print(f"  {o['symbol']} {o['side'].upper()} {o['size']} @ ${o['price']}")
            print(f"  Type: {o['type']} | Filled: {o['filled']}")
            print("-" * 80)
    else:
        print("  No open orders found.")
    
    print("\n" + "=" * 80)
    print("💼 OPEN POSITIONS:")
    print("=" * 80)
    positions = await trader.get_positions()
    if positions:
        for p in positions:
            print(f"  {p.symbol} {p.side.upper()} {p.size}")
            print(f"  Entry: ${p.entry_price:.2f} | Mark: ${p.mark_price:.2f}")
            print(f"  PnL: ${p.unrealized_pnl:.2f} | Leverage: {p.leverage}x")
            print("-" * 80)
    else:
        print("  No open positions.")
    
    print("\n" + "=" * 80)
    print("💰 ACCOUNT:")
    print("=" * 80)
    account = await trader.get_account_state()
    print(f"  Equity: ${account['equity']:.2f}")
    print(f"  Available: ${account['available_balance']:.2f}")
    print(f"  Margin Usage: {account['margin_usage']:.2%}")

    await trader.cleanup()

if __name__ == "__main__":
    asyncio.run(check_status())
