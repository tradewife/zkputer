import sys
import asyncio
sys.path.insert(0, '/home/kt/ZKputer/HyperOPS/📊 Core Trading System')
from trading_module import TradingConfig, ExtendedTrader

async def main():
    config_path = "/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json"
    config = TradingConfig.from_file(config_path)
    trader = ExtendedTrader(config)
    await trader.initialize()
    
    # Get account state
    account = await trader.get_account_state()
    print(f"Account Equity: ${account['equity']:.2f}")
    print(f"Available Balance: ${account['available_balance']:.2f}")
    print(f"Margin Usage: {account['margin_usage']:.2%}")
    
    # Get open orders
    orders = await trader.get_open_orders()
    print(f"\nOpen Orders: {len(orders)}")
    for order in orders:
        print(f"  {order['symbol']} {order['side']} {order['size']} @ {order['price']} ID: {order['id']}")
    
    # Cancel all open orders
    if orders:
        print(f"\nCanceling {len(orders)} open orders...")
        for order in orders:
            result = await trader.cancel_order(order['id'])
            print(f"  Canceled {order['id']}: {result}")
    
    await trader.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
