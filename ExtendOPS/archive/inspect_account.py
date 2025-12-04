#!/usr/bin/env python3
"""
Inspect Account methods to find set_leverage
"""
import asyncio
import sys
sys.path.insert(0, '/home/kt/ZKputer/HyperOPS/📊 Core Trading System')

from trading_module import TradingConfig, ExtendedTrader

async def inspect_account():
    config = TradingConfig.from_file(
        "/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json"
    )
    
    trader = ExtendedTrader(config)
    await trader.initialize()
    
    print("Methods of trader.trading_client.account:")
    print(dir(trader.trading_client.account))
    
    await trader.cleanup()

if __name__ == "__main__":
    asyncio.run(inspect_account())
