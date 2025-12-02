# OpenBB FREE Data Providers for HyperOPS

**Updated:** 2025-11-25  
**Focus:** Crypto trading, market news, and intelligence

---

## ✅ Currently Working (NO API KEY)

### YFinance
- **Status:** ✅ Active & tested
- **Data:** Crypto prices (BTC, ETH, SOL), stocks, indices
- **Cost:** FREE, no API key required
- **Limits:** None for basic usage
- **Use Case:** Cross-reference Hyperliquid prices, market context

---

## 🔑 FREE Tier Providers (API Key Required)

### 1. **Alpha Vantage** ⭐ RECOMMENDED
- **Data:** Crypto, stocks, forex, technical indicators
- **Free Tier:** 25 API calls/day
- **Registration:** https://www.alphavantage.co/support/#api-key
- **Cost:** $0 (free forever)
- **Limits:** 25 requests/day
- **Use For:** Daily crypto data refresh, technical indicators
- **HyperOPS Value:** 8/10 - Perfect for daily routine

### 2. **Financial Modeling Prep (FMP)** ⭐
- **Data:** Crypto prices, company data, market news
- **Free Tier:** 250 API calls/day
- **Registration:** https://financialmodelingprep.com/developer/docs/
- **Cost:** $0 (free tier), Paid starts at $14/mo
- **Limits:** 250 requests/day (generous)
- **Use For:** Crypto data, news aggregation
- **HyperOPS Value:** 7/10 - Good backup source

### 3. **Polygon.io** ⭐⭐ HIGHLY RECOMMENDED
- **Data:** Real-time & historical crypto, stocks, forex
- **Free Tier:** 5 API calls/minute
- **Registration:** https://polygon.io/
- **Cost:** $0 (starter tier), Paid starts at $29/mo
- **Limits:** 5 calls/min (very usable)
- **Use For:** Real-time crypto prices, market snapshots
- **HyperOPS Value:** 9/10 - Excellent for live data

### 4. **CoinGecko** 🪙
- **Data:** Comprehensive crypto data, trending coins, market cap
- **Free Tier:** Demo API (30 calls/min)
- **Registration:** https://www.coingecko.com/en/api
- **Cost:** $0 (demo), Paid starts at $129/mo
- **Limits:** 30 calls/min, 10,000/month
- **Use For:** Crypto market overview, trending coins
- **HyperOPS Value:** 8/10 - Best for crypto-specific data

### 5. **FRED (St. Louis Fed)** 📊
- **Data:** Economic indicators, macro data
- **Free Tier:** Unlimited
- **Registration:** https://fredaccount.stlouisfed.org/
- **Cost:** $0 (completely free)
- **Limits:** None
- **Use For:** Fed policy, yield curve, macro regime detection
- **HyperOPS Value:** 6/10 - Useful for macro context

### 6. **Tiingo**
- **Data:** Stocks, crypto, news
- **Free Tier:** 1,000 unique symbols/month
- **Registration:** https://www.tiingo.com/
- **Cost:** $0 (free tier)
- **Limits:** Moderate
- **Use For:** Backup crypto data source
- **HyperOPS Value:** 5/10 - Redundant with others

### 7. **Benzinga** 📰
- **Data:** Financial news, market moving events
- **Free Tier:** Limited trial
- **Registration:** https://www.benzinga.com/apis
- **Cost:** Trial, then paid ($30-100/mo)
- **Limits:** Trial period only
- **Use For:** Breaking news, catalyst detection
- **HyperOPS Value:** 4/10 - Expensive after trial

### 8. **Biztoc** 📰
- **Data:** Aggregated business/crypto news
- **Free Tier:** Yes (community tier)
- **Registration:** https://biztoc.com/
- **Cost:** $0
- **Limits:** Basic access
- **Use For:** News aggregation
- **HyperOPS Value:** 6/10 - Good for headlines

---

## 🎯 RECOMMENDED SETUP FOR HYPEROPS

### Tier 1: Essential (FREE, get immediately)
1. **Polygon.io** - Real-time crypto (5 calls/min is plenty for daily routine)
2. **CoinGecko** - Crypto market intelligence (trending coins, market cap)
3. **Alpha Vantage** - Technical indicators (25 calls/day for daily analysis)

### Tier 2: Nice to Have (FREE, add later)
4. **FMP** - News + backup crypto data
5. **FRED** - Macro economic data (if you want Fed policy context)
6. **Biztoc** - News aggregation

### Tier 3: Skip For Now
- Benzinga (trial only, then paid)
- Tiingo (redundant with others)
- Intrinio (requires paid tier for useful data)

---

## 📊 DATA COVERAGE COMPARISON

| Provider | Crypto Prices | News | Macro | Free Limit | Setup Time |
|:---------|:------------:|:----:|:-----:|:-----------|:-----------|
| **YFinance** | ✅ | ❌ | ❌ | Unlimited | 0 min (working) |
| **Polygon.io** | ✅ | ❌ | ❌ | 5/min | 2 min |
| **CoinGecko** | ✅ | ✅ | ❌ | 30/min | 2 min |
| **Alpha Vantage** | ✅ | ❌ | ❌ | 25/day | 1 min |
| **FMP** | ✅ | ✅ | ❌ | 250/day | 2 min |
| **FRED** | ❌ | ❌ | ✅ | Unlimited | 1 min |
| **Biztoc** | ❌ | ✅ | ❌ | Community | 2 min |

---

## 🚀 QUICK START GUIDE

### Step 1: Register for Top 3 APIs (10 minutes total)

```bash
# Polygon.io
1. Go to https://polygon.io/dashboard/signup
2. Get API key
3. Add to OpenBB: obb.account.credentials(polygon_api_key='YOUR_KEY')

# CoinGecko
1. Go to https://www.coingecko.com/en/api/pricing
2. Get free Demo API key
3. Add to OpenBB: obb.account.credentials(coingecko_api_key='YOUR_KEY')

# Alpha Vantage
1. Go to https://www.alphavantage.co/support/#api-key
2. Get free API key
3. Add to OpenBB: obb.account.credentials(alpha_vantage_api_key='YOUR_KEY')
```

### Step 2: Test Integration

```python
from openbb import obb

# Test Polygon (real-time crypto)
btc = obb.crypto.price.historical("BTCUSD", provider="polygon", limit=1)

# Test CoinGecko (trending coins)
trending = obb.crypto.trending()

# Test Alpha Vantage (technical indicators)
rsi = obb.technical.rsi("BTCUSD", provider="alpha_vantage")
```

---

## 💡 INTEGRATION PRIORITY FOR HYPEROPS

**Week 1:** Get Polygon.io setup
- Real-time crypto prices (5/min is plenty)
- Better quality than YFinance
- Use for daily trading brief price snapshots

**Week 2:** Add CoinGecko
- Trending coins detection
- Market cap rankings  
- Catalyst discovery (which coins are moving)

**Week 3:** Add Alpha Vantage (optional)
- Technical indicators (RSI, MACD, etc.)
- Only if you want automated TA in briefs

**Skip:** Everything else unless you need specific features

---

**Total Cost:** $0/month for all recommended providers!
