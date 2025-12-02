#!/usr/bin/env python3
"""
OpenBB Free Data Sources Test - HyperOPS Integration
Test crypto and market data using FREE providers (no API keys)
"""

from openbb import obb
import json
from datetime import datetime

def test_free_data_sources():
    """Test free data sources: CoinGecko (crypto) and YFinance (stocks/indices)"""
    print("=" * 60)
    print("🧪 Testing OpenBB FREE Data Sources (No API Keys)")
    print("=" * 60)
    
    results = {}
    
    # Test 1: Crypto Data (CoinGecko - FREE)
    print("\n📊 Test 1: Crypto Market Data (CoinGecko)")
    try:
        btc_data = obb.crypto.price.historical(
            symbol="BTCUSD",
            provider="fmp",  # Free provider
            interval="1d",
            limit=1
        )
        
        if btc_data and len(btc_data.results) > 0:
            latest = btc_data.results[-1]
            results["BTC"] = {
                "provider": "fmp",
                "price": latest.close,
                "date": str(latest.date),
                "status": "✅ SUCCESS"
            }
            print(f"   ✅ BTC Price: ${latest.close:,.2f}")
            print(f"   Date: {latest.date}")
        else:
            results["BTC"] = {"status": "❌ NO DATA"}
            print("   ❌ No data returned")
            
    except Exception as e:
        results["BTC"] = {"error": str(e), "status": "❌ ERROR"}
        print(f"   ❌ Error: {e}")
    
    # Test 2: ETH Price
    print("\n📊 Test 2: ETH Market Data")
    try:
        eth_data = obb.crypto.price.historical(
            symbol="ETHUSD",
            provider="fmp",
            interval="1d",
            limit=1
        )
        
        if eth_data and len(eth_data.results) > 0:
            latest = eth_data.results[-1]
            results["ETH"] = {
                "provider": "fmp",
                "price": latest.close,
                "date": str(latest.date),
                "status": "✅ SUCCESS"
            }
            print(f"   ✅ ETH Price: ${latest.close:,.2f}")
        else:
            results["ETH"] = {"status": "❌ NO DATA"}
            print("   ❌ No data returned")
            
    except Exception as e:
        results["ETH"] = {"error": str(e), "status": "❌ ERROR"}
        print(f"   ❌ Error: {e}")
    
    # Test 3: Market Index (SPY via YFinance - FREE)
    print("\n📊 Test 3: Stock Market Index (YFinance)")
    try:
        spy_data = obb.equity.price.historical(
            symbol="SPY",
            provider="yfinance",
            interval="1d",
            limit=1
        )
        
        if spy_data and len(spy_data.results) > 0:
            latest = spy_data.results[-1]
            results["SPY"] = {
                "provider": "yfinance",
                "price": latest.close,
                "date": str(latest.date),
                "status": "✅ SUCCESS"
            }
            print(f"   ✅ SPY Price: ${latest.close:.2f}")
        else:
            results["SPY"] = {"status": "❌ NO DATA"}
            print("   ❌ No data returned")
            
    except Exception as e:
        results["SPY"] = {"error": str(e), "status": "❌ ERROR"}
        print(f"   ❌ Error: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    successes = sum(1 for r in results.values() if r.get("status") == "✅ SUCCESS")
    total = len(results)
    
    print(f"Success Rate: {successes}/{total}")
    
    if successes > 0:
        print("\n🎉 FREE DATA ACCESS WORKING!")
        print("\nAvailable Market Data:")
        for symbol, data in results.items():
            if data.get("status") == "✅ SUCCESS":
                print(f"  • {symbol}: ${data['price']:,.2f} (via {data['provider']})")
    
    if successes < total:
        print("\n⚠️  Some sources failed. This is OK - we have working alternatives!")
    
    # Save results
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    output_file = f"/home/kt/Desktop/HyperOPS/📖 Status/openbb_free_test_{timestamp}.json"
    
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📝 Results saved to: openbb_free_test_{timestamp}.json")
    
    return results

if __name__ == "__main__":
    test_free_data_sources()
