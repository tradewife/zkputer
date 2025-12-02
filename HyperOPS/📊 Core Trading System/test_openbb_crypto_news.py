#!/usr/bin/env python3
"""
OpenBB Crypto & News - FREE Data Test
Focus: Crypto prices and market news (no API keys required)
"""

from openbb import obb
import json
from datetime import datetime

def test_free_crypto_and_news():
    """Test FREE crypto and news data sources"""
    print("=" * 70)
    print("🚀 Testing OpenBB: FREE Crypto + News (Zero API Keys)")
    print("=" * 70)
    
    results = {}
    
    # Test different free providers for crypto
    crypto_providers = ["yfinance", "cboe", "tmx"]  # Free providers
    crypto_symbols = ["BTC-USD", "ETH-USD", "SOL-USD"]
    
    print("\n📊 CRYPTO PRICE DATA (YFinance - FREE)")
    print("-" * 70)
    
    for symbol in crypto_symbols:
        try:
            data = obb.equity.price.historical(
                symbol=symbol,
                provider="yfinance",
                interval="1d",
                limit=1
            )
            
            if data and len(data.results) > 0:
                latest = data.results[-1]
                ticker = symbol.replace("-USD", "")
                results[ticker] = {
                    "provider": "yfinance",
                    "price": float(latest.close),
                    "volume": float(latest.volume) if latest.volume else 0,
                    "date": str(latest.date),
                    "status": "✅"
                }
                print(f"✅ {ticker:6} ${latest.close:>10,.2f}  Vol: {latest.volume:>15,}")
            else:
                print(f"❌ {symbol}: No data")
                
        except Exception as e:
            print(f"❌ {symbol}: {str(e)[:50]}")
    
    # Test News (if available without API key)
    print("\n📰 MARKET NEWS (Checking free sources...)")
    print("-" * 70)
    
    try:
        # Try to get general market news
        news = obb.news.world(limit=5)
        
        if news and len(news.results) > 0:
            results["news"] = {
                "count": len(news.results),
                "headlines": [],
                "status": "✅"
            }
            
            print(f"✅ Found {len(news.results)} news items:\n")
            for i, article in enumerate(news.results[:5], 1):
                headline = article.title[:60] if hasattr(article, 'title') else "No title"
                results["news"]["headlines"].append(headline)
                print(f"   {i}. {headline}...")
        else:
            print("⚠️  No news data (may require API key)")
            results["news"] = {"status": "❌", "note": "Requires API key"}
            
    except Exception as e:
        print(f"⚠️  News: {str(e)[:80]}")
        results["news"] = {"status": "❌", "error": str(e)[:100]}
    
    # Alternative: Check crypto-specific news
    print("\n📰 CRYPTO NEWS (Checking...)")
    print("-" * 70)
    
    try:
        crypto_news = obb.crypto.news(limit=3)
        
        if crypto_news and len(crypto_news.results) > 0:
            print(f"✅ Found {len(crypto_news.results)} crypto news items\n")
            for i, article in enumerate(crypto_news.results[:3], 1):
                headline = article.title[:60] if hasattr(article, 'title') else str(article)[:60]
                print(f"   {i}. {headline}...")
        else:
            print("⚠️  No crypto news available")
            
    except Exception as e:
        print(f"⚠️  Crypto News: {str(e)[:80]}")
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    
    crypto_count = sum(1 for k, v in results.items() 
                      if k in ["BTC", "ETH", "SOL"] and v.get("status") == "✅")
    
    print(f"\n✅ Working Crypto Prices: {crypto_count}/3")
    
    if crypto_count > 0:
        print("\n🎉 SUCCESS! Free crypto data is working!")
        print("\nAvailable Data for HyperOPS:")
        for ticker in ["BTC", "ETH", "SOL"]:
            if ticker in results and results[ticker].get("status") == "✅":
                data = results[ticker]
                print(f"  • {ticker}: ${data['price']:,.2f}")
    
    # Save results
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    output_file = f"/home/kt/Desktop/HyperOPS/📖 Status/openbb_crypto_test_{timestamp}.json"
    
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📝 Results: openbb_crypto_test_{timestamp}.json")
    
    return results

if __name__ == "__main__":
    test_free_crypto_and_news()
