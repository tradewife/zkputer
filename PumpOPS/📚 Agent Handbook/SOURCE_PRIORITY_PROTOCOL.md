# 🎯 Source Priority Protocol (Solana)

## Purpose
This protocol defines the hierarchy of data sources to ensure accurate research and prevent automation failures.

---

## Data Source Hierarchy

### Tier 1: Primary Sources (MUST USE FIRST)

#### 1. Padre.gg (https://trade.padre.gg/trenches)
**Use For:**
- Trench radar (New pairs)
- Volume and liquidity metrics
- Chart analysis
- "Kill Zone" filtering

**Quality Standard:**
- ✅ Real-time data (<30s lag)
- ✅ Direct from RPC
- ✅ Cross-referenced with Pump.Fun

#### 2. Pump.Fun (https://pump.fun/)
**Use For:**
- Bonding Curve status (90%+)
- King of the Hill verification
- Dev profile check

**Quality Standard:**
- ✅ Direct platform data
- ✅ Bonding curve accurate

#### 3. RugCheck.xyz (https://rugcheck.xyz/)
**Use For:**
- Security analysis (Mint Auth, Freeze Auth)
- Holder distribution risk
- LP Lock verification

---

### Tier 2: Confirmation Sources (REQUIRED FOR DEEP DIVE)

#### 4. Solscan (https://solscan.io/)
**Use For:**
- Contract verification
- Dev wallet history (dumps?)
- Holder cluster analysis

#### 5. GMGN.ai (https://gmgn.ai/)
**Use For:**
- Smart Money tracking
- Insider wallet detection
- "Blue Chip" holder verification

#### 6. Twitter / X
**Use For:**
- Sentiment analysis
- Dev activity check
- "Cabal" verification (KOL clusters)

---

### Tier 3: Fallback Sources (ONLY IF TIER 1-2 UNAVAILABLE)

#### 7. DexScreener
**Use For:**
- Alternative charting
- Multi-DEX liquidity check (Raydium vs Orca)

#### 8. Web Search
**Use For:**
- Project background
- Team doxxing (rare)

---

## Automation Failure Protocol

### When Browser Automation Fails

**IMMEDIATE RESPONSE:**

1. **STOP Complex Automation**
   - Do not persist with failing tool calls.

2. **SWITCH to Screenshot Mode**
   - Capture Padre.gg / Pump.Fun tables.

3. **PERFORM Manual Analysis**
   - Extract tickers and metrics visually.

4. **DOCUMENT Failure**
   - Log in `failure_logs/`.

---

## Source Verification Checklist

### For Every Claim, Document:
- [ ] **Source Name** (Padre, Pump, Solscan)
- [ ] **Timestamp**
- [ ] **Confidence** (High/Med/Low)

### When Sources Conflict:
1. **Prefer Tier 1** (Padre/Pump)
2. **Use conservative value**
3. **Document discrepancy**

---

**Follow the hierarchy. Verify independently. Document thoroughly.**
