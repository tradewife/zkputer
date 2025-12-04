#!/usr/bin/env python3
"""
Place Stop Loss and Take Profit Orders
Executes trigger orders for all 4 open positions
"""

import json
import time
from hyperliquid.exchange import Exchange
from eth_account import Account

# Load config
config_path = "/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json"
with open(config_path, 'r') as f:
    config = json.load(f)

print("🔄 Waiting 5 seconds for rate limit...")
time.sleep(5)

# Initialize exchange
account = Account.from_key(config['secret_key'])
exchange = Exchange(
    wallet=account,
    account_address=config['account_address']
)

print("🚀 PLACING STOP LOSS & TAKE PROFIT ORDERS")
print("=" * 80)

# Order specifications
orders = [
    # BTC-PERP
    {
        "symbol": "BTC",
        "type": "stop_loss",
        "side": "sell",
        "size": 0.0035,
        "trigger_px": 88071.0,
        "limit_px": 87500.0,  # Execute slightly below trigger
        "reduce_only": True,
        "description": "BTC Stop Loss @ $88,071 (breakeven)"
    },
    {
        "symbol": "BTC",
        "type": "take_profit_1",
        "side": "sell",
        "size": 0.00175,  # 50%
        "limit_px": 90750.0,
        "reduce_only": True,
        "description": "BTC TP1 @ $90,750 (50% position)"
    },
    {
        "symbol": "BTC",
        "type": "take_profit_2",
        "side": "sell",
        "size": 0.00175,  # 50%
        "limit_px": 93000.0,
        "reduce_only": True,
        "description": "BTC TP2 @ $93,000 (50% position)"
    },
    
    # ETH-PERP
    {
        "symbol": "ETH",
        "type": "stop_loss",
        "side": "sell",
        "size": 0.11,
        "trigger_px": 2942.0,
        "limit_px": 2920.0,  # Execute slightly below trigger
        "reduce_only": True,
        "description": "ETH Stop Loss @ $2,942 (breakeven)"
    },
    {
        "symbol": "ETH",
        "type": "take_profit_1",
        "side": "sell",
        "size": 0.055,  # 50%
        "limit_px": 3090.0,
        "reduce_only": True,
        "description": "ETH TP1 @ $3,090 (50% position)"
    },
    {
        "symbol": "ETH",
        "type": "take_profit_2",
        "side": "sell",
        "size": 0.055,  # 50%
        "limit_px": 3240.0,
        "reduce_only": True,
        "description": "ETH TP2 @ $3,240 (50% position)"
    },
    
    # SOL-PERP
    {
        "symbol": "SOL",
        "type": "stop_loss",
        "side": "sell",
        "size": 0.2,
        "trigger_px": 140.0,
        "limit_px": 138.0,  # Execute slightly below trigger
        "reduce_only": True,
        "description": "SOL Stop Loss @ $140 (protective)"
    },
    {
        "symbol": "SOL",
        "type": "take_profit",
        "side": "sell",
        "size": 0.2,
        "limit_px": 150.0,
        "reduce_only": True,
        "description": "SOL TP @ $150 (full position)"
    },
    
    # XRP-PERP
    {
        "symbol": "XRP",
        "type": "stop_loss",
        "side": "sell",
        "size": 24.0,
        "trigger_px": 2.15,
        "limit_px": 2.13,  # Execute slightly below trigger
        "reduce_only": True,
        "description": "XRP Stop Loss @ $2.15 (protective)"
    },
    {
        "symbol": "XRP",
        "type": "take_profit",
        "side": "sell",
        "size": 24.0,
        "limit_px": 2.35,
        "reduce_only": True,
        "description": "XRP TP @ $2.35 (full position)"
    },
]

results = []

for order in orders:
    try:
        print(f"\n📝 {order['description']}")
        
        # Determine order method
        if "stop" in order['type']:
            # Trigger order (stop loss)
            result = exchange.order(
                name=order['symbol'],
                is_buy=False,  # Selling to close long
                sz=order['size'],
                limit_px=order['limit_px'],
                order_type={
                    "trigger": {
                        "triggerPx": order['trigger_px'],
                        "isMarket": False,
                        "tpsl": "sl"  # Stop loss type
                    }
                },
                reduce_only=True
            )
        else:
            # Limit order (take profit)
            result = exchange.order(
                name=order['symbol'],
                is_buy=False,  # Selling to close long
                sz=order['size'],
                limit_px=order['limit_px'],
                order_type={"limit": {"tif": "Gtc"}},  # Good til cancel
                reduce_only=True
            )
        
        print(f"✅ Order placed successfully")
        print(f"   Result: {result}")
        results.append({
            "order": order['description'],
            "status": "success",
            "result": result
        })
        
        # Wait between orders to avoid rate limiting
        time.sleep(2)
        
    except Exception as e:
        print(f"❌ Error placing order: {e}")
        results.append({
            "order": order['description'],
            "status": "error",
            "error": str(e)
        })

print("\n" + "=" * 80)
print("📊 EXECUTION SUMMARY:")
print(f"   Total Orders: {len(orders)}")
print(f"   Successful: {sum(1 for r in results if r['status'] == 'success')}")
print(f"   Failed: {sum(1 for r in results if r['status'] == 'error')}")

# Save results
with open('/home/kt/ZKputer/HyperOPS/research_logs/2025-11-27/stop_tp_execution.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\n✅ Results saved to: stop_tp_execution.json")
print("\n⚠️  IMPORTANT: Verify orders on Hyperliquid UI")
