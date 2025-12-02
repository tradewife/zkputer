#!/usr/bin/env python3
"""
Execute ADA 25x Leverage Long Trade
Dec 2, 2025 07:47 AEST
"""

import asyncio
import sys
import os
from decimal import Decimal

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from trading_module import TradingConfig, ExtendedTrader, OrderSpec

async def execute_ada_long():
    """Execute ADA 25x long with proper stops"""
    
    print("=" * 80)
    print("🎯 ADA 25x LEVERAGE LONG - EXECUTION")
    print("=" * 80)
    
    # Trade parameters
    SYMBOL = "ADA-USD"
    ENTRY_PRICE = 0.377
    STOP_PRICE = 0.352
    TP1_PRICE = 0.390
    TP2_PRICE = 0.400
    TP3_PRICE = 0.420
    POSITION_SIZE = 800  # ADA contracts
    LEVERAGE = 25
    
    print(f"\n📊 TRADE SETUP:")
    print(f"   Symbol: {SYMBOL}")
    print(f"   Entry: ${ENTRY_PRICE}")
    print(f"   Stop Loss: ${STOP_PRICE} (${ENTRY_PRICE - STOP_PRICE:.3f} distance)")
    print(f"   Position Size: {POSITION_SIZE} ADA")
    print(f"   Leverage: {LEVERAGE}x")
    print(f"   Notional: ${POSITION_SIZE * ENTRY_PRICE:.2f}")
    print(f"   Margin Required: ${(POSITION_SIZE * ENTRY_PRICE) / LEVERAGE:.2f}")
    print(f"   Liquidation (est): ~$0.362 (4% from entry)")
    print(f"\n💰 TAKE PROFITS:")
    print(f"   TP1: ${TP1_PRICE} (50% position)")
    print(f"   TP2: ${TP2_PRICE} (30% position)")
    print(f"   TP3: ${TP3_PRICE} (20% position)")
    
    # Load configuration
    try:
        config = TradingConfig.from_file("⚙️ Configuration/config/trading_config.json")
        print(f"\n✅ Config loaded for vault {config.vault_number}")
    except FileNotFoundError:
        print("\n❌ ERROR: Config file not found")
        print("   Create config at: ⚙️ Configuration/config/trading_config.json")
        return
    
    # Initialize trader
    trader = ExtendedTrader(config)
    
    try:
        print("\n🔌 Connecting to Extended Exchange...")
        await trader.initialize()
        
        # Check account
        account = await trader.get_account_state()
        print(f"\n💼 Account Status:")
        print(f"   Equity: ${account.get('equity', 0):.2f}")
        print(f"   Available: ${account.get('available_balance', 0):.2f}")
        
        # Verify we have enough margin
        required_margin = (POSITION_SIZE * ENTRY_PRICE) / LEVERAGE
        available = account.get('available_balance', 0)
        
        if available < required_margin:
            print(f"\n❌ INSUFFICIENT MARGIN")
            print(f"   Required: ${required_margin:.2f}")
            print(f"   Available: ${available:.2f}")
            return
        
        print(f"\n✅ Sufficient margin available")
        
        # Confirmation
        print(f"\n⚠️  WARNING: 25x LEVERAGE IS EXTREME RISK")
        print(f"   Liquidation only 4% away at ~$0.362")
        print(f"   Max loss: $20 (20% of account)")
        
        response = input("\n🚨 EXECUTE THIS TRADE? (type 'EXECUTE' to confirm): ")
        
        if response != "EXECUTE":
            print("\n❌ Trade cancelled")
            return
        
        print("\n🚀 EXECUTING TRADE...")
        print("-" * 80)
        
        # 1. Place entry order (market buy)
        print("\n📈 Placing ENTRY order...")
        entry_order = OrderSpec(
            symbol=SYMBOL,
            side="buy",
            order_type="market",
            size=POSITION_SIZE,
            price=ENTRY_PRICE,  # Reference price for IOC
            reduce_only=False
        )
        
        entry_result = await trader.place_order(entry_order)
        
        if entry_result.get("status") == "ok":
            print(f"   ✅ Entry filled: {entry_result.get('order_id')}")
            print(f"   Size: {POSITION_SIZE} ADA @ ~${ENTRY_PRICE}")
        else:
            print(f"   ❌ Entry FAILED: {entry_result.get('error')}")
            return
        
        # Wait for fill
        await asyncio.sleep(2)
        
        # 2. Place STOP LOSS (critical!)
        print("\n🛡️  Placing STOP LOSS order...")
        stop_order = OrderSpec(
            symbol=SYMBOL,
            side="sell",
            order_type="stop_loss",
            size=POSITION_SIZE,
            stop_loss_price=STOP_PRICE,
            reduce_only=True
        )
        
        stop_result = await trader.place_order(stop_order)
        
        if stop_result.get("status") == "ok":
            print(f"   ✅ Stop Loss set: {stop_result.get('order_id')}")
            print(f"   Trigger: ${STOP_PRICE} (STOP type, not limit!)")
        else:
            print(f"   ⚠️  Stop Loss FAILED: {stop_result.get('error')}")
            print(f"   ⚠️  POSITION IS UNPROTECTED - PLACE MANUAL STOP IMMEDIATELY")
        
        # 3. Place TAKE PROFITS
        print("\n💰 Placing TAKE PROFIT orders...")
        
        # TP1 (50%)
        tp1_order = OrderSpec(
            symbol=SYMBOL,
            side="sell",
            order_type="take_profit",
            size=POSITION_SIZE * 0.5,
            take_profit_price=TP1_PRICE,
            reduce_only=True
        )
        tp1_result = await trader.place_order(tp1_order)
        print(f"   TP1 @ ${TP1_PRICE}: {'✅' if tp1_result.get('status') == 'ok' else '❌'}")
        
        # TP2 (30%)
        tp2_order = OrderSpec(
            symbol=SYMBOL,
            side="sell",
            order_type="take_profit",
            size=POSITION_SIZE * 0.3,
            take_profit_price=TP2_PRICE,
            reduce_only=True
        )
        tp2_result = await trader.place_order(tp2_order)
        print(f"   TP2 @ ${TP2_PRICE}: {'✅' if tp2_result.get('status') == 'ok' else '❌'}")
        
        # TP3 (20%)
        tp3_order = OrderSpec(
            symbol=SYMBOL,
            side="sell",
            order_type="take_profit",
            size=POSITION_SIZE * 0.2,
            take_profit_price=TP3_PRICE,
            reduce_only=True
        )
        tp3_result = await trader.place_order(tp3_order)
        print(f"   TP3 @ ${TP3_PRICE}: {'✅' if tp3_result.get('status') == 'ok' else '❌'}")
        
        # Final status
        print("\n" + "=" * 80)
        print("✅ ADA 25x LONG POSITION OPENED")
        print("=" * 80)
        print(f"\n📍 POSITION:")
        print(f"   {POSITION_SIZE} ADA LONG @ ${ENTRY_PRICE}")
        print(f"   Leverage: {LEVERAGE}x")
        print(f"   Margin: ${required_margin:.2f}")
        
        print(f"\n🛡️  STOP LOSS: ${STOP_PRICE}")
        print(f"💰 TAKE PROFITS: ${TP1_PRICE}, ${TP2_PRICE}, ${TP3_PRICE}")
        
        print(f"\n⚠️  MONITOR CLOSELY:")
        print(f"   Liquidation: ~$0.362 (only 4% away)")
        print(f"   Set alerts at $0.365!")
        
        # Check position
        positions = await trader.get_positions()
        for pos in positions:
            if pos.symbol == SYMBOL:
                print(f"\n📊 Live Position:")
                print(f"   Size: {pos.size}")
                print(f"   Entry: ${pos.entry_price:.4f}")
                print(f"   Mark: ${pos.mark_price:.4f}")
                print(f"   PnL: ${pos.unrealized_pnl:.2f}")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await trader.cleanup()
        print("\n✅ Connection closed")

if __name__ == "__main__":
    asyncio.run(execute_ada_long())
