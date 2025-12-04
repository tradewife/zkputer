import asyncio
from extended_executor import ExtendedExecutor
import json

async def main():
    print("Initializing executor...", flush=True)
    executor = ExtendedExecutor()
    await executor.initialize()
    
    print("Fetching markets...", flush=True)
    try:
        markets = await executor.trading_client.markets_info.get_markets()
        print(f"Markets Response Type: {type(markets)}", flush=True)
        print(f"Markets Response Attributes: {[a for a in dir(markets) if not a.startswith('_')]}", flush=True)
        
        if hasattr(markets, 'data'):
            print(f"Data Type: {type(markets.data)}", flush=True)
            if isinstance(markets.data, list):
                print(f"Data Length: {len(markets.data)}", flush=True)
                if len(markets.data) > 0:
                    first_market = markets.data[0]
                    print(f"\nFirst Market Object Type: {type(first_market)}", flush=True)
                    print(f"First Market Attributes: {[a for a in dir(first_market) if not a.startswith('_')]}", flush=True)
                    
                    if hasattr(first_market, 'market_stats'):
                        stats = first_market.market_stats
                        print(f"\nStats Object Type: {type(stats)}", flush=True)
                        print(f"Stats Attributes: {[a for a in dir(stats) if not a.startswith('_')]}", flush=True)
            else:
                print(f"Data Content: {markets.data}", flush=True)
        else:
            print("No 'data' attribute found in response", flush=True)
            
    except Exception as e:
        print(f"Error fetching markets: {e}", flush=True)

asyncio.run(main())
