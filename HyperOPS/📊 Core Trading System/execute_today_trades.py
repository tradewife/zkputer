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

        # Trade 1: ZEC-USD Long
        print("Executing Trade 1: ZEC-USD Long")
        order1 = OrderSpec(
            symbol="ZEC-USD",
            side="buy",
            order_type="limit",
            size=0.1,
            price=452.50,
            post_only=True
        )
        res1 = await trader.place_order(order1)
        print(f"Result 1: {res1}")

        # Trade 2: ETH-USD Short
        print("Executing Trade 2: ETH-USD Short")
        order2 = OrderSpec(
            symbol="ETH-USD",
            side="sell",
            order_type="limit",
            size=0.01,
            price=2980.00,
            post_only=True
        )
        res2 = await trader.place_order(order2)
        print(f"Result 2: {res2}")

        await trader.cleanup()
    except Exception as e:
        print(f"Execution failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
