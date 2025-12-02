# Extended Exchange API Reference

**Official Documentation**: https://api.docs.extended.exchange/  
**Python SDK**: https://github.com/x10xchange/python_sdk  
**SDK Package**: `x10-python-trading-starknet`

## Base Configuration

### Mainnet (Production)
```python
from x10.perpetual.configuration import MAINNET_CONFIG

# Endpoints:
# API: https://api.starknet.extended.exchange/api/v1
# WebSocket: wss://api.starknet.extended.exchange/stream.extended.exchange/v1
# UI: https://app.extended.exchange/perp
```

### Testnet (Development)
```python
from x10.perpetual.configuration import TESTNET_CONFIG

# Endpoints:
# API: https://api.starknet.sepolia.extended.exchange/api/v1
# WebSocket: wss://starknet.sepolia.extended.exchange/stream.extended.exchange/v1
```

## Canonical Usage Pattern

### 1. Initialize Account (from trading_module.py)
```python
from x10.perpetual.accounts import StarkPerpetualAccount

stark_account = StarkPerpetualAccount(
    vault=vault_number,
    private_key=stark_private_key,
    public_key=stark_public_key,
    api_key=api_key,
)
```

### 2. Create Trading Client
```python
from x10.perpetual.trading_client import PerpetualTradingClient
from x10.perpetual.configuration import MAINNET_CONFIG

trading_client = PerpetualTradingClient.create(
    MAINNET_CONFIG, 
    stark_account
)
```

### 3. Access Modules
```python
# Account operations
balance = await trading_client.account.get_balance()
positions = await trading_client.account.get_positions()
open_orders = await trading_client.account.get_open_orders()

# Order management
placed_order = await trading_client.place_order(...)
await trading_client.orders.cancel_order(order_id=order.id)

# Market data
markets = await trading_client.markets_info.get_markets()
```

## Key Public REST API Endpoints

### Market Data
```
GET /api/v1/info/markets?market={market}
GET /api/v1/info/markets/{market}/stats
GET /api/v1/info/markets/{market}/orderbook
GET /api/v1/info/markets/{market}/trades
GET /api/v1/info/candles
GET /api/v1/info/funding-rates
GET /api/v1/info/open-interest
```

## Available SDK Methods

### Account Module (`trading_client.account`)

#### `get_balance()`
Returns account balance information.

#### `get_positions(market_names=None, side=None)`
Returns current open positions. Can filter by market and side.

**Returns**: List of `PositionModel`
```python
class PositionModel:
    id: int
    market: str
    side: PositionSide  # LONG or SHORT
    leverage: Decimal
    size: Decimal
    value: Decimal
    open_price: Decimal
    mark_price: Decimal
    liquidation_price: Optional[Decimal]
    unrealised_pnl: Decimal
    realised_pnl: Decimal
    tp_price: Optional[Decimal]
    sl_price: Optional[Decimal]
```

#### `get_positions_history(market_names=None, side=None)`
Returns historical closed positions.

#### `get_open_orders(market_names=None, order_type=None, side=None)`
Returns all open orders. Can filter by market, type, and side.

**Returns**: List of `OpenOrderModel`
```python
class OpenOrderModel:
    id: int
    external_id: str
    market: str
    type: OrderType  # LIMIT, MARKET, STOP, etc.
    side: OrderSide  # BUY or SELL
    status: OrderStatus
    price: Decimal
    average_price: Optional[Decimal]
    qty: Decimal
    filled_qty: Optional[Decimal]
    reduce_only: bool
    post_only: bool
```

#### `get_orders_history(market_names=None, order_type=None, side=None, cursor=None, limit=None)`
Returns historical orders with pagination.

#### `get_trades(market_names=None, side=None, trade_type=None)`
Returns user's trade history.

#### `get_leverage(market_names=List[str])`
Returns current leverage for specified markets.

**Returns**: List of `AccountLeverage`
```python
class AccountLeverage:
    market: str
    leverage: Decimal
```

#### `update_leverage(market_name: str, leverage: Decimal)`
Updates leverage for a specific market.

#### `get_fees(market_names=None)`
Returns trading fee structure for markets.

### Order Management Module (`trading_client.orders`)

#### `place_order()` (via `trading_client.place_order()`)
```python
placed_order = await trading_client.place_order(
    market_name="BTC-USD",
    amount_of_synthetic=Decimal("1"),
    price=Decimal("63000.1"),
    side=OrderSide.SELL,  # or OrderSide.BUY
    reduce_only=False,
    post_only=False,
    time_in_force=TimeInForce.GTC,
)
```

#### `cancel_order(order_id: int)`
Cancels a specific order by ID.

#### `mass_cancel(order_ids: List[int])`
Cancels multiple orders at once.

### Markets Info Module (`trading_client.markets_info`)

#### `get_markets(market_names=None)`
Returns market configurations and statistics.

**Market Response**:
```python
{
    "name": "BTC-USD",
    "assetName": "BTC",
    "status": "ACTIVE",  # ACTIVE, REDUCE_ONLY, DELISTED, etc.
    "marketStats": {
        "lastPrice": "42000",
        "markPrice": "39950",
        "indexPrice": "39940",
        "fundingRate": "0.001",
        "openInterest": "1245.2",
        "dailyVolume": "39659164065",
        "dailyPriceChangePercentage": "5.57"
    },
    "tradingConfig": {
        "minOrderSize": "0.001",
        "maxLeverage": "50",
        "maxPositionValue": "10000000"
    }
}
```

## Order Types

### OrderSide
- `OrderSide.BUY` - Long position
- `OrderSide.SELL` - Short position

### OrderType
- `LIMIT` - Limit order at specific price
- `MARKET` - Market order (immediate execution)
- `STOP` - Stop loss order
- `STOP_LIMIT` - Stop limit order

### TimeInForce
- `GTC` - Good Till Cancel
- `IOC` - Immediate Or Cancel
- `FOK` - Fill Or Kill
- `GTT` - Good Till Time

## Market Symbols Format

Extended uses hyphenated format:
- `BTC-USD`
- `ETH-USD`
- `SOL-USD`
- `ADA-USD`
- `AVAX-USD`
- `HYPE-USD`

## Important Notes

### 1. Stop Loss Order Types
**CRITICAL**: Never use LIMIT orders for stop losses. Use proper STOP or STOP_LIMIT order types.

❌ **WRONG**:
```python
# This executes immediately!
order = await trading_client.place_order(
    market_name="BTC-USD",
    amount_of_synthetic=Decimal("1"),
    price=Decimal("50000"),  # Stop price
    side=OrderSide.SELL,
    order_type=OrderType.LIMIT  # WRONG!
)
```

✅ **CORRECT**:
```python
# This triggers only when price reaches stop level
order = await trading_client.place_order(
    market_name="BTC-USD",
    amount_of_synthetic=Decimal("1"),
    price=Decimal("50000"),  # Stop trigger price
    side=OrderSide.SELL,
    order_type=OrderType.STOP  # CORRECT!
)
```

### 2. Async/Await Pattern
The SDK uses async/await. Wrap calls in async functions:

```python
import asyncio

async def main():
    balance = await trading_client.account.get_balance()
    print(balance)

asyncio.run(main())
```

### 3. Decimal Precision
Always use `Decimal` type for prices and quantities:

```python
from decimal import Decimal

price = Decimal("42000.50")  # Correct
amount = Decimal("1.5")      # Correct
```

### 4. Authentication
The SDK handles authentication automatically using the `api_key` and stark keys. All private endpoints require:
- Valid API key in headers
- Proper Stark key signatures

## HyperOPS Integration

Our `trading_module.py` wraps the Extended SDK and provides:
- Synchronous wrappers around async SDK calls
- Error handling and retry logic
- Position and order state management
- Risk management calculations

**Primary Module**: `📊 Core Trading System/trading_module.py`

**Usage in HyperOPS**:
```python
from trading_module import ExtendedTrader

trader = ExtendedTrader()
positions = trader.get_positions()
balance = trader.get_balance()
```

## Useful Resources

- **API Docs**: https://api.docs.extended.exchange/
- **Python SDK**: https://github.com/x10xchange/python_sdk
- **Examples**: https://github.com/x10xchange/python_sdk/tree/starknet/examples
- **UI**: https://app.extended.exchange/perp
