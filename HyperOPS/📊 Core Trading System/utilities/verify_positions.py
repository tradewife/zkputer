#!/usr/bin/env python3
"""
Verify Positions and Orders
"""

import asyncio
import sys
import logging
import json

# Add current directory to path
sys.path.insert(0, '/home/kt/ZKputer/HyperOPS/📊 Core Trading System')

from trading_module import TradingConfig, ExtendedTrader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def verify():
    # Load config
    config = TradingConfig.from_file(
        "/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json"
    )
    
    trader = ExtendedTrader(config)
    if not await trader.initialize():
        print("Failed to initialize trader")
        return

    print("\n🔍 VERIFYING ACCOUNT STATE...")
    
    # Account
    account = await trader.get_account_state()
    print(f"💰 Equity: ${account['equity']:.2f}")
    print(f"   Available: ${account['available_balance']:.2f}")
    print(f"   Margin Usage: {account['margin_usage']:.2%}")

    # Positions
    print("\n📊 OPEN POSITIONS:")
    positions = await trader.get_positions()
    if positions:
        for p in positions:
            print(f"   • {p.symbol} {p.side.upper()} {p.size} @ ${p.entry_price:.2f} (PnL: ${p.unrealized_pnl:.2f})")
    else:
        print("   No open positions.")

    # Open Orders
    print("\n📝 OPEN ORDERS:")
    orders = await trader.get_open_orders()
    if orders:
        for o in orders:
            print(f"   • {o['symbol']} {o['side'].upper()} {o['size']} @ ${o['price']:.2f} [{o['type']}]")
    else:
        print("   No open orders.")

    await trader.cleanup()

if __name__ == "__main__":
    asyncio.run(verify())
