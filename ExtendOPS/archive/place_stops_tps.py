#!/usr/bin/env python3
"""
Place Stop Loss and Take Profit Orders
Executes trigger orders for open positions using Extended SDK
"""

import asyncio
import sys
import logging
import json
import time

# Add current directory to path
sys.path.insert(0, '/home/kt/ZKputer/HyperOPS/📊 Core Trading System')

from trading_module import TradingConfig, ExtendedTrader, OrderSpec

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def place_stops_and_tps():
    # Load config
    config = TradingConfig.from_file(
        "/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json"
    )
    
    trader = ExtendedTrader(config)
    if not await trader.initialize():
        print("Failed to initialize trader")
        return

    print("🚀 PLACING STOP LOSS & TAKE PROFIT ORDERS (Extended SDK)")
    print("=" * 80)

    # Order specifications
    orders = [
        # BTC-PERP
        OrderSpec(
            symbol="BTC-USD",
            side="sell", # Closing Long
            order_type="stop_loss",
            size=0.0035,
            price=88071.0, # Trigger Price
            reduce_only=True
        ),
        OrderSpec(
            symbol="BTC-USD",
            side="sell", # Closing Long
            order_type="take_profit",
            size=0.00175, # 50%
            price=90750.0, # Trigger Price
            reduce_only=True
        ),
        OrderSpec(
            symbol="BTC-USD",
            side="sell", # Closing Long
            order_type="take_profit",
            size=0.00175, # 50%
            price=93000.0, # Trigger Price
            reduce_only=True
        ),
        
        # ETH-PERP
        OrderSpec(
            symbol="ETH-USD",
            side="sell", # Closing Long
            order_type="stop_loss",
            size=0.11,
            price=2942.0, # Trigger Price
            reduce_only=True
        ),
        OrderSpec(
            symbol="ETH-USD",
            side="sell", # Closing Long
            order_type="take_profit",
            size=0.055, # 50%
            price=3090.0, # Trigger Price
            reduce_only=True
        ),
        OrderSpec(
            symbol="ETH-USD",
            side="sell", # Closing Long
            order_type="take_profit",
            size=0.055, # 50%
            price=3240.0, # Trigger Price
            reduce_only=True
        ),
        
        # SOL-PERP
        OrderSpec(
            symbol="SOL-USD",
            side="sell", # Closing Long
            order_type="stop_loss",
            size=0.2,
            price=140.0, # Trigger Price
            reduce_only=True
        ),
        OrderSpec(
            symbol="SOL-USD",
            side="sell", # Closing Long
            order_type="take_profit",
            size=0.2,
            price=150.0, # Trigger Price
            reduce_only=True
        ),
        
        # XRP-PERP
        OrderSpec(
            symbol="XRP-USD",
            side="sell", # Closing Long
            order_type="stop_loss",
            size=24.0,
            price=2.15, # Trigger Price
            reduce_only=True
        ),
        OrderSpec(
            symbol="XRP-USD",
            side="sell", # Closing Long
            order_type="take_profit",
            size=24.0,
            price=2.35, # Trigger Price
            reduce_only=True
        ),
    ]

    results = []

    for order in orders:
        try:
            print(f"\n📝 Placing {order.order_type} for {order.symbol} @ {order.price}")
            
            result = await trader.place_order(order)
            
            if result.get("status") == "ok":
                print(f"✅ Order placed successfully: ID {result.get('order_id')}")
                results.append({
                    "symbol": order.symbol,
                    "type": order.order_type,
                    "status": "success",
                    "result": result
                })
            else:
                print(f"❌ Failed: {result.get('error')}")
                results.append({
                    "symbol": order.symbol,
                    "type": order.order_type,
                    "status": "error",
                    "error": result.get("error")
                })
            
            # Wait between orders to avoid rate limiting
            await asyncio.sleep(1)
            
        except Exception as e:
            print(f"❌ Error placing order: {e}")
            results.append({
                "symbol": order.symbol,
                "type": order.order_type,
                "status": "error",
                "error": str(e)
            })

    await trader.cleanup()

    print("\n" + "=" * 80)
    print("📊 EXECUTION SUMMARY:")
    print(f"   Total Orders: {len(orders)}")
    print(f"   Successful: {sum(1 for r in results if r['status'] == 'success')}")
    print(f"   Failed: {sum(1 for r in results if r['status'] == 'error')}")

    # Save results
    with open('/home/kt/ZKputer/HyperOPS/research_logs/2025-11-30/stop_tp_execution.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("\n✅ Results saved to: stop_tp_execution.json")

if __name__ == "__main__":
    asyncio.run(place_stops_and_tps())
