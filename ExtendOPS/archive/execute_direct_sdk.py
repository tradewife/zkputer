import asyncio
import json
import os
from decimal import Decimal
from x10.perpetual.accounts import StarkPerpetualAccount
from x10.perpetual.trading_client import PerpetualTradingClient
from x10.perpetual.configuration import MAINNET_CONFIG
from x10.perpetual.orders import OrderSide

async def main():
    print("🚀 Starting Direct SDK Execution Test...", flush=True)
    
    config_path = "/home/kt/ZKputer/ExtendOPS/⚙️ Configuration/config/trading_config.json"
    with open(config_path, "r") as f:
        config = json.load(f)

    account = StarkPerpetualAccount(
        vault=config["vault_number"],
        private_key=config["stark_private_key"],
        public_key=config["stark_public_key"],
        api_key=config["api_key"],
    )
    
    client = PerpetualTradingClient(MAINNET_CONFIG, account)
    print("✅ Client initialized", flush=True)
    
    # BTC Order
    market = "BTC-USD"
    size = Decimal("0.011")
    price = Decimal("93000")
    side = OrderSide.BUY
    
    print(f"⏳ Placing Order: {market} {side} {size} @ {price}", flush=True)
    
    try:
        # Set leverage first (optional, might hang)
        # print("Setting leverage...", flush=True)
        # await client.account.update_leverage(market_name=market, leverage=Decimal("10"))
        
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
