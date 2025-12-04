#!/usr/bin/env python3
"""
ADA 25x Long - CORRECTED EXECUTION
Using proper Extended SDK order placement
"""
import asyncio
import sys
sys.path.insert(0, '/home/kt/ZKputer/HyperOPS/📊 Core Trading System')
from trading_module import TradingConfig, ExtendedTrader, OrderSpec

async def execute_ada():
    print("="*80)
    print("🎯 ADA 25x LONG - CORRECTED EXECUTION")
    print("="*80)
    
    config = TradingConfig.from_file('/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json')
    trader = ExtendedTrader(config)
    await trader.initialize()
    
    # Get current ADA price
    market_data = await trader.get_market_data(["ADA-USD"])
    ada_data = market_data.get("ADA-USD", {})
    mark = ada_data.get("mark_price", 0.377)
    
    print(f"\n📊 ADA Mark Price: ${mark:.4f}")
    
    # Check account
    account = await trader.get_account_state()
    print(f"💼 Account: ${account.get('equity', 0):.2f} equity, ${account.get('available_balance', 0):.2f} available")
    
    # Trade params
    SIZE = 800
    STOP = 0.352
    TP1, TP2, TP3 = 0.390, 0.400, 0.420
    
    required_margin = (SIZE * mark) / 25
    print(f"\n💰 Trade: {SIZE} ADA @ ${mark:.4f} (25x leverage)")
    print(f"   Margin needed: ${required_margin:.2f}")
    print(f"   Stop: ${STOP} | TPs: ${TP1}/${TP2}/${TP3}")
    
    confirm = input("\n🚨 EXECUTE? (type YES): ")
    if confirm != "YES":
        print("❌ Cancelled")
        await trader.cleanup()
        return
    
    print("\n🚀 EXECUTING...")
    
    # 1. ENTRY - Use limit order at current mark + small buffer
    entry_price = round(mark + 0.001, 4)
    print(f"\n[1/4] Entry: BUY {SIZE} ADA @ ${entry_price}")
    
    entry = OrderSpec(
        symbol="ADA-USD",
        side="buy",
        order_type="limit",
        size=SIZE,
        price=entry_price,
        reduce_only=False,
        post_only=False
    )
    
    result = await trader.place_order(entry)
    if result.get("status") == "ok":
        print(f"   ✅ Entry placed: {result.get('order_id')}")
        await asyncio.sleep(3)
    else:
        print(f"   ❌ FAILED: {result.get('error')}")
        await trader.cleanup()
        return
    
    # 2. STOP LOSS - Place protective stop
    print(f"\n[2/4] Stop Loss: SELL {SIZE} @ ${STOP}")
    
    stop = OrderSpec(
        symbol="ADA-USD",
        side="sell",
        order_type="stop_loss",
        size=SIZE,
        stop_loss_price=STOP,
        reduce_only=True
    )
    
    result_stop = await trader.place_order(stop)
    if result_stop.get("status") == "ok":
        print(f"   ✅ Stop placed: {result_stop.get('order_id')}")
    else:
        print(f"   ⚠️  STOP FAILED: {result_stop.get('error')}")
        print("   🚨 POSITION MAY BE UNPROTECTED!")
    
    # 3. TAKE PROFITS
    print(f"\n[3/4] Take Profits...")
    
    tp1 = OrderSpec(
        symbol="ADA-USD",
        side="sell",
        order_type="limit",
        size=400,
        price=TP1,
        reduce_only=True,
        post_only=True
    )
    r1 = await trader.place_order(tp1)
    print(f"   TP1 (400 @ ${TP1}): {'✅' if r1.get('status') == 'ok' else '❌'}")
    
    tp2 = OrderSpec(
        symbol="ADA-USD",
        side="sell",
        order_type="limit",
        size=240,
        price=TP2,
        reduce_only=True,
        post_only=True
    )
    r2 = await trader.place_order(tp2)
    print(f"   TP2 (240 @ ${TP2}): {'✅' if r2.get('status') == 'ok' else '❌'}")
    
    tp3 = OrderSpec(
        symbol="ADA-USD",
        side="sell",
        order_type="limit",
        size=160,
        price=TP3,
        reduce_only=True,
        post_only=True
    )
    r3 = await trader.place_order(tp3)
    print(f"   TP3 (160 @ ${TP3}): {'✅' if r3.get('status') == 'ok' else '❌'}")
    
    # 4. VERIFY
    print(f"\n[4/4] Verifying position...")
    await asyncio.sleep(2)
    
    positions = await trader.get_positions()
    ada_pos = None
    for p in positions:
        if "ADA" in p.symbol:
            ada_pos = p
            print(f"\n✅ POSITION CONFIRMED:")
            print(f"   {p.size} ADA {p.side.upper()}")
            print(f"   Entry: ${p.entry_price:.4f}")
            print(f"   Mark: ${p.mark_price:.4f}")
            print(f"   PnL: ${p.unrealized_pnl:.2f}")
            break
    
    if not ada_pos:
        print("\n⚠️  NO ADA POSITION FOUND - Check Extended UI!")
    
    await trader.cleanup()
    
    print("\n" + "="*80)
    print("✅ EXECUTION COMPLETE")
    print("="*80)
    print(f"\n⚠️  Monitor liquidation at ~$0.362 (4% from entry)")

asyncio.run(execute_ada())
