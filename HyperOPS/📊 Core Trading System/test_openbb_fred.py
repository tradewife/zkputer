#!/usr/bin/env python3
"""
OpenBB FRED Data Test - HyperOPS Integration
Test FRED economic data retrieval for macro intelligence
"""

from openbb import obb
import json
from datetime import datetime

def test_fred_data():
    """Test FRED data retrieval for key macro indicators"""
    print("=" * 60)
    print("🧪 Testing OpenBB FRED Data Access")
    print("=" * 60)
    
    indicators = {
        "DFF": "Federal Funds Rate",
        "T10Y2Y": "10Y-2Y Treasury Yield Spread", 
        "VIXCLS": "VIX (Market Volatility)",
    }
    
    results = {}
    
    for symbol, name in indicators.items():
        try:
            print(f"\n📊 Fetching {name} ({symbol})...")
            
            # Fetch data from FRED
            data = obb.economy.fred_series(symbol=symbol, limit=1)
            
            if data and len(data.results) > 0:
                latest = data.results[0]
                results[symbol] = {
                    "name": name,
                    "value": latest.value,
                    "date": str(latest.date),
                    "status": "✅ SUCCESS"
                }
                print(f"   Value: {latest.value}")
                print(f"   Date: {latest.date}")
            else:
                results[symbol] = {
                    "name": name,
                    "status": "❌ NO DATA"
                }
                print(f"  ❌ No data returned")
                
        except Exception as e:
            results[symbol] = {
                "name": name,
                "error": str(e),
                "status": "❌ ERROR"
            }
            print(f"   ❌ Error: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    successes = sum(1 for r in results.values() if r["status"] == "✅ SUCCESS")
    print(f"Success Rate: {successes}/{len(indicators)}")
    
    if successes == len(indicators):
        print("\n🎉 ALL TESTS PASSED! OpenBB FRED access is working!")
        print("\nMacro Intelligence Available:")
        for symbol, data in results.items():
            if "value" in data:
                print(f"  • {data['name']}: {data['value']}")
    else:
        print("\n⚠️  Some tests failed. Check errors above.")
    
    # Save results
    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M")
    output_file = f"/home/kt/Desktop/HyperOPS/📖 Status/openbb_test_results_{timestamp}.json"
    
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📝 Results saved to: {output_file}")
    
    return results

if __name__ == "__main__":
    test_fred_data()
