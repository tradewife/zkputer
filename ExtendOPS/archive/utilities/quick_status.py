#!/usr/bin/env python3
import asyncio
import sys
sys.path.insert(0, '/home/kt/ZKputer/HyperOPS/📊 Core Trading System')
from trading_module import TradingConfig, ExtendedTrader

async def check():
    try:
        config = TradingConfig.from_file('/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json')
        trader = ExtendedTrader(config)
        success = await trader.initialize()
        
        if not success:
            print("ERROR: Failed to initialize trader")
            return
        
        print("=" * 60)
        print("CURRENT STATUS:")
        print("=" * 60)
        
        orders = await trader.get_open_orders()
        print(f"\nOpen Orders: {len(orders)}")
        for o in orders:
            print(f"  • {o['symbol']} {o['side'].upper()} {o['size']} @ ${o['price']}")
        
        positions = await trader.get_positions()
        print(f"\nOpen Positions: {len(positions)}")
        for p in positions:
            print(f"  • {p.symbol} {p.side.upper()} {p.size} @ ${p.entry_price:.2f}")
            print(f"    PnL: ${p.unrealized_pnl:.2f}")
        
        account = await trader.get_account_state()
        print(f"\nAccount:")
        print(f"  Equity: ${account['equity']:.2f}")
        print(f"  Available: ${account['available_balance']:.2f}")
        
        await trader.cleanup()
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(check())
