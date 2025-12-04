import asyncio
import json
import os
from decimal import Decimal
from x10.perpetual.accounts import StarkPerpetualAccount
# Try importing SimpleTradingClient
try:
    from x10.perpetual.simple_client.simple_trading_client import SimpleTradingClient
except ImportError:
    print("❌ SimpleTradingClient not found", flush=True)
    exit(1)

from x10.perpetual.configuration import MAINNET_CONFIG
from x10.perpetual.orders import OrderSide

async def main():
    print("🚀 Starting Simple SDK Execution Test...", flush=True)
    
    config_path = "/home/kt/ZKputer/ExtendOPS/⚙️ Configuration/config/trading_config.json"
    with open(config_path, "r") as f:
        config = json.load(f)

    account = StarkPerpetualAccount(
        vault=config["vault_number"],
        private_key=config["stark_private_key"],
        public_key=config["stark_public_key"],
        api_key=config["api_key"],
    )
    
    # Initialize Simple Client
    # Note: Constructor signature might be different, guessing it's similar
    try:
        client = SimpleTradingClient(MAINNET_CONFIG, account)
        print("✅ Simple Client initialized", flush=True)
    except Exception as e:
        print(f"❌ Failed to init Simple Client: {e}", flush=True)
        return

    # BTC Order
    market = "BTC-USD"
    size = Decimal("0.011")
    price = Decimal("93000")
    side = OrderSide.BUY
    
    print(f"⏳ Placing Order via Simple Client: {market} {side} {size} @ {price}", flush=True)
    
    try:
        order = await client.place_order(
            market_name=market,
            amount_of_synthetic=size,
            price=price,
            side=side,
            reduce_only=False,
            post_only=False
        )
        print(f"✅ Order Placed! ID: {order.data.id}", flush=True)
    except Exception as e:
        print(f"❌ Order Failed: {e}", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
