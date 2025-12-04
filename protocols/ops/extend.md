# ExtendOPS Protocol

> **Exchange:** Extended Exchange (https://app.extended.exchange)
> **Focus:** USDC-margined perpetual futures trading
> **Inherits:** `protocols/core/MASTER_PROTOCOL.md`

---

## 1. Overview

ExtendOPS is a thesis-driven perpetual trading system optimized for Extended Exchange. It leverages whale intelligence from Hyperliquid ecosystem platforms, real-time funding analysis, and strict risk management.

**Symbol Format:** `BTC-USD`, `ETH-USD`, `SOL-USD`, etc.

---

## 2. Account Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Default Equity | $100 | Adjust in ACTIVE_OPS.json |
| Max Risk/Trade | 20% | $20 on $100 account |
| Leverage Range | 9-12× | Verify notional ≤ $1200 |
| Max Positions | 2 | 40% total exposure |
| Entry Preference | Limit | Market allowed for urgency |

---

## 3. Daily Routine

### Phase 0: Preparation (10 min)
1. **Review Performance**
   - Open `knowledge_graph/performance_log.md`
   - Analyze yesterday's trades
   - Note patterns and mistakes

2. **Market Regime**
   - Update `knowledge_graph/narratives.md`
   - Identify: Risk-On / Risk-Off / Neutral
   - Check scheduled catalysts (FOMC, CPI, unlocks)

3. **Smart Money Check**
   - Review `knowledge_graph/smart_money.md`
   - Note elite trader positioning changes
   - Identify wallets to follow

### Phase 1: Market Scan (20 min)
1. **Universe Definition**
   - Core: BTC-USD, ETH-USD, SOL-USD
   - Add: Top 5 by volume/OI from Extended API
   
2. **Filter Criteria**
   - Volume ≥ $500K (24h)
   - Open Interest ≥ $1M
   - Orderbook Depth ≥ $50K within 0.5%

3. **Funding & OI Analysis**
   - Current funding rates (flag if >±0.1%)
   - OI changes (24h, 1h deltas)
   - Funding/OI divergences

4. **Whale Intelligence (USE BROWSER)**
   - Dextrabot: Large prints >$50K
   - ApexLiquid: Top PnL trader positions
   - SuperX: Trader screener insights

### Phase 2: Setup Identification (25 min)

#### Setup Types

**1. Funding Arbitrage**
- Signal: Funding >0.1% (short) or <-0.1% (long)
- Entry: Limit at VWAP/LVN on pullback
- Exit: Funding normalization + 1.5× risk

**2. Momentum Catalyst**
- Signal: News/upgrade with volume confirmation
- Entry: Breakout on momentum
- Exit: Catalyst completion or 2.5× risk

**3. Liquidity Hunt**
- Signal: Thin orderbook + liquidation cluster
- Entry: Fade to liquidity magnet
- Exit: Liquidation cascade + 2× risk

**4. Mean Reversion**
- Signal: Extreme deviation from VWAP + stretched funding
- Entry: Limit at extreme with OI divergence
- Exit: Return to VWAP + 1.5× risk

**5. Smart Money Follow**
- Signal: Verified smart money accumulation
- Entry: Follow their execution style
- Exit: Their exit signal + 2× risk

#### Analysis Checklist
- [ ] Technical levels (VWAP, HVN/LVN)
- [ ] Orderbook analysis (depth, stops, magnets)
- [ ] Catalyst confirmation (3+ sources)
- [ ] R:R calculation (min 1.5:1)
- [ ] Smart money alignment

### Phase 3: Trade Planning (15 min)
1. **Specify Entry**
   - Precise price range
   - Anchor level (LVN/VWAP/liquidity)
   - Order type: Limit (prefer) or Market

2. **Size Calculation**
   ```
   RiskUSD = $100 × 0.20 = $20
   StopDistance = (Entry - Stop) / Entry
   Quantity = RiskUSD / (Entry × StopDistance)
   Notional = Quantity × Entry
   Leverage = Notional / $100
   ```

3. **Exit Planning**
   - Stop: Technical level + 0.2% buffer
   - TP1: 1.5-2× risk (take 50%)
   - TP2: 3-4× risk (remainder)

### Phase 4: Documentation (10 min)
1. Create `docs/research_logs/{YYYY-MM-DD}/daily_trading_brief.md`
2. Update knowledge graph files
3. Log session to `SESSION_LOG.jsonl`

### Phase 5: Execution (ON COMMAND ONLY)
1. **WAIT** for user approval
2. Execute via Extended API
3. Verify order placement
4. Log execution details

---

## 4. API Integration

### Configuration
```json
// ExtendOPS/config/trading_config.json
{
  "account_address": "0x...",
  "api_key": "...",
  "stark_public_key": "...",
  "stark_private_key": "...",
  "vault_number": 0,
  "testnet": false,
  "legacy_signing": false
}
```

### Executor Usage
```python
from ExtendOPS.core.executor import ExtendedExecutor

executor = ExtendedExecutor()
await executor.initialize()
await executor.place_order(
    symbol="SOL-USD",
    side="buy",
    size=0.5,
    price=240.0
)
```

---

## 5. Whale Intel Sources

| Platform | URL | Data |
|----------|-----|------|
| Dextrabot | app.dextrabot.com/hyperliquid-whale-trades | Large prints, wallet labels |
| ApexLiquid | apexliquid.bot | Top PnL traders, positions |
| SuperX | trysuper.co | Trader screener, vaults |

**CRITICAL:** Use BROWSER for these platforms. API not available.

---

## 6. Risk Rules (Extended-Specific)

### Order Types
- **Entry:** Limit preferred, Market for high-urgency catalysts
- **Stop Loss:** STOP or STOP_LIMIT only (NEVER regular Limit)
- **Take Profit:** Limit orders

### Position Management
- Check for existing positions before new entries
- Stale orders: Cancel after 90 minutes
- MAE Cut: If >60% of stop hit in 3 min, close immediately

### Correlation Limits
- Max 1 position per correlated pair (e.g., BTC+ETH = correlated)
- Total exposure: 40% of equity maximum

---

## 7. Output Format

### Daily Trading Brief
```markdown
# Daily Trading Brief - {DATE}

## Market Snapshot
- Timestamp: {AEST}
- Regime: {Risk-On/Risk-Off/Neutral}
- Key Themes: {catalysts}

## Evidence Tables
| Symbol | Funding | OI Δ24h | Volume | Thesis |
|--------|---------|---------|--------|--------|

## Whale Intel Digest
- Large prints: ...
- Smart money bias: ...

## Top 3 Setups
### Setup 1: {Symbol} {Side}
- Entry: $X
- Stop: $Y
- TP1/TP2: $A / $B
- Thesis: ...
- Sources: [...]

## Final Trades (Awaiting Approval)
| Symbol | Side | Entry | Stop | Size | Risk | Leverage |
|--------|------|-------|------|------|------|----------|
```

---

## 8. Compliance Checklist

Before every trade:
- [ ] Risk ≤ 20% ($20 on $100)
- [ ] Leverage ≤ 12×
- [ ] Stop loss set (STOP order type)
- [ ] 3+ source confirmation
- [ ] No conflicting positions
- [ ] User explicitly approved
- [ ] Logged to SESSION_LOG.jsonl

---

**Execute with precision. Trade with thesis. Manage risk relentlessly.**
