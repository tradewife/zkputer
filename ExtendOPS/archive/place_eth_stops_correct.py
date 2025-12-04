import sys
import asyncio
sys.path.insert(0, '/home/kt/ZKputer/HyperOPS/📊 Core Trading System')
from trading_module import TradingConfig, ExtendedTrader, OrderSpec

async def main():
    config_path = "/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json"
    config = TradingConfig.from_file(config_path)
    trader = ExtendedTrader(config)
    await trader.initialize()
    
    # Get current position to confirm size
    positions = await trader.get_positions()
    print(f"Current positions: {len(positions)}")
    for pos in positions:
        print(f"  {pos.symbol} {pos.side} {pos.size}")
    
    # ETH-USD Stop Loss @ $3050 (for 0.02 ETH short position)
    print("\nPlacing ETH-USD Stop Loss @ $3050")
    eth_sl = OrderSpec(
        symbol="ETH-USD",
        side="buy",  # Buy to close short
        order_type="limit",
        size=0.02,  # Match actual position size
        price=3050.00,
        reduce_only=True
    )
    res1 = await trader.place_order(eth_sl)
    print(f"ETH SL Result: {res1}")
    
    # ETH-USD Take Profit @ $2900 (full position)
    print("\nPlacing ETH-USD Take Profit @ $2900")
    eth_tp = OrderSpec(
        symbol="ETH-USD",
        side="buy",  # Buy to close short
        order_type="limit",
        size=0.02,  # Full position
        price=2900.00,
        reduce_only=True
    )
    res2 = await trader.place_order(eth_tp)
    print(f"ETH TP Result: {res2}")
    
    await trader.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
