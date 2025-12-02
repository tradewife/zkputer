#!/usr/bin/env python3
"""
Check Hyperliquid Account Status
Query positions, orders, and recent fills
"""

import json
import sys
from hyperliquid.info import Info
from datetime import datetime

def check_account_status():
    """Query Hyperliquid API for account status"""
    try:
        # Load configuration
        config_path = "/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json"
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        address = config['account_address']
        
        # Initialize Info API (read-only, no wallet needed)
        info = Info(skip_ws=True)
        
        print(f"🔍 Checking account: {address}")
        print(f"📅 Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S AEST')}")
        print("=" * 80)
        
        # Get account state
        print("\n📊 ACCOUNT STATE:")
        user_state = info.user_state(address)
        
        if user_state:
            # Account value
            margin_summary = user_state.get('marginSummary', {})
            account_value = float(margin_summary.get('accountValue', 0))
            total_margin_used = float(margin_summary.get('totalMarginUsed', 0))
            total_ntl_pos = float(margin_summary.get('totalNtlPos', 0))
            
            print(f"  Account Value: ${account_value:.2f}")
            print(f"  Margin Used: ${total_margin_used:.2f}")
            print(f"  Total Position Value: ${total_ntl_pos:.2f}")
            
            # Positions
            positions = user_state.get('assetPositions', [])
            print(f"\n📍 OPEN POSITIONS ({len(positions)}):")
            
            if positions:
                for pos in positions:
                    position = pos.get('position', {})
                    coin = position.get('coin', 'UNKNOWN')
                    szi = float(position.get('szi', 0))
                    entry_px = float(position.get('entryPx', 0))
                    position_value = float(position.get('positionValue', 0))
                    unrealized_pnl = float(position.get('unrealizedPnl', 0))
                    leverage = position.get('leverage', {}).get('value', 0)
                    
                    side = "LONG" if szi > 0 else "SHORT"
                    print(f"\n  {coin}-PERP:")
                    print(f"    Side: {side}")
                    print(f"    Size: {abs(szi)}")
                    print(f"    Entry: ${entry_px:.4f}")
                    print(f"    Position Value: ${position_value:.2f}")
                    print(f"    Unrealized PnL: ${unrealized_pnl:.2f}")
                    print(f"    Leverage: {leverage}x")
            else:
                print("  No open positions")
        
        # Get open orders
        print("\n📋 OPEN ORDERS:")
        open_orders = info.open_orders(address)
        
        if open_orders:
            for order in open_orders:
                coin = order.get('coin', 'UNKNOWN')
                side = order.get('side', 'UNKNOWN')
                sz = order.get('sz', 0)
                limit_px = order.get('limitPx', 0)
                oid = order.get('oid', 'UNKNOWN')
                
                print(f"\n  {coin}-PERP:")
                print(f"    Order ID: {oid}")
                print(f"    Side: {side}")
                print(f"    Size: {sz}")
                print(f"    Limit Price: ${limit_px}")
        else:
            print("  No open orders")
        
        # Get recent fills (last 24h)
        print("\n📈 RECENT FILLS (Last 50):")
        user_fills = info.user_fills(address)
        
        if user_fills:
            # Filter fills from Nov 25 onwards
            recent_fills = []
            for fill in user_fills[:50]:  # Last 50 fills
                time_ms = fill.get('time', 0)
                fill_time = datetime.fromtimestamp(time_ms / 1000)
                
                # Only show fills from Nov 25 onwards
                if fill_time.date() >= datetime(2025, 11, 25).date():
                    recent_fills.append(fill)
            
            if recent_fills:
                for fill in recent_fills:
                    coin = fill.get('coin', 'UNKNOWN')
                    side = fill.get('side', 'UNKNOWN')
                    px = fill.get('px', 0)
                    sz = fill.get('sz', 0)
                    time_ms = fill.get('time', 0)
                    fill_time = datetime.fromtimestamp(time_ms / 1000)
                    closed_pnl = fill.get('closedPnl', '0')
                    
                    print(f"\n  {fill_time.strftime('%Y-%m-%d %H:%M:%S')} | {coin}-PERP")
                    print(f"    Side: {side} | Size: {sz} | Price: ${px}")
                    print(f"    Closed PnL: ${closed_pnl}")
            else:
                print("  No fills since Nov 25")
        else:
            print("  No recent fills found")
        
        print("\n" + "=" * 80)
        print("✅ Account check complete")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking account: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    check_account_status()
