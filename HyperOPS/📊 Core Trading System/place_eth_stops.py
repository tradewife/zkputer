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

        # ETH-USD Stop Loss only (TP sizes too small for min trade size)
        print("Placing ETH-USD Stop Loss @ $3050")
        eth_sl = OrderSpec(
            symbol="ETH-USD",
            side="buy",
            order_type="limit",
            size=0.01,
            price=3050.00,
            reduce_only=True
        )
        res = await trader.place_order(eth_sl)
        print(f"ETH SL Result: {res}")

        # ETH-USD TP - using full size since partials don't meet min size
        print("Placing ETH-USD TP @ $2900 (full size)")
        eth_tp = OrderSpec(
            symbol="ETH-USD",
            side="buy",
            order_type="limit",
            size=0.01,
            price=2900.00,
            reduce_only=True
        )
        res2 = await trader.place_order(eth_tp)
        print(f"ETH TP Result: {res2}")

        await trader.cleanup()
    except Exception as e:
        print(f"Execution failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
