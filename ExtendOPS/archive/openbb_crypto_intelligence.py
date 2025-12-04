#!/usr/bin/env python3
"""
OpenBB Crypto Intelligence Module - HyperOPS Integration
Provides FREE crypto market data for daily trading routine
Uses: YFinance (no API keys required)
"""

from openbb import obb
from datetime import datetime, timedelta
import json

class CryptoIntelligence:
    """
    Fetch and analyze crypto market data using FREE OpenBB sources
    """
    
    def __init__(self):
        self.provider = "yfinance"  #Free, no API key
        
    def get_crypto_prices(self, symbols=None):
        """
        Get current crypto prices
        
        Args:
            symbols (list): List of crypto symbols, default ["BTC", "ETH", "SOL", "HYPE"]
        
        Returns:
            dict: Price data for each symbol
        """
        if symbols is None:
            symbols = ["BTC", "ETH", "SOL"]
        
        results = {}
        
        for symbol in symbols:
            try:
                ticker = f"{symbol}-USD"
                data = obb.equity.price.historical(
                    symbol=ticker,
                    provider=self.provider,
                    interval="1d",
                    limit=7  # Get last 7 days for trend
                )
                
                if data and len(data.results) > 0:
                    latest = data.results[-1]
                    previous = data.results[0] if len(data.results) > 1 else latest
                    
                    # Calculate 7d change
                    change_7d = ((latest.close - Previous.close) / previous.close * 100) if previous.close else 0
                    
                    results[symbol] = {
                        "price": float(latest.close),
                        "volume_24h": float(latest.volume) if latest.volume else 0,
                        "change_7d_pct": round(change_7d, 2),
                        "date": str(latest.date),
                        "provider": self.provider
                    }
                    
            except Exception as e:
                results[symbol] = {"error": str(e)}
        
        return results
    
    def generate_crypto_snapshot(self, symbols=None):
        """
        Generate crypto market snapshot for daily brief
        
        Returns:
            str: Formatted snapshot for inclusion in trading brief
        """
        prices = self.get_crypto_prices(symbols)
        
        timestamp = datetime.now().strftime("%H:%M AEST")
        
        snapshot = f"""## 💰 CRYPTO MARKET SNAPSHOT (OpenBB - Free Data)

**Timestamp:** {timestamp}  
**Source:** YFinance (No API Key Required)

"""
        
        for symbol, data in prices.items():
            if "error" not in data:
                price = data["price"]
                change = data["change_7d_pct"]
                vol = data["volume_24h"]
                
                trend_emoji = "📈" if change > 0 else "📉"
                
                snapshot += f"**{symbol}:** ${price:,.2f} {trend_emoji} ({change:+.2f}% 7d) | Vol: ${vol/1e9:.2f}B\n"
            else:
                snapshot += f"**{symbol}:** ❌ Error fetching data\n"
        
        snapshot += f"\n**Provenance:** OpenBB Platform (yfinance provider)\n"
        
        return snapshot
    
    def get_hyperliquid_comparison(self):
        """
        Get prices to compare with Hyperliquid API data
        Returns current BTC, ETH prices for cross-reference
        """
        symbols = ["BTC", "ETH"]
        prices = self.get_crypto_prices(symbols)
        
        comparison = {}
        for symbol, data in prices.items():
            if "error" not in data:
                comparison[symbol] = {
                    "openbb_price": data["price"],
                    "source": "yfinance",
                    "timestamp": data["date"]
                }
        
        return comparison


def main():
    """Test the crypto intelligence module"""
    print("🧪 Testing Crypto Intelligence Module")
    print("=" * 60)
    
    intel = CryptoIntelligence()
    
    # Test 1: Get prices
    print("\n📊 Current Crypto Prices:")
    prices = intel.get_crypto_prices()
    print(json.dumps(prices, indent=2))
    
    # Test 2: Generate snapshot
    print("\n📰 Daily Trading Brief Snapshot:")
    print(intel.generate_snapshot())
    
    # Test 3: Hyperliquid comparison
    print("\n🔄 Hyperliquid Comparison Data:")
    comparison = intel.get_hyperliquid_comparison()
    print(json.dumps(comparison, indent=2))


if __name__ == "__main__":
    main()
