# ZKputer Execution Hooks

Hooks that run before and after every trade execution. **These are mandatory.**

## Hook Chain

```
[Trade Request] 
    → pre_trade.py (VALIDATE)
    → [EXECUTE on Exchange]
    → post_trade.py (LOG)
    → [Audit Trail]
```

## Hooks

### `pre_trade.py` - Pre-Trade Validation

**Runs before every trade.** Validates:
- Exchange config exists and is MAINNET
- Position size within limits ($100 max)
- Leverage within limits (12x max)
- Stop loss is present (REQUIRED)
- Position count per exchange (2 max)

**Usage:**
```python
from .zkputer.hooks.pre_trade import run_pre_trade_hook

trades = [{"exchange": "extended", "symbol": "BTC-USD", ...}]
if run_pre_trade_hook(trades):
    # Execute trades
else:
    # Abort - validation failed
```

### `post_trade.py` - Post-Trade Logging

**Runs after every trade.** Logs:
- Trade details and result to audit trail
- Session summary with success/failure counts
- Append-only JSONL format in `logs/trade_audit.jsonl`

**Usage:**
```python
from .zkputer.hooks.post_trade import run_post_trade_hook

run_post_trade_hook(trades, results)
```

## Risk Limits (ADVISORY)

**Human has final say on all trades.** These are protocol recommendations, not blocks:

| Limit | Protocol Value | Enforcement |
|-------|----------------|-------------|
| Max Leverage | 12x (position = margin * leverage) | Advisory |
| Max Positions/Exchange | 2 | Advisory |
| Stop Loss | Recommended | Advisory |

The hook displays warnings for protocol deviations. Human reviews and decides.

## Audit Trail

All trades logged to `logs/trade_audit.jsonl`:
```jsonl
{"timestamp": "2025-12-04T10:30:00", "trade": {...}, "result": {...}, "success": true}
{"timestamp": "2025-12-04T10:30:01", "type": "session_summary", "total_trades": 2, "successes": 2}
```
