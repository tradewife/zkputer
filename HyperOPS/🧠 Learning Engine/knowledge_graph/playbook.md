# Trading Playbook

## Active Setups
1. **Funding Arbitrage**
   - Status: Active
   - Win Rate: N/A

2. **Momentum Catalyst**
   - Status: Active
   - Win Rate: N/A

3. **Liquidity Hunt**
   - Status: Active
   - Win Rate: N/A

4. **Mean Reversion**
   - Status: Active
   - Win Rate: N/A

5. **Smart Money Follow**
   - Status: Active
   - Win Rate: 0/1 (ETH short stopped out prematurely)
   - Current Plays: ETH Short (Leviathan), ZEC Long (Whale)

## Critical Lessons Learned

### 2025-12-01: Stop Loss Placement - ATR/Volatility Check Mandatory
**Trade:** AVAX-USD Long (30 units)
**Error:** Set stop loss at $13.15 when entry was $13.31 (only 16 cents / 1.2% away)
**Impact:** Immediately stopped out for -$5.90 loss due to normal volatility
**Root Cause:**
- No ATR (Average True Range) check before setting stop
- Used arbitrary tight percentage instead of technical support level
- Mid-cap altcoins need wider stops than majors

**Correct Process (MANDATORY):**
1. **Check 24h ATR** before ANY stop placement
2. **Minimum stop distance:** 0.8x ATR (for trending) or 1.2x ATR (for ranging)
3. **Use structural levels:** Support/resistance, not arbitrary prices
4. **Asset-specific rules:**
   - BTC/ETH: Minimum $200-300 stop distance
   - SOL: Minimum $2-3 stop distance  
   - Mid-caps (AVAX/ADA): Minimum $0.40-0.60 stop distance
   - Low-cap: Minimum 3-5% stop distance

**Example (AVAX):**
```python
# ❌ WRONG (what I did):
stop_price = entry - 0.16  # Way too tight!

# ✅ CORRECT:
atr_24h = 0.45  # Check actual ATR
stop_distance = max(atr_24h * 0.8, 0.40)  # At least $0.40
support_level = 13.00  # Technical level
stop_price = min(entry - stop_distance, support_level)
# Result: $13.00 stop (proper breathing room)
```

**Action Taken:**
- Documented in performance_log.md
- Updated playbook.md (this section)
- **NEW RULE:** All future trades MUST show ATR calculation in brief

**Enforcement:** Any trade recommendation without ATR-based stop will be rejected.

---

### 2025-11-30: Stop Loss Order Type Error
**Trade:** ETH-USD Short
**Error:** Used LIMIT order type for stop loss instead of STOP or STOP_LIMIT
**Impact:** Position closed immediately upon entry instead of providing protection
**Root Cause:** 
- `trading_module.py` incorrectly configured with `OrderTpslType.ORDER` using `LIMIT` price type
- Should use `OrderType.STOP` or `OrderType.STOP_LIMIT` with proper trigger parameters

**Correct Implementation:**
```python
# WRONG (old code):
stop_order = OrderSpec(
    order_type="limit",  # ❌ WRONG
    price=stop_price
)

# CORRECT (new code):
stop_order = OrderSpec(
    order_type="stop_loss",  # ✅ CORRECT
    stop_loss_price=trigger_price
)
```

**Rule:** NEVER use limit orders for stop losses. Always use STOP or STOP_LIMIT order types.

**Impact:** Position closed immediately at market price instead of being protected at $3050

## Order Type Reference (Extended Exchange)

### LIMIT Orders
- Execute at specified price or BETTER
- Buy limit @ $100 when price is $105 = waits for $100 or lower
- Buy limit @ $100 when price is $95 = executes immediately at $95

### STOP Orders (Required for protective stops)
- Only trigger when price REACHES specified level
- Stop-loss for shorts: Triggers when price goes UP to stop level
- Stop-loss for longs: Triggers when price goes DOWN to stop level
