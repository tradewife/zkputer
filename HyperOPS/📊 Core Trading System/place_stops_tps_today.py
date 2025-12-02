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

        # ZEC-USD Stop Loss
        print("Placing ZEC-USD Stop Loss @ $440")
        zec_sl = OrderSpec(
            symbol="ZEC-USD",
            side="sell",
            order_type="limit",
            size=1.0,
            price=440.00,
            reduce_only=True
        )
        res1 = await trader.place_order(zec_sl)
        print(f"ZEC SL Result: {res1}")

        # ZEC-USD TP1
        print("Placing ZEC-USD TP1 @ $475")
        zec_tp1 = OrderSpec(
            symbol="ZEC-USD",
            side="sell",
            order_type="limit",
            size=0.5,
            price=475.00,
            reduce_only=True
        )
        res2 = await trader.place_order(zec_tp1)
        print(f"ZEC TP1 Result: {res2}")

        # ZEC-USD TP2
        print("Placing ZEC-USD TP2 @ $500")
        zec_tp2 = OrderSpec(
            symbol="ZEC-USD",
            side="sell",
            order_type="limit",
            size=0.5,
            price=500.00,
            reduce_only=True
        )
        res3 = await trader.place_order(zec_tp2)
        print(f"ZEC TP2 Result: {res3}")

        # ETH-USD Stop Loss
        print("Placing ETH-USD Stop Loss @ $3050")
        eth_sl = OrderSpec(
            symbol="ETH-USD",
            side="buy",
            order_type="limit",
            size=0.01,
            price=3050.00,
            reduce_only=True
        )
        res4 = await trader.place_order(eth_sl)
        print(f"ETH SL Result: {res4}")

        # ETH-USD TP1
        print("Placing ETH-USD TP1 @ $2900")
        eth_tp1 = OrderSpec(
            symbol="ETH-USD",
            side="buy",
            order_type="limit",
            size=0.005,
            price=2900.00,
            reduce_only=True
        )
        res5 = await trader.place_order(eth_tp1)
        print(f"ETH TP1 Result: {res5}")

        # ETH-USD TP2
        print("Placing ETH-USD TP2 @ $2800")
        eth_tp2 = OrderSpec(
            symbol="ETH-USD",
            side="buy",
            order_type="limit",
            size=0.005,
            price=2800.00,
            reduce_only=True
        )
        res6 = await trader.place_order(eth_tp2)
        print(f"ETH TP2 Result: {res6}")

        await trader.cleanup()
    except Exception as e:
        print(f"Execution failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
