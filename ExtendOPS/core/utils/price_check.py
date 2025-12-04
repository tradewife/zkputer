#!/usr/bin/env python3
"""
Get Real-Time Extended Exchange Prices
Direct API implementation to bypass SDK issues
"""
import asyncio
import aiohttp
import json
from datetime import datetime

async def main():
    print("\n🔌 Connecting to Extended Exchange (Direct API)...", flush=True)
    
    url = "https://api.starknet.extended.exchange/api/v1/info/markets"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    print(f"❌ API Error: {response.status}", flush=True)
                    return
                
                data = await response.json()
                
                if data.get("status") != "OK":
                    print(f"❌ API returned error status: {data}", flush=True)
                    return
                
                markets = data.get("data", [])
                
                print(f'\n📊 REAL-TIME EXTENDED EXCHANGE PRICES', flush=True)
                print(f'Timestamp: {datetime.now().strftime("%H:%M:%S AEST")} (Dec 4, 2025)', flush=True)
                print('=' * 95, flush=True)
                print(f'{"SYMBOL":<10} | {"PRICE":>12} | {"24H VOL":>12} | {"OPEN INT":>12} | {"FUNDING":>10}', flush=True)
                print('=' * 95, flush=True)
                
                target_symbols = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'HYPE-USD', 'ADA-USD']
                
                for symbol in target_symbols:
                    market_data = next((m for m in markets if m["name"] == symbol), None)
                    
                    if market_data:
                        stats = market_data["marketStats"]
                        price = float(stats["lastPrice"])
                        volume = float(stats["dailyVolume"])
                        oi = float(stats["openInterest"])
                        funding = float(stats["fundingRate"]) * 100
                        
                        print(f'{symbol:<10} | ${price:>11,.2f} | ${volume/1e6:>10,.1f}M | ${oi/1e6:>10,.1f}M | {funding:>+9.4f}%', flush=True)
                    else:
                        print(f'{symbol:<10} | NOT FOUND', flush=True)

    except Exception as e:
        print(f"❌ Connection failed: {e}", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
