import sys
import asyncio
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

        # Only place ETH Short
        print("Executing Trade: ETH-USD Short")
        order = OrderSpec(
            symbol="ETH-USD",
            side="sell",
            order_type="limit",
            size=0.01,
            price=2980.00,
            post_only=True
        )
        res = await trader.place_order(order)
        print(f"Result: {res}")

        await trader.cleanup()
    except Exception as e:
        print(f"Execution failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
