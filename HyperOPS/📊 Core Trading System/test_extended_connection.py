#!/usr/bin/env python3
"""
Test Extended connection and fetch account data
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, '/home/kt/ZKputer/HyperOPS/📊 Core Trading System')

from trading_module import TradingConfig, ExtendedTrader


async def test_connection():
    """Test Extended connection"""
    print("🔍 Testing Extended Connection...")
    print("=" * 60)
    
    try:
        # Load config
        config = TradingConfig.from_file(
            "/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json"
        )
        
        print(f"✅ Config loaded")
        print(f"   Vault: {config.vault_number}")
        print(f"   Mainnet: {not config.testnet}")
        
        # Initialize trader
        trader = ExtendedTrader(config)
        await trader.initialize()
        
        print(f"✅ Extended client initialized")
        
        # Get account state
        print("\n💰 Account State:")
        account_state = await trader.get_account_state()
        if account_state:
            print(f"   Equity: ${account_state['equity']:.2f}")
            print(f"   Available: ${account_state['available_balance']:.2f}")
            print(f"   Margin Usage: {account_state['margin_usage']:.2%}")
        
        # Get positions
        print("\n📊 Current Positions:")
        positions = await trader.get_positions()
        if positions:
            for pos in positions:
                print(f"   {pos.symbol}: {pos.side} {pos.size} @ ${pos.entry_price:.2f}")
                print(f"      PnL: ${pos.unrealized_pnl:.2f} | Leverage: {pos.leverage}x")
        else:
            print("   No open positions")
        
        # Get market data
        print("\n📈 Market Data (BTC-USD, ETH-USD, SOL-USD):")
        markets = await trader.get_market_data(["BTC-USD", "ETH-USD", "SOL-USD"])
        for symbol, data in markets.items():
            mark_price = data.get('mark_price', 'N/A')
            print(f"   {symbol}: ${mark_price}")
        
        print("\n" + "=" * 60)
        print("✅ CONNECTION TEST SUCCESSFUL!")
        
        # Cleanup
        await trader.cleanup()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Connection test failed: {e}")
        import traceback
        traceback.print_exc()
        
        # Try to cleanup anyway
        try:
            if 'trader' in locals():
                await trader.cleanup()
        except:
            pass
            
        return False


if __name__ == "__main__":
    result = asyncio.run(test_connection())
    sys.exit(0 if result else 1)
