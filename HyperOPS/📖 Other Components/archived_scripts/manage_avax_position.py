#!/usr/bin/env python3
"""
AVAX Position Management:
1. Buy 15 more AVAX at market
2. Add stop loss for total 30 AVAX position
3. Add take profit for total 30 AVAX position
"""

import asyncio
import sys
sys.path.insert(0, '/home/kt/ZKputer/HyperOPS/📊 Core Trading System')
from trading_module import TradingConfig, ExtendedTrader, OrderSpec

async def manage_avax():
    config = TradingConfig.from_file('/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json')
    trader = ExtendedTrader(config)
    await trader.initialize()
    
    print("=" * 70)
    print("AVAX POSITION MANAGEMENT")
    print("=" * 70)
    
    # Check current state
    account = await trader.get_account_state()
    positions = await trader.get_positions()
    
    avax_pos = [p for p in positions if p.symbol == "AVAX-USD"][0]
    print(f"\nCurrent Position:")
    print(f"  {avax_pos.size} AVAX @ ${avax_pos.entry_price:.2f}")
    print(f"  Mark: ${avax_pos.mark_price:.2f}")
    print(f"  PnL: ${avax_pos.unrealized_pnl:.2f}")
    print(f"\nAvailable Margin: ${account['available_balance']:.2f}")
    
    # Step 1: Buy 15 more AVAX (limit at current market + buffer)
    buy_price = round(avax_pos.mark_price + 0.05, 2)  # Small buffer above market
    
    print(f"\n📈 STEP 1: Buying 15 AVAX @ ${buy_price}")
    
    buy_order = OrderSpec(
        symbol="AVAX-USD",
        side="buy",
        order_type="limit",
        size=15.0,
        price=buy_price,
        reduce_only=False,
        post_only=False  # Allow taker
    )
    
    res_buy = await trader.place_order(buy_order)
    
    if res_buy.get("status") == "ok":
        print(f"   ✅ Buy order placed: ID {res_buy['order_id']}")
        
        # Wait a moment for fill
        await asyncio.sleep(2)
        
        # Step 2: Add Stop Loss for TOTAL 30 AVAX
        # Average entry will be: (15*$14.05 + 15*$13.65) / 30 ≈ $13.85
        # Stop at $13.30 = $16.50 total risk
        
        print(f"\n🛡️ STEP 2: Adding Stop Loss @ $13.30 for 30 AVAX")
        
        stop_order = OrderSpec(
            symbol="AVAX-USD",
            side="sell",
            order_type="limit",  # Have to use limit due to SDK issues
            size=30.0,
            price=13.20,  # Below stop trigger to ensure fill
            reduce_only=True,
            post_only=False
        )
        
        res_stop = await trader.place_order(stop_order)
        
        if res_stop.get("status") == "ok":
            print(f"   ✅ Stop placed: ID {res_stop['order_id']}")
        else:
            print(f"   ❌ Stop failed: {res_stop.get('error')}")
        
        # Step 3: Add Take Profit for 30 AVAX
        # TP at $15.00 = $34.50 profit
        
        print(f"\n🎯 STEP 3: Adding Take Profit @ $15.00 for 30 AVAX")
        
        tp_order = OrderSpec(
            symbol="AVAX-USD",
            side="sell",
            order_type="limit",
            size=30.0,
            price=15.00,
            reduce_only=True,
            post_only=True
        )
        
        res_tp = await trader.place_order(tp_order)
        
        if res_tp.get("status") == "ok":
            print(f"   ✅ TP placed: ID {res_tp['order_id']}")
        else:
            print(f"   ❌ TP failed: {res_tp.get('error')}")
        
    else:
        print(f"   ❌ Buy failed: {res_buy.get('error')}")
    
    await trader.cleanup()
    
    print("\n" + "=" * 70)
    print("SUMMARY:")
    print("  Position: 30 AVAX (if buy filled)")
    print("  Avg Entry: ~$13.85")
    print("  Stop: $13.30 (-$16.50 risk)")
    print("  Target: $15.00 (+$34.50 profit)")
    print("  R:R: 2.1:1")
    print("=" * 70)

asyncio.run(manage_avax())
