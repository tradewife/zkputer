#!/usr/bin/env python3
"""
Quick Market Data Fetcher for HyperOPS Daily Routine
Uses Extended SDK to fetch real-time market data for core assets
"""

import sys
import asyncio
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from trading_module import ExtendedTrader, TradingConfig
from decimal import Decimal


def format_funding_rate(rate):
    """Format funding rate as percentage"""
    if rate is None:
        return "N/A"
    return f"{float(rate) * 100:.4f}%"


def format_price(price):
    """Format price with appropriate precision"""
    if price is None:
        return "N/A"
    price_float = float(price)
    if price_float < 1:
        return f"${price_float:.4f}"
    elif price_float < 100:
        return f"${price_float:.2f}"
    else:
        return f"${price_float:,.0f}"


async def get_market_data():
    """Fetch and display market data for core assets"""
    
    # Load config and initialize trader
    try:
        config_path = '/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json'
        config = TradingConfig.from_file(config_path)
        trader = ExtendedTrader(config)
        
        success = await trader.initialize()
        if not success:
            print("ERROR: Failed to initialize trader")
            return
            
    except Exception as e:
        print(f"ERROR initializing trader: {e}")
        return
    
    # Core assets to scan
    markets = ["BTC-USD", "ETH-USD", "SOL-USD", "ADA-USD", "AVAX-USD", "HYPE-USD"]
    
    print("=" * 80)
    print(f"EXTENDED EXCHANGE - MARKET SCAN")
    print("=" * 80)
    print()
    
    # Get account info
    try:
        balance = await trader.get_account_state()
        print(f"Account Equity: ${float(balance.get('equity', 0)):.2f}")
        print(f"Available Margin: ${float(balance.get('available_balance', 0)):.2f}")
        print()
    except Exception as e:
        print(f"Could not fetch balance: {e}")
        print()
    
    # Market data header
    print(f"{'Market':<12} {'Last Price':>12} {'Mark Price':>12} {'Funding':>10} {'24h Vol':>15} {'OI':>12}")
    print("-" * 80)
    
    for market in markets:
        try:
            # Get market info
            market_data_dict = await trader.get_market_data([market])
            
            if market_data_dict and market in market_data_dict:
                stats = market_data_dict[market]
                
                last_price = format_price(stats.get('last_price'))
                mark_price = format_price(stats.get('mark_price'))
                funding = format_funding_rate(stats.get('funding_rate'))
                volume = stats.get('daily_volume', '0')
                oi = stats.get('open_interest', '0')
                
                # Format volume in millions/billions
                vol_num = float(volume)
                if vol_num >= 1_000_000_000:
                    vol_str = f"${vol_num/1_000_000_000:.2f}B"
                elif vol_num >= 1_000_000:
                    vol_str = f"${vol_num/1_000_000:.2f}M"
                else:
                    vol_str = f"${vol_num:,.0f}"
                
                # Format OI
                oi_num = float(oi)
                if oi_num >= 1_000_000:
                    oi_str = f"${oi_num/1_000_000:.2f}M"
                else:
                    oi_str = f"${oi_num:,.0f}"
                
                print(f"{market:<12} {last_price:>12} {mark_price:>12} {funding:>10} {vol_str:>15} {oi_str:>12}")
            else:
                print(f"{market:<12} {'ERROR':>12} {'N/A':>12} {'N/A':>10} {'N/A':>15} {'N/A':>12}")
                
        except Exception as e:
            print(f"{market:<12} ERROR: {str(e)[:50]}")
    
    print()
    print("=" * 80)
    
    # Get open positions
    try:
        positions = await trader.get_positions()
        if positions:
            print()
            print("OPEN POSITIONS:")
            print("-" * 80)
            for pos in positions:
                side = pos.side.upper()
                market = pos.symbol
                size = pos.size
                entry = format_price(pos.entry_price)
                mark = format_price(pos.mark_price)
                pnl = pos.unrealized_pnl
                pnl_str = f"${pnl:+.2f}"
                
                print(f"  • {market} {side} {size} @ {entry} (Mark: {mark}, PnL: {pnl_str})")
            print()
    except Exception as e:
        print(f"Could not fetch positions: {e}")
    
    # Cleanup
    await trader.cleanup()


if __name__ == "__main__":
    asyncio.run(get_market_data())
