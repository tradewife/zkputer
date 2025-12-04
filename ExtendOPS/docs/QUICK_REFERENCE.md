# ExtendOPS Quick Reference

## Trading Execution Scripts

### Check Account Status
```bash
python3 account_manager.py
```
Shows: Equity, positions, PnL, open orders

### Get Market Data
```bash
python3 market_data.py
```
Shows: Prices, funding, volume, OI for key markets

### Execute Trades (Python)
```python
from extended_executor import ExtendedExecutor

executor = ExtendedExecutor()
await executor.initialize()

# Place order
await executor.place_order(
    market="BTC-USD",
    side="buy",
    size=0.01,
    price=92000,
    leverage=20
)

# Place stop/TP
await executor.place_stop_tp_orders(
    market="BTC-USD",
    position_side="long",
    size=0.01,
    stop_price=90000,
    tp1_price=94000,
    tp2_price=96000
)

# Close position
await executor.close_position("BTC-USD")

# Cancel all orders
await executor.cancel_all_orders()
```

## Key Changes from HyperOPS
- ✅ Folder renamed: `HyperOPS` → `ExtendOPS`
- ✅ Consolidated to 3 core scripts (extended_executor.py, market_data.py, account_manager.py)
- ✅ Removed all Hyperliquid execution code
- ✅ Kept Hyperliquid whale intel (browser-based)
- ✅ All trading executes on Extended Exchange

## Daily Routine
1. Run `account_manager.py` - check status
2. Run `market_data.py` - scan markets
3. Browser → Dextrabot/ApexLiquid - whale intel
4. Identify setups
5. Use `extended_executor.py` to place trades

## Configuration
Located: `⚙️ Configuration/config/trading_config.json`
- Extended vault credentials
- Leverage limits (9-20x)
- Risk parameters
