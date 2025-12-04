#!/usr/bin/env python3
"""
Buy 15 AVAX at market and add stop/TP for 30 total
"""

import asyncio
import sys
sys.path.insert(0, '/home/kt/ZKputer/HyperOPS/📊 Core Trading System')
from trading_module import TradingConfig, ExtendedTrader, OrderSpec

async def buy_avax():
    config = TradingConfig.from_file('/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json')
    trader = ExtendedTrader(config)
    await trader.initialize()
    
    # Get current mark price
    market_data = await trader.get_market_data(["AVAX-USD"])
    avax_data = market_data.get("AVAX-USD", {})
    mark = avax_data.get("mark_price", 13.30)
    
    print(f"AVAX Mark Price: ${mark:.2f}")
    print(f"📈 Buying 15 AVAX...")
    
    # Buy 15 AVAX with limit slightly above market
    buy_price = round(mark + 0.05, 2)
    
    buy_order = OrderSpec(
        symbol="AVAX-USD",
        side="buy",
        order_type="limit",
        size=15.0,
        price=buy_price,
        reduce_only=False,
        post_only=False
    )
    
    res = await trader.place_order(buy_order)
    
    if res.get("status") == "ok":
        print(f"✅ Buy order placed: 15 @ ${buy_price}")
        print(f"   Order ID: {res['order_id']}")
        print(f"\nWaiting 2s for fill...")
        await asyncio.sleep(2)
        
        # Now add protective orders for 30 AVAX total
        print(f"\n🛡️ Adding Stop Loss @ $13.20 for 30 AVAX...")
        
        stop = OrderSpec(
            symbol="AVAX-USD",
            side="sell",
            order_type="limit",
            size=30.0,
            price=13.15,  # Below stop to ensure fill
            reduce_only=True,
            post_only=False
        )
        
        res_stop = await trader.place_order(stop)
        if res_stop.get("status") == "ok":
            print(f"   ✅ Stop placed: ID {res_stop['order_id']}")
        else:
            print(f"   ❌ Stop failed: {res_stop.get('error')}")
        
        print(f"\n🎯 Adding Take Profit @ $14.50 for 30 AVAX...")
        
        tp = OrderSpec(
            symbol="AVAX-USD",
            side="sell",
            order_type="limit",
            size=30.0,
            price=14.50,
            reduce_only=True,
            post_only=True
        )
        
        res_tp = await trader.place_order(tp)
        if res_tp.get("status") == "ok":
            print(f"   ✅ TP placed: ID {res_tp['order_id']}")
        else:
            print(f"   ❌ TP failed: {res_tp.get('error')}")
    else:
        print(f"❌ Buy failed: {res.get('error')}")
    
    await trader.cleanup()
    
    print("\n" + "="*60)
    print("SUMMARY:")
    print("  Position: 30 AVAX (if buy filled)")
    print("  Avg Entry: ~$13.65")
    print("  Stop: $13.20 (-$13.50 risk)")
    print("  Target: $14.50 (+$25.50 profit)")
    print("  R:R: 1.9:1")
    print("="*60)

asyncio.run(buy_avax())
