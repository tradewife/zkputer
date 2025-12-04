import asyncio
import json
import os
from x10.perpetual.accounts import StarkPerpetualAccount
from x10.perpetual.trading_client import PerpetualTradingClient
from x10.perpetual.configuration import MAINNET_CONFIG

async def main():
    print("Starting direct SDK test...", flush=True)
    
    config_path = "/home/kt/ZKputer/ExtendOPS/⚙️ Configuration/config/trading_config.json"
    if not os.path.exists(config_path):
        print(f"Config not found at {config_path}", flush=True)
        return

    with open(config_path, "r") as f:
        config = json.load(f)
    
    print("Config loaded.", flush=True)

    account = StarkPerpetualAccount(
        vault=config["vault_number"],
        private_key=config["stark_private_key"],
        public_key=config["stark_public_key"],
        api_key=config["api_key"],
    )
    
    print("Account created.", flush=True)
    
    client = PerpetualTradingClient(MAINNET_CONFIG, account)
    print("Client created.", flush=True)
    
    print("Fetching markets directly...", flush=True)
    try:
        markets = await client.markets_info.get_markets()
        print("Markets fetched!", flush=True)
        print(f"Markets type: {type(markets)}", flush=True)
        if hasattr(markets, 'data') and len(markets.data) > 0:
            print(f"First market: {markets.data[0]}", flush=True)
            print(f"First market dir: {dir(markets.data[0])}", flush=True)
    except Exception as e:
        print(f"Error fetching markets: {e}", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
