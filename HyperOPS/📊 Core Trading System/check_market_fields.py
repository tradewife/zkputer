#!/usr/bin/env python3
import asyncio
import json
from x10.perpetual.trading_client import PerpetualTradingClient
from x10.perpetual.configuration import MAINNET_CONFIG  
from x10.perpetual.accounts import StarkPerpetualAccount

async def test():
    config = json.load(open('⚙️ Configuration/config/trading_config.json'))
    account = StarkPerpetualAccount(
        vault=config['vault_number'],
        private_key=config['stark_private_key'],
        public_key=config['stark_public_key'],
        api_key=config['api_key']
    )
    client = PerpetualTradingClient(MAINNET_CONFIG, account)
    markets = await client.markets_info.get_markets()
    
    print('Sample market attributes:')
    for m in markets.data[:2]:
        print(f'\nMarket: {m.name}')
        print(f'Type: {type(m)}')
        print(f'Fields: {m.model_fields.keys() if hasattr(m, "model_fields") else "N/A"}')
        print(f'Dict: {m.model_dump() if hasattr(m, "model_dump") else m}')
    
    await client.close()

asyncio.run(test())
