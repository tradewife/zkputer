import sys
import asyncio
import json
sys.path.insert(0, '/home/kt/ZKputer/HyperOPS/📊 Core Trading System')
from trading_module import TradingConfig, ExtendedTrader, OrderSpec

async def main():
    config_path = "/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json"
    try:
        config = TradingConfig.from_file(config_path)
        trader = ExtendedTrader(config)
        success = await trader.initialize()
        if not success:
            print("Failed to initialize trader")
            return

        print("Fetching market data...")
        markets = await trader.get_market_data(['ZEC-USD', 'ETH-USD'])
        print(json.dumps(markets, indent=2, default=str))

        await trader.cleanup()
    except Exception as e:
        print(f"Execution failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
