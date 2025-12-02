#!/usr/bin/env python3
"""
Check Extended balance response structure
"""

import asyncio
from x10.perpetual.accounts import StarkPerpetualAccount
from x10.perpetual.trading_client import PerpetualTradingClient
from x10.perpetual.configuration import MAINNET_CONFIG
import json

async def check_structure():
    with open("/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json") as f:
        config = json.load(f)
    
    account = StarkPerpetualAccount(
        vault=config["vault_number"],
        private_key=config["stark_private_key"],
        public_key=config["stark_public_key"],
        api_key=config["api_key"],
    )
    
    client = PerpetualTradingClient(MAINNET_CONFIG, account)
    
    try:
        balance = await client.account.get_balance()
        print("Balance object type:", type(balance))
        print("Balance attributes:", dir(balance))
        print("\nBalance object:", balance)
        
        # Try different access methods
        if hasattr(balance, 'data'):
            print("\nbalance.data:", balance.data)
            print("balance.data type:", type(balance.data))
            if hasattr(balance.data, 'equity'):
                print("✅ balance.data.equity:", balance.data.equity)
        
        if hasattr(balance, 'equity'):
            print("✅ balance.equity:", balance.equity)
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    await client.close()

if __name__ == "__main__":
    asyncio.run(check_structure())
