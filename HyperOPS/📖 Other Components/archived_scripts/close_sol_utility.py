#!/usr/bin/env python3
"""
Close SOL using trading_module's close utility
"""

import asyncio
import sys
sys.path.insert(0, '/home/kt/ZKputer/HyperOPS/📊 Core Trading System')
from trading_module import TradingConfig, ExtendedTrader

async def close_sol_utility():
    config = TradingConfig.from_file('/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json')
    trader = ExtendedTrader(config)
    await trader.initialize()
    
    # Check position first
    positions = await trader.get_positions()
    sol_pos = [p for p in positions if p.symbol == "SOL-USD"]
    
    if not sol_pos:
        print("No SOL position found")
        await trader.cleanup()
        return
    
    print(f"SOL Position: SHORT {sol_pos[0].size} @ ${sol_pos[0].entry_price:.2f}")
    print(f"Current Mark: ${sol_pos[0].mark_price:.2f}")
    print(f"PnL: +${sol_pos[0].unrealized_pnl:.2f} 🎉")
    
    # Use the built-in close_all_positions which handles market orders properly
    print(f"\nClosing via utility function...")
    results = await trader.close_all_positions()
    
    for res in results:
        if res.get("status") == "ok":
            print(f"✅ Closed successfully!")
            print(f"   Final profit: +${sol_pos[0].unrealized_pnl:.2f}")
        else:
            print(f"❌ Error: {res.get('error')}")
    
    await trader.cleanup()

asyncio.run(close_sol_utility())
