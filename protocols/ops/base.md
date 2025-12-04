# BaseOPS Protocol

> **Chain:** Base (Coinbase L2)
> **Focus:** Early-stage gem discovery and spot trading
> **Inherits:** `protocols/core/MASTER_PROTOCOL.md`

---

## 1. Overview

BaseOPS is designed for discovering and trading early-stage tokens on Base chain before they gain mainstream attention. It emphasizes fundamental analysis, on-chain verification, and strict filtering to avoid rugs.

**Exchange:** Uniswap V3 (Base), Aerodrome, CDP Trade API

---

## 2. Core Filters (HARD LIMITS)

| Parameter | Limit | Rationale |
|-----------|-------|-----------|
| FDV | < $4,000,000 | Early-stage only |
| Liquidity | > $50,000 | Minimum tradability |
| Age | Any | New launches OK if liq > $50K |

**If a token fails ANY filter, it is REJECTED. No exceptions.**

---

## 3. Scoring System (LT_Score)

Each token is scored 0-5 on five modules:

### 1. Product/Innovation (0-5)
- 0: No product, vaporware
- 1: Concept only, no demo
- 2: Basic MVP, limited functionality
- 3: Working product, some users
- 4: Strong product, growing adoption
- 5: Category leader, clear moat

### 2. Traction (0-5)
- 0: No social presence
- 1: <1K followers, no engagement
- 2: 1-5K followers, minimal engagement
- 3: 5-20K followers, active community
- 4: 20-50K followers, strong engagement
- 5: >50K followers, viral potential

### 3. Tokenomics (0-5)
- 0: No info, suspicious distribution
- 1: High concentration (>50% single wallet)
- 2: Fair launch but unlocks imminent
- 3: Reasonable distribution, known vesting
- 4: Strong distribution, long vesting
- 5: Community-owned, fully unlocked

### 4. Liquidity (0-5)
- 0: <$10K (untradeable)
- 1: $10-25K
- 2: $25-50K
- 3: $50-100K
- 4: $100-500K
- 5: >$500K

### 5. Security (0-5)
- 0: Honeypot, blacklist functions
- 1: Unverified contract, high risk
- 2: Verified but no audit
- 3: Verified, basic audit
- 4: Strong audit, renounced ownership
- 5: Battle-tested, no red flags

**Minimum Threshold:** LT_Score ≥ 15 (average 3/5)

---

## 4. Daily Routine

### Phase 0: Review & Learn (10 min)
1. Review `knowledge_graph/performance_log.md`
2. Update `knowledge_graph/narratives.md` (Base ecosystem themes)
3. Check `knowledge_graph/wallets.md` for smart money activity

### Phase 1: Scan & Filter (20 min)

#### Data Sources
1. **GeckoTerminal** - New pools, volume leaders
2. **DEX Screener** - Price action, liquidity changes
3. **Padre.gg** - Whale accumulation on Base
4. **BaseScan** - Contract verification, holder distribution

#### Scan Criteria
```
Filter 1: FDV < $4M AND Liquidity > $50K
Filter 2: Volume spike (>200% 24h) OR Whale accumulation
Filter 3: Contract verified on BaseScan
Filter 4: No honeypot flags
```

### Phase 2: Deep Dive (30 min)
For each candidate:

1. **Contract Analysis**
   - Verify on BaseScan
   - Check for malicious functions
   - Review holder distribution
   - Identify team/deployer wallets

2. **Social Analysis**
   - X/Twitter presence and engagement
   - Telegram/Discord activity
   - Influencer mentions
   - Sentiment analysis

3. **On-Chain Analysis**
   - Wallet concentration
   - Recent large buys/sells
   - LP lock status
   - Token transfers pattern

4. **Scoring**
   - Apply LT_Score (5 modules)
   - Minimum 15 points to proceed
   - Document rationale for each score

### Phase 3: Position Planning (15 min)

#### Position Types
1. **Foundation Play** (Low Risk)
   - LT_Score ≥ 20
   - Strong fundamentals
   - Size: 5-10% of portfolio
   
2. **Momentum Play** (Medium Risk)
   - LT_Score 15-19
   - Strong catalyst
   - Size: 3-5% of portfolio

3. **Casino Play** (High Risk)
   - LT_Score 12-14 (exception only)
   - Clear rug detection measures
   - Size: 1-2% of portfolio

#### Exit Strategy
- Take Profit 1: 2× (sell 50%)
- Take Profit 2: 5× (sell 30%)
- Moon Bag: Hold 20% for 10×+
- Stop Loss: -30% from entry

### Phase 4: Documentation (10 min)
1. Create token deep dive in `research_logs/`
2. Update `knowledge_graph/tokens.md`
3. Log session to `SESSION_LOG.jsonl`

### Phase 5: Execution (ON COMMAND ONLY)
1. **WAIT** for user approval
2. Execute via CDP Trade API or Uniswap
3. Set price alerts for TPs
4. Log execution details

---

## 5. Privacy Integration

BaseOPS is designed to work with the ZKputer privacy layer:

### Flow
```
User → Zcash (Shielded) → NEAR Intents → Base Chain → Uniswap
```

### Benefits
- No on-chain link between user identity and trades
- Funded with ZEC, traded on Base
- Settlement back to shielded address

### Setup
1. Fund ZKputer Zcash wallet
2. Enable NEAR Intents in `ACTIVE_OPS.json`
3. Execute trades via privacy layer

---

## 6. API Integration

### CDP Trade API
```python
from cdp import CDPClient

client = CDPClient(api_key="...")
tx = client.trade(
    from_token="USDC",
    to_token="0x...",  # Token address
    amount=100,
    slippage=0.5
)
```

### Direct Uniswap (Backup)
```python
from web3 import Web3
from uniswap import Uniswap

uniswap = Uniswap(address, private_key, version=3, provider=base_rpc)
uniswap.make_trade(input_token, output_token, qty)
```

---

## 7. Risk Rules (Base-Specific)

### Position Limits
- Max position size: 10% of portfolio per token
- Max total exposure: 50% of portfolio
- Always keep 50% in stables

### Rug Protection
- Only trade verified contracts
- Check honeypot status before every trade
- Set hard stop at -30%
- Never buy tokens with suspicious tax

### Liquidity Rules
- Don't buy >5% of pool liquidity
- Check for LP lock before buying
- Monitor for liquidity removal

---

## 8. Compliance Checklist

Before every trade:
- [ ] FDV < $4M
- [ ] Liquidity > $50K
- [ ] Contract verified
- [ ] No honeypot flags
- [ ] LT_Score ≥ 15
- [ ] Position size ≤ 10%
- [ ] User explicitly approved
- [ ] Logged to SESSION_LOG.jsonl

---

**Hunt gems. Verify everything. Protect capital.**
