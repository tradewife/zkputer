# API Execution Playbook

**MANDATORY READING before any trade execution.**

This document provides crystal-clear instructions for executing trades on all supported exchanges. Any AI pair-programmer opening ZKputer must follow these protocols exactly.

---

## Pre-Flight Checklist

Before ANY trade:

```bash
# 1. Verify all exchange configs
python -c "from src.core.exchanges import verify_all_configs; verify_all_configs()"

# 2. Run pre-trade validation
python .zkputer/hooks/pre_trade.py
```

**If either fails, DO NOT PROCEED.**

---

## Exchange Reference

### Extended Exchange

**SDK:** `x10-python-trading-starknet`  
**Config:** `config/exchanges/extended.json`  
**Network:** Mainnet (testnet=false)

#### Authentication
```python
from x10.perpetual.accounts import StarkPerpetualAccount
from x10.perpetual.trading_client import PerpetualTradingClient
from x10.perpetual.configuration import MAINNET_CONFIG

stark_account = StarkPerpetualAccount(
    vault=config["vault_number"],        # 232387
    private_key=config["stark_private_key"],
    public_key=config["stark_public_key"],
    api_key=config["api_key"],
)

trading_client = PerpetualTradingClient(MAINNET_CONFIG, stark_account)
```

#### Place Order
```python
from src.core.exchanges.extended_client import ExtendedClient, ExtendedOrder

client = ExtendedClient()
await client.connect()

order = ExtendedOrder(
    symbol="BTC-USD",
    side="buy",
    size=0.001,
    price=95000.0,
    stop_loss=93000.0,    # REQUIRED
    take_profit=100000.0  # Optional
)

result = await client.place_order(order)
await client.disconnect()
```

#### Symbol Format
- Use market name: `BTC-USD`, `ETH-USD`, `SOL-USD`

---

### Hyperliquid

**SDK:** `hyperliquid-python-sdk`  
**Config:** `config/exchanges/hyperliquid.json`  
**Network:** Mainnet (testnet=false)

#### Authentication
```python
from hyperliquid.exchange import Exchange
from eth_account import Account

account = Account.from_key(config["secret_key"])
exchange = Exchange(
    wallet=account,
    account_address=config["account_address"],
)
```

#### Place Order (Market)
```python
from src.core.exchanges.hyperliquid_client import HyperliquidClient, HyperliquidOrder

client = HyperliquidClient()
client.connect()

order = HyperliquidOrder(
    symbol="BTC",
    side="buy",
    size=0.001,
    price=95000.0,
    slippage=0.05
)

result = client.place_order(order)  # Uses market_open for reliable fill
```

#### Symbol Format
- Use coin ticker only: `BTC`, `ETH`, `SOL`, `XRP`, `AVAX`
- NOT `BTC-USD` or `BTC-PERP`

---

### Base (Coinbase CDP)

**SDK:** `cdp-sdk`  
**Config:** `config/exchanges/base.env`  
**Network:** base-mainnet

#### Authentication
```python
from cdp import Cdp, Wallet

Cdp.configure(
    api_key_name=f"organizations/default/apiKeys/{config['api_key_id']}",
    private_key=config['api_key_secret']
)
```

#### Swap
```python
from src.core.exchanges.base_client import BaseClient, BaseSwap

client = BaseClient()
client.connect()

# Create or import wallet first
client.create_wallet()  # or client.import_wallet(wallet_data)

swap = BaseSwap(
    from_asset="eth",
    to_asset="usdc",
    amount=0.01
)

result = client.swap(swap)
```

#### Asset IDs
- `eth` - Native ETH
- `usdc` - USDC stablecoin
- Contract addresses for other tokens

---

## Unified Execution Flow

```python
import asyncio
from .zkputer.hooks.pre_trade import run_pre_trade_hook
from .zkputer.hooks.post_trade import run_post_trade_hook
from src.core.exchanges.extended_client import ExtendedClient, ExtendedOrder
from src.core.exchanges.hyperliquid_client import HyperliquidClient, HyperliquidOrder

async def execute_session(trades: list):
    """Execute a trading session with full validation and logging"""
    
    # 1. PRE-TRADE VALIDATION (MANDATORY)
    if not run_pre_trade_hook(trades):
        print("ABORTED: Pre-trade validation failed")
        return []
    
    results = []
    
    # 2. EXECUTE TRADES
    for trade in trades:
        exchange = trade["exchange"].lower()
        
        if exchange == "extended":
            result = await execute_extended(trade)
        elif exchange == "hyperliquid":
            result = execute_hyperliquid(trade)
        elif exchange == "base":
            result = execute_base(trade)
        else:
            result = {"status": "error", "error": f"Unknown exchange: {exchange}"}
        
        results.append(result)
    
    # 3. POST-TRADE LOGGING (MANDATORY)
    run_post_trade_hook(trades, results)
    
    return results


async def execute_extended(trade: dict):
    client = ExtendedClient()
    if not await client.connect():
        return {"status": "error", "error": "Connection failed"}
    
    order = ExtendedOrder(
        symbol=trade["symbol"],
        side=trade["side"],
        size=trade["size"],
        price=trade.get("price"),
        stop_loss=trade.get("stop_loss"),
        take_profit=trade.get("take_profit")
    )
    
    result = await client.place_order(order)
    await client.disconnect()
    return result


def execute_hyperliquid(trade: dict):
    client = HyperliquidClient()
    if not client.connect():
        return {"status": "error", "error": "Connection failed"}
    
    order = HyperliquidOrder(
        symbol=trade["symbol"],
        side=trade["side"],
        size=trade["size"],
        price=trade["price"],
    )
    
    return client.place_order(order)


def execute_base(trade: dict):
    from src.core.exchanges.base_client import BaseClient, BaseSwap
    
    client = BaseClient()
    if not client.connect():
        return {"status": "error", "error": "Connection failed"}
    
    swap = BaseSwap(
        from_asset=trade.get("from_asset", "eth"),
        to_asset=trade.get("to_asset", "usdc"),
        amount=trade["size"]
    )
    
    return client.swap(swap)
```

---

## Risk Enforcement

| Rule | Limit | Enforced By |
|------|-------|-------------|
| Max Position | $100 | pre_trade.py |
| Max Leverage | 12x | pre_trade.py |
| Max Positions/Exchange | 2 | pre_trade.py |
| Stop Loss Required | YES | pre_trade.py |
| Mainnet Only | YES | config loaders |

---

## Troubleshooting

### "Config not found"
```bash
ls config/exchanges/
# Should show: extended.json, hyperliquid.json, base.env, README.md
```

### "ABORT: testnet=true"
Edit the config file and set `"testnet": false`

### "Connection failed"
1. Check internet connectivity
2. Verify API keys are valid and not expired
3. Check if exchange is operational

### "Stop loss required"
Every trade MUST have a `stop_loss` field. No exceptions.

---

## Audit Trail

All trades logged to `logs/trade_audit.jsonl`:

```bash
tail -10 logs/trade_audit.jsonl
```

Format:
```json
{"timestamp": "2025-12-04T10:30:00", "trade": {...}, "result": {...}, "success": true}
```
