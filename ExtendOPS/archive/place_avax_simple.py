#!/usr/bin/env python3
"""
Place AVAX Order WITHOUT TP/SL
Add protective orders manually after fill
"""

import asyncio
import sys
sys.path.insert(0, '/home/kt/ZKputer/HyperOPS/📊 Core Trading System')
from trading_module import TradingConfig, ExtendedTrader, OrderSpec

async def place_avax_simple():
    config = TradingConfig.from_file('/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json')
    trader = ExtendedTrader(config)
    await trader.initialize()
    
    account = await trader.get_account_state()
    print(f"Available Margin: ${account['available_balance']:.2f}")
    
    # Simple limit order WITHOUT TP/SL attached
    # We'll add those separately after it fills
    avax_order = OrderSpec(
        symbol="AVAX-USD",
        side="buy",
        order_type="limit",
        size=15.0,
        price=14.05,
        post_only=False
        # NO stop_loss_price or take_profit_price!
    )
    
    print("\n🚀 Placing AVAX Long (No TP/SL attached)")
    print("   15 AVAX @ $14.05")
    print("   Note: Will add SL/TP after order fills")
    
    res = await trader.place_order(avax_order)
    
    if res.get("status") == "ok":
        print(f"\n✅ SUCCESS!")
        print(f"   Order ID: {res['order_id']}")
        print("\n⚠️ IMPORTANT: No automatic stop/target on this order")
        print("   Monitor manually and add stops after fill")
    else:
        print(f"\n❌ Failed: {res.get('error')}")
    
    await trader.cleanup()

asyncio.run(place_avax_simple())
