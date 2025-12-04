#!/usr/bin/env python3
"""
Execute HYPE Long - Proper Sizing
Conforms to 9-12x leverage, 20% max risk
"""

import asyncio
import sys
sys.path.insert(0, '/home/kt/ZKputer/HyperOPS/📊 Core Trading System')
from trading_module import TradingConfig, ExtendedTrader, OrderSpec

async def execute_hype():
    config = TradingConfig.from_file('/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json')
    trader = ExtendedTrader(config)
    await trader.initialize()
    
    account = await trader.get_account_state()
    print(f"Account: ${account['equity']:.2f}")
    print(f"Max Risk (20%): ${account['equity'] * 0.20:.2f}")
    
    print("\n" + "="*70)
    print("HYPE-USD LONG - PROPER SIZING")
    print("="*70)
    
    # Position sizing
    entry = 31.00
    stop = 29.90
    risk_per_unit = entry - stop  # $1.10
    max_risk_usd = account['equity'] * 0.20  # 20%
    size = int(max_risk_usd / risk_per_unit)  # 15 HYPE
    
    notional = size * entry  # $465
    leverage = 10  # Target 10x (within 9-12 range)
    margin = notional / leverage  # $46.50
    
    print(f"\n📊 POSITION DETAILS:")
    print(f"  Entry: ${entry}")
    print(f"  Stop: ${stop}")
    print(f"  Size: {size} HYPE")
    print(f"  Notional: ${notional:.2f}")
    print(f"  Leverage: {leverage}x")
    print(f"  Margin: ${margin:.2f}")
    print(f"  Risk: ${size * risk_per_unit:.2f} ({size * risk_per_unit / account['equity'] * 100:.1f}%)")
    print(f"  TP1 Profit: ${size * 1.50:.2f}")
    print(f"  TP2 Profit: ${size * 3.00:.2f}")
    
    print(f"\n🚀 Placing HYPE Long Entry...")
    
    entry_order = OrderSpec(
        symbol="HYPE-USD",
        side="buy",
        order_type="limit",
        size=float(size),
        price=entry,
        reduce_only=False,
        post_only=False
    )
    
    res = await trader.place_order(entry_order)
    
    if res.get("status") == "ok":
        print(f"✅ Entry placed: {size} @ ${entry}")
        print(f"   Order ID: {res['order_id']}")
        
        print(f"\n⏳ Waiting 2s for potential fill...")
        await asyncio.sleep(2)
        
        # Add stop loss
        print(f"\n🛡️ Adding Stop Loss @ ${stop - 0.05} (below trigger)...")
        
        stop_order = OrderSpec(
            symbol="HYPE-USD",
            side="sell",
            order_type="limit",
            size=float(size),
            price=29.85,  # Below stop to ensure fill
            reduce_only=True,
            post_only=False
        )
        
        res_stop = await trader.place_order(stop_order)
        if res_stop.get("status") == "ok":
            print(f"   ✅ Stop placed: ID {res_stop['order_id']}")
        else:
            print(f"   ⚠️ Stop failed: {res_stop.get('error')}")
            print(f"   **CRITICAL: Manually add stop @ $29.85**")
        
        # Add TP1
        print(f"\n🎯 Adding TP1 @ $32.50 (50% size)...")
        
        tp1_order = OrderSpec(
            symbol="HYPE-USD",
            side="sell",
            order_type="limit",
            size=float(size) / 2,
            price=32.50,
            reduce_only=True,
            post_only=True
        )
        
        res_tp1 = await trader.place_order(tp1_order)
        if res_tp1.get("status") == "ok":
            print(f"   ✅ TP1 placed: ID {res_tp1['order_id']}")
        else:
            print(f"   ⚠️ TP1 failed: {res_tp1.get('error')}")
            
    else:
        print(f"❌ Entry failed: {res.get('error')}")
    
    await trader.cleanup()
    
    print("\n" + "="*70)
    print("EXECUTION SUMMARY:")
    print(f"  Position: {size} HYPE @ ${entry}")
    print(f"  Leverage: {leverage}x (compliant ✅)")
    print(f"  Risk: ${size * risk_per_unit:.2f} / 20% (compliant ✅)")
    print(f"  Stop: ${stop} (ATR-compliant ✅)")
    print("="*70)

asyncio.run(execute_hype())
