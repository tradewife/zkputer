# Hyperliquid Trade Execution - Error Handling Guide

## Common Issues & Solutions

### 1. SDK Installation Issues
**Problem:** `ModuleNotFoundError: No module named 'hyperliquid'`
**Solution:** 
```bash
cd /home/kt/Desktop/HyperOPS
python3 -m venv venv
source venv/bin/activate
pip install hyperliquid
```

### 2. Account Initialization Issues
**Problem:** `TypeError: LocalAccount.__init__() got an unexpected keyword argument 'private_key'`
**Solution:** Use `Account.from_key()` instead:
```python
from eth_account import Account
account = Account.from_key(config["secret_key"])
exchange = Exchange(wallet=account, account_address=config["account_address"])
```

### 3. Order Type Issues
**Problem:** `type object 'OrderType' has no attribute 'LIMIT'`
**Solution:** Use `market_open()` method instead of complex limit orders:
```python
result = exchange.market_open(
    name=symbol,
    is_buy=is_buy,
    sz=float(size),
    px=float(price),
    slippage=0.05
)
```

### 4. Order Size Precision Issues
**Problem:** `Order has invalid size.`
**Solution:** Check symbol-specific size requirements:
- XRP: Can use 8.0
- SOL: Use 0.1 instead of 0.086 (precision issues)

### 5. Response Parsing Issues
**Problem:** Incorrect result parsing leading to false failures
**Solution:** Parse the actual response structure:
```python
if result.get("status") == "ok":
    statuses = result.get("response", {}).get("data", {}).get("statuses", [])
    if statuses and "filled" in statuses[0]:
        # Success handling
```

## Standard Execution Pattern

```python
# 1. Initialize
executor = HyperliquidExecutor()
if not executor.initialize():
    print("❌ Initialization failed")
    sys.exit(1)

# 2. Define trades
trades = [
    {"symbol": "XRP", "side": "buy", "size": 8.0, "price": 2.24},
    {"symbol": "SOL", "side": "buy", "size": 0.1, "price": 138.50}
]

# 3. Execute
results = executor.execute_trades(trades)

# 4. Verify
for symbol, result in results.items():
    if result.get("status") == "ok":
        print(f"✅ {symbol}: {result['fill_size']} @ ${result['fill_price']}")
    else:
        print(f"❌ {symbol}: {result.get('error', 'Unknown error')}")
```

## File Structure
- `hyperliquid_executor_production.py` - Main production executor
- `trade_template.py` - Template for custom trades
- `trading_config.json` - Configuration with working parameters

## Virtual Environment
Always use the virtual environment:
```bash
cd /home/kt/Desktop/HyperOPS
source venv/bin/activate
python3 "📊 Core Trading System/hyperliquid_executor_production.py"
```