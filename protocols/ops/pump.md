# PumpOPS Protocol

> **Chain:** Solana
> **Focus:** High-speed token sniping (Pump.fun, Raydium, Jupiter)
> **Inherits:** `protocols/core/MASTER_PROTOCOL.md`

---

## 1. Overview

PumpOPS is designed for ultra-fast Solana token sniping, primarily on Pump.fun launches. This is the highest-risk, highest-reward OPS mode requiring strict rug detection and small position sizes.

**Exchanges:** Pump.fun, Jupiter, Raydium

---

## 2. Risk Warning

⚠️ **HIGH RISK MODE**

- Most tokens on Pump.fun are rugs or go to zero
- Only trade with money you can 100% lose
- Small position sizes mandatory
- Speed is critical - use dedicated RPC

---

## 3. Core Filters

| Parameter | Limit | Rationale |
|-----------|-------|-----------|
| Max Position | $100 | Capital preservation |
| Slippage | ≤ 5% | Avoid manipulation |
| Tax | ≤ 10% | Excessive tax = rug |
| Liquidity | > $10K | Minimum tradability |
| Honeypot | PASS | Always check |

---

## 4. Snipe Categories

### 1. Pump.fun Fresh Launch
- Age: < 5 minutes
- Focus: Bonding curve position
- Risk: EXTREME
- Size: $10-25

### 2. Migration Snipe
- Token migrating from Pump.fun to Raydium
- Liquidity being added
- Risk: HIGH
- Size: $25-50

### 3. Volume Breakout
- Established token with sudden volume
- Whale accumulation detected
- Risk: MEDIUM
- Size: $50-100

### 4. Narrative Play
- Token tied to trending narrative
- Strong social momentum
- Risk: MEDIUM
- Size: $50-100

---

## 5. Rug Detection Checklist

Before EVERY trade, verify:

### Contract Checks
- [ ] Mint authority disabled
- [ ] Freeze authority disabled
- [ ] No blacklist function
- [ ] No hidden fees
- [ ] LP burned or locked

### Social Checks
- [ ] Real X/Twitter account (not just created)
- [ ] Telegram exists and active
- [ ] Dev wallet not dumping
- [ ] No copy-paste project

### On-Chain Checks
- [ ] Holder distribution reasonable
- [ ] No single wallet >20% (except LP)
- [ ] No suspicious transfer patterns
- [ ] Liquidity sufficient for exit

---

## 6. Daily Routine

### Phase 0: Setup (5 min)
1. Check SOL balance
2. Verify RPC connection (low latency crucial)
3. Review `knowledge_graph/performance_log.md`
4. Update target socials list

### Phase 1: Narrative Scan (15 min)
1. **X/Twitter Scan**
   - Trending crypto topics
   - Influencer mentions
   - Meme trends
   
2. **Pump.fun Monitor**
   - New launches
   - Bonding curve progress
   - Migration candidates

3. **Whale Wallet Watch**
   - Track wallets from `knowledge_graph/wallets.md`
   - Note fresh accumulation

### Phase 2: Target Identification (Continuous)
For each candidate:

1. **Quick Rug Check** (30 seconds)
   - Contract authority status
   - Holder distribution
   - Liquidity level

2. **Social Verification** (1 minute)
   - X account legitimacy
   - Community activity
   - Dev responsiveness

3. **Entry Decision**
   - If PASS all checks → Add to watchlist
   - If user approves → Prepare snipe

### Phase 3: Execution (ON COMMAND)
1. **Pre-flight Check**
   - Confirm slippage settings
   - Verify gas (priority fee)
   - Double-check token address

2. **Execute**
   - Use Jupiter or Pump.fun UI
   - Set priority fee for speed
   - Immediate stop-loss setup

3. **Post-Trade**
   - Verify token received
   - Set price alerts
   - Log to SESSION_LOG.jsonl

---

## 7. Exit Strategy

### Take Profit Levels
- TP1: 2× (sell 50%) - Recover capital
- TP2: 5× (sell 30%) - Lock profit
- Moon Bag: 20% - Let it ride

### Stop Loss
- Hard stop: -50% from entry
- Time stop: Sell if no movement in 24h
- Rug detection: Sell immediately if red flags appear

### Trailing Strategy
- After 3×, trail with 30% drawdown tolerance
- Lock in profit progressively

---

## 8. API Integration

### Jupiter Swap
```python
import httpx

async def swap_jupiter(input_mint, output_mint, amount, slippage=50):
    quote_url = f"https://quote-api.jup.ag/v6/quote"
    params = {
        "inputMint": input_mint,
        "outputMint": output_mint,
        "amount": amount,
        "slippageBps": slippage
    }
    async with httpx.AsyncClient() as client:
        quote = await client.get(quote_url, params=params)
        # Execute swap with quote
```

### Pump.fun (Browser/API)
- Use browser automation for bonding curve buys
- Monitor graduation events
- Track migration transactions

---

## 9. Privacy Integration

PumpOPS supports ZKputer privacy layer:

### Flow
```
User → Zcash (Shielded) → NEAR Intents → Solana → Jupiter
```

### Benefits
- Trade memecoins without wallet exposure
- No link to main identity
- Separate from portfolio wallets

---

## 10. Target Socials

Maintain in `target_socials.md`:

### Influencers to Monitor
- @example1 (calls memecoins)
- @example2 (Pump.fun specialist)

### Alpha Groups
- Telegram groups
- Discord servers

### Whale Wallets
- High-conviction sniper wallets
- Smart money accumulators

---

## 11. Compliance Checklist

Before every snipe:
- [ ] Position ≤ $100
- [ ] Slippage ≤ 5%
- [ ] Rug checks PASSED
- [ ] Exit strategy defined
- [ ] User explicitly approved
- [ ] Logged to SESSION_LOG.jsonl

---

**Speed is key. Verify everything. Size small. Exit fast.**
