#!/usr/bin/env python3
"""
Check Hyperliquid Trigger Orders (Stop Losses & Take Profits)
"""

import json
from hyperliquid.info import Info
from datetime import datetime

def check_trigger_orders():
    """Query Hyperliquid API for trigger orders"""
    try:
        # Load configuration
        config_path = "/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json"
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        address = config['account_address']
        
        # Initialize Info API
        info = Info(skip_ws=True)
        
        print(f"🔍 Checking trigger orders for: {address}")
        print(f"📅 Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S AEST')}")
        print("=" * 80)
        
        # Get user state for positions
        user_state = info.user_state(address)
        positions = user_state.get('assetPositions', [])
        
        print(f"\n📍 OPEN POSITIONS: {len(positions)}")
        for pos in positions:
            position = pos.get('position', {})
            coin = position.get('coin', 'UNKNOWN')
            szi = float(position.get('szi', 0))
            entry_px = float(position.get('entryPx', 0))
            
            side = "LONG" if szi > 0 else "SHORT"
            print(f"  {coin}-PERP: {side} {abs(szi)} @ ${entry_px}")
        
        # Get open orders (includes trigger orders)
        print(f"\n📋 CHECKING FOR STOP LOSSES & TAKE PROFITS:")
        open_orders = info.open_orders(address)
        
        # Separate regular orders from trigger orders
        trigger_orders = []
        regular_orders = []
        
        for order in open_orders:
            if order.get('orderType') == 'trigger':
                trigger_orders.append(order)
            else:
                regular_orders.append(order)
        
        print(f"\n  Total Open Orders: {len(open_orders)}")
        print(f"  Trigger Orders (SL/TP): {len(trigger_orders)}")
        print(f"  Regular Limit Orders: {len(regular_orders)}")
        
        if trigger_orders:
            print(f"\n✅ TRIGGER ORDERS FOUND ({len(trigger_orders)}):")
            for order in trigger_orders:
                coin = order.get('coin', 'UNKNOWN')
                side = order.get('side', 'UNKNOWN')
                sz = order.get('sz', 0)
                limit_px = order.get('limitPx', 0)
                trigger_px = order.get('triggerPx', 0)
                is_market = order.get('isMarket', False)
                reduce_only = order.get('reduceOnly', False)
                
                order_type = "STOP LOSS" if reduce_only else "TAKE PROFIT"
                
                print(f"\n  {coin}-PERP - {order_type}:")
                print(f"    Side: {side}")
                print(f"    Size: {sz}")
                print(f"    Trigger Price: ${trigger_px}")
                print(f"    Limit Price: ${limit_px}")
                print(f"    Market Order: {is_market}")
                print(f"    Reduce Only: {reduce_only}")
        else:
            print(f"\n❌ NO TRIGGER ORDERS FOUND")
            print(f"   ⚠️  WARNING: No stop losses or take profits are set!")
        
        # Check which positions are missing protection
        print(f"\n🛡️ RISK ANALYSIS:")
        position_coins = set()
        for pos in positions:
            position = pos.get('position', {})
            coin = position.get('coin', 'UNKNOWN')
            position_coins.add(coin)
        
        protected_coins = set()
        for order in trigger_orders:
            coin = order.get('coin', 'UNKNOWN')
            protected_coins.add(coin)
        
        unprotected = position_coins - protected_coins
        
        if unprotected:
            print(f"  ❌ UNPROTECTED POSITIONS ({len(unprotected)}):")
            for coin in unprotected:
                # Get position details
                for pos in positions:
                    position = pos.get('position', {})
                    if position.get('coin') == coin:
                        szi = float(position.get('szi', 0))
                        entry_px = float(position.get('entryPx', 0))
                        position_value = float(position.get('positionValue', 0))
                        unrealized_pnl = float(position.get('unrealizedPnl', 0))
                        
                        side = "LONG" if szi > 0 else "SHORT"
                        print(f"    {coin}-PERP: {side} {abs(szi)} @ ${entry_px}")
                        print(f"      Position Value: ${position_value:.2f}")
                        print(f"      Unrealized PnL: ${unrealized_pnl:.2f}")
                        print(f"      ⚠️  NO STOP LOSS OR TAKE PROFIT SET!")
        else:
            print(f"  ✅ All positions have protection")
        
        print("\n" + "=" * 80)
        
        return {
            'total_positions': len(positions),
            'total_trigger_orders': len(trigger_orders),
            'unprotected_positions': list(unprotected)
        }
        
    except Exception as e:
        print(f"❌ Error checking trigger orders: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = check_trigger_orders()
    
    if result and result['unprotected_positions']:
        print(f"\n⚠️  ACTION REQUIRED: {len(result['unprotected_positions'])} positions need stop losses!")
        exit(1)
    else:
        print(f"\n✅ All positions protected")
        exit(0)
