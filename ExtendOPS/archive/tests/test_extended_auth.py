#!/usr/bin/env python3
"""
Simple diagnostic to check Extended API authentication
"""

import asyncio
from x10.perpetual.accounts import StarkPerpetualAccount
from x10.perpetual.trading_client import PerpetualTradingClient
from x10.perpetual.configuration import MAINNET_CONFIG
import json

async def test_auth():
    # Load config
    with open("/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json") as f:
        config = json.load(f)
    
    print("Testing Extended API Authentication...")
    print(f"Vault: {config['vault_number']}")
    print(f"API Key (first 10 chars): {config['api_key'][:10]}...")
    print(f"Public Key (first 20 chars): {config['stark_public_key'][:20]}...")
    
    try:
        # Create account
        account = StarkPerpetualAccount(
            vault=config["vault_number"],
            private_key=config["stark_private_key"],
            public_key=config["stark_public_key"],
            api_key=config["api_key"],
        )
        print("✅ Stark account created")
        
        # Create client
        client = PerpetualTradingClient(MAINNET_CONFIG, account)
        print("✅ Trading client created")
        
        # Try to get markets (public endpoint, no auth needed)
        print("\nTesting public endpoint (markets)...")
        markets = await client.markets_info.get_markets()
        print(f"✅ Got {len(markets.data)} markets")
        for i, market in enumerate(markets.data[:3]):
            print(f"   {i+1}. {getattr(market, 'name', 'N/A')}")
        
        # Try authenticated endpoint
        print("\nTesting authenticated endpoint (balance)...")
        try:
            balance = await client.account.get_balance()
            print(f"✅ Balance retrieved: ${float(balance.equity):.2f}")
        except Exception as e:
            print(f"❌ Balance failed: {e}")
            print("\n🔍 This suggests API key issue. Please regenerate at:")
            print("   https://app.extended.exchange/api-management")
        
        await client.close()
        print("\n✅ Client closed")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_auth())
