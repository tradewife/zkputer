# Daily Trading Brief — December 1, 2025 (Final - ATR Protocol Enforced)

## 1. Market Snapshot
**Timestamp:** 11:43 AEST  
**Account**: $84.10 (Clean slate after SOL +$13, AVAX -$6)  
**Key Shift:** BTC dropped to $87.9k (-$3.7k from earlier), ETH at $2,872 (-$172)  
**Market Regime:** Risk-off correction underway  
**Provenance:** Hyperliquid API, Dextrabot Whale Intel

## 2. Evidence Tables

### Whale Intelligence (Dextrabot)
| Asset | Total Notional | Long/Short Bias | Signal |
|-------|----------------|-----------------|--------|
| **ASTER** | $74.9M | 55.33% Long | **Strong whale accumulation** |
| HYPE | $751.8M | 50.11% Short | Neutral (balanced) |
| PUMP | $75.5M | 51.33% Short | Weak bear bias |

### Market Data (24h)
| Symbol | Price | Volume | OI | Funding | ATR (est) |
|--------|-------|--------|----|---------|-----------| 
| BTC | $87,882 | $450M | $22.8M | +0.0013% | ~$800 |
| ETH | $2,872 | $128.7M | $10.5M | +0.0013% | ~$80 |
| **HYPE** | $30.93 | $94.7M | $4.77M | +0.0013% | ~$1.20 |
| SOL | $129.05 | $35.7M | $4.15M | -0.0024% | ~$3.50 |

### Key Observations
- **BTC/ETH correction:** Major down over -4% and -5.6% respectively
- **HYPE surging:** New mover with massive $94.7M volume (3rd place)
- **ASTER whale signal:** Clear 55% long bias on $74.9M notional
- **Funding neutral:** No extreme positioning edges

## 3. Setup Analysis

### Setup 1: HYPE-USD Long (Volume Leader) ⭐ HIGHEST CONVICTION

**Thesis:** HYPE is the dark horse - #3 by volume ($94.7M), but barely on radar. Fresh mover with institutional interest landing.

**Technical:**
- Price: $30.93
- Recent range: $28-32
- Support: $30.00 (psychological)
- Resistance: $32.50

**ATR Analysis (MANDATORY):**
- 24h ATR (estimated from range): ~$1.20
- Min stop distance: max(0.8 × $1.20, $0.80) = **$0.96**
- Technical stop: $30.00 (support)
- **Selected stop: $29.90** ($1.03 away - exceeds minimum ✅)

**Risk/Reward:**
- Entry: $31.00 (limit)
- Stop: $29.90
- TP1: $32.50 (50%)
- TP2: $34.00 (50%)
- Size: 3.0 HYPE (~$93 notional @ 10x = $9.30 margin)
- Risk: $3.30
- Profit: $4.50 (TP1) / $9.00 (TP2)
- R:R: 1.4:1 to 2.7:1

**Whale Intel:** Balanced positioning (50/50) = not crowded either way

---

### Setup 2: ASTER-USD Long (Whale Follow) 

**Thesis:** Following clear whale accumulation (55.33% long bias on $74.9M).

**Issue:** No ASTER data in Hyperliquid API feed - **cannot calculate precise ATR**.

**Status:** SKIP - Cannot comply with ATR protocol without market data.

---

### Setup 3: BTC-USD Mean Reversion Short

**Thesis:** BTC dropped -4.2% to $87.9k. Potential dead cat bounce to short.

**ATR Analysis:**
- 24h ATR: ~$800
- Min stop distance: max(0.8 × $800, $250) = **$640**
- Entry: $88,000
- Stop: $88,700 ($700 away - exceeds minimum ✅)
- TP: $86,500
- Size: 0.001 BTC (~$88 notional / 10x = $8.80 margin)
- Risk: $0.70
- Profit: $1.50
- R:R: 2.1:1

**Concerns:** Catching falling knife, no clear support until $85k

---

## 4. Final Recommendation

### PRIMARY TRADE: HYPE-USD LONG

**Entry:** $31.00 (Limit)  
**Stop:** $29.90 (below support + ATR compliance)  
**TP1:** $32.50 (50% size)  
**TP2:** $34.00 (50% size)  
**Size:** 3.0 HYPE  
**Margin:** ~$9.30 (10x leverage)  
**Risk:** $3.30 (3.9% account)  
**Profit Potential:** $4.50-$9.00  

**ATR Compliance:** ✅  
- ATR: $1.20
- Min distance: $0.96
- Actual: $1.03  
- Exceeds minimum by 7%

**Why HYPE:**
1. Massive volume (#3 spot, $94.7M) but flying under radarpulled
2. Fresh mover (not overtraded like SOL/AVAX)
3. Proper ATR-based stop
4. Decent R:R (1.4-2.7:1)
5. Not crowded (50/50 whale positioning)

**Alternative:** BTC Short @ $88k if you prefer majors

## 5. Risk Factors
- HYPE is newer/less liquid than BTC/ETH
- If BTC continues dumping, could drag HYPE down
- No historical support data for HYPE (newer asset)

## 6. Execution Plan
1. Place HYPE long limit @ $31.00
2. **DO NOT SET automated TP/SL** (SDK issues)
3. After fill, manually place:
   - Stop sell limit @ $29.85 (below $29.90 trigger)
   - TP sell limit @ $32.50 (TP1)
4. Monitor for fill, adjust TP2 manually

## 7. Citations
- Dextrabot whale data (ASTER 55% long bias)
- Hyperliquid API (HYPE $94.7M volume)
- STOP_LOSS_PROTOCOL.md (ATR calculations)
