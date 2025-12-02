# 📊 Core Trading System - Critical Implementation Notes

## ⚠️ STOP LOSS ORDER TYPE - CRITICAL BUG

**Date Identified:** 2025-11-30
**Severity:** CRITICAL - Can cause immediate position closure instead of protection

### The Problem

The current `trading_module.py` implementation uses **LIMIT orders** for stop losses, which is fundamentally incorrect.

**What happens:**
```python
# WRONG - This is what the current code does:
OrderSpec(
    symbol="ETH-USD",
    side="buy",          # Close short position
    order_type="limit",  # ❌ WRONG ORDER TYPE
    size=0.02,
    price=3050.00,       # Stop loss level
    reduce_only=True
)
```

**Why it's wrong:**
- ETH short position @ $2980, want stop loss @ $3050
- Limit BUY @ $3050 when price is $2980 means "buy at $3050 or BETTER"
- Since current price ($2980) is better than $3050, order **executes IMMEDIATELY**
- Position is closed at market price instead of being protected at $3050

### The Solution

**Use STOP or STOP_LIMIT order types:**
```python
# CORRECT - What should be implemented:
# Option 1: Stop Market Order
OrderSpec(
    symbol="ETH-USD",
    side="buy",
    order_type="stop",      # ✅ Correct - only triggers at $3050
    size=0.02,
    trigger_price=3050.00,  # Price that triggers the order
    reduce_only=True
)

# Option 2: Stop Limit Order
OrderSpec(
    symbol="ETH-USD",
    side="buy",
    order_type="stop_limit",    # ✅ Correct - triggers at stop, executes at limit
    size=0.02,
    trigger_price=3050.00,      # Trigger price
    limit_price=3055.00,        # Execution price (allows slippage control)
    reduce_only=True
)
```

### Extended SDK Implementation

Check the Extended/X10 Python SDK documentation for:
1. Available order types (likely `OrderType.STOP` or similar)
2. Proper parameter names (`trigger_price` vs `stop_price` vs `price`)
3. Stop order examples in SDK documentation

### Files Requiring Updates

1. **`trading_module.py`**
   - Line ~255-276: `place_order()` method
   - Add support for stop order types
   - Update `OrderSpec` dataclass to include trigger price

2. **`place_stops_tps.py`** and related scripts
   - Update all stop loss placement scripts
   - Use correct order type

### Temporary Workaround

**DO NOT place automated stop losses** until this is fixed. Instead:
- Monitor positions manually
- Use exchange UI to place stop orders
- Or implement manual stop checks and close positions when hit

### Testing Required

Before using in production:
1. Test stop order placement on testnet
2. Verify order only triggers at specified price
3. Test both long and short stop losses
4. Verify reduce-only flag works correctly

---

## Order Type Reference

### LIMIT Orders
- Execute at specified price **or better**
- Buy limit @ $100 when price is $95 = executes immediately at $95
- Use for: Entries, take profits in direction of current price movement

### STOP Orders
- Only trigger when price **reaches** specified level
- Stop-buy triggers when price goes UP to stop level
- Stop-sell triggers when price goes DOWN to stop level
- Use for: Stop losses, breakout entries

### When to Use Each

| Scenario | Current Price | Target | Order Type |
|----------|--------------|--------|------------|
| Long entry | $100 | Buy @ $95 | LIMIT (buy at $95 or lower) |
| Long stop loss | $100 | Sell @ $90 | STOP (sell when drops to $90) |
| Long take profit | $100 | Sell @ $110 | LIMIT (sell at $110 or higher) |
| Short entry | $100 | Sell @ $105 | LIMIT (sell at $105 or higher) |
| Short stop loss | $100 | Buy @ $110 | STOP (buy when rises to $110) |
| Short take profit | $100 | Buy @ $90 | LIMIT (buy at $90 or lower) |

---

**Last Updated:** 2025-11-30  
**Status:** 🔴 CRITICAL BUG - DO NOT USE AUTOMATED STOPS UNTIL FIXED
