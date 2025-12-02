import sys
import asyncio
sys.path.insert(0, '/home/kt/ZKputer/HyperOPS/📊 Core Trading System')
from trading_module import TradingConfig, ExtendedTrader

async def main():
    config_path = "/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json"
    config = TradingConfig.from_file(config_path)
    trader = ExtendedTrader(config)
    await trader.initialize()
    
    # Get positions
    positions = await trader.get_positions()
    print(f"\n=== POSITIONS ({len(positions)}) ===")
    for pos in positions:
        print(f"{pos.symbol} {pos.side} {pos.size} @ ${pos.entry_price:.2f}")
        print(f"  Mark: ${pos.mark_price:.2f} | PnL: ${pos.unrealized_pnl:.2f}")
    
    # Get open orders - need to fix the enum handling
    print(f"\n=== OPEN ORDERS ===")
    try:
        orders_response = await trader.trading_client.account.get_open_orders()
        print(f"Total open orders: {len(orders_response.data)}")
        for order in orders_response.data:
            print(f"{order.market} {order.side} {order.qty} @ ${order.price}")
            print(f"  ID: {order.id} | Type: {order.type} | Reduce: {order.reduce_only}")
    except Exception as e:
        print(f"Error getting orders: {e}")
    
    await trader.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
