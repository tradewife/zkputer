#!/usr/bin/env python3
"""
Execute HyperOPS Daily Trades - 2025-11-25
Adjusted for $57 available capital
"""

import sys
sys.path.append('/home/kt/Desktop/HyperOPS/📊 Core Trading System')

from hyperliquid_executor_production import HyperliquidExecutor

if __name__ == "__main__":
    # Adjusted trade sizes for $57 capital
    # BTC: $88,500 entry, aimed for ~$310 notional (11× leverage from $28.50)
    # ETH: $2,940 entry, aimed for ~$315 notional (11× leverage from $28.50)
    
    trade_list = [
        {
            "symbol": "BTC",
            "side": "buy",
            "size": 0.0035,  # ~$310 notional at $88,500
            "price": 88500
        },
        {
            "symbol": "ETH",
            "side": "buy",
            "size": 0.11,  # ~$323 notional at $2,940
            "price": 2940
        }
    ]
    
    print("=" * 60)
    print("🚀 HYPEROPS TRADE EXECUTION - 2025-11-25 11:57 AEST")
    print("=" * 60)
    print(f"\n📊 TRADE SPECIFICATIONS:")
    print(f"\nTRADE 1: BTC MEAN REVERSION LONG")
    print(f"  Entry: $88,500")
    print(f"  Size: 0.0035 BTC (~$310 notional)")
    print(f"  Stop: $87,000 | TP1: $90,750 | TP2: $93,000")
    print(f"  Setup: Extreme fear + whale accumulation")
    
    print(f"\nTRADE 2: ETH SMART MONEY FOLLOW LONG")
    print(f"  Entry: $2,940")
    print(f"  Size: 0.11 ETH (~$323 notional)")
    print(f"  Stop: $2,840 | TP1: $3,090 | TP2: $3,240")
    print(f"  Setup: Following $5.88M Tidal Whale")
    
    print(f"\n💰 ACCOUNT INFO:")
    print(f"  Available Capital: $57")
    print(f"  Total Notional: ~$633 (~11× leverage)")
    print(f"  Total Risk: ~$16 combined")
    
    print("\n" + "=" * 60)
    print("⚠️  EXECUTING LIVE TRADES ON MAINNET...")
    print("=" * 60 + "\n")
    
    # Execute
    executor = HyperliquidExecutor()
    executor.main(trade_list)
