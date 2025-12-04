# HyperOPS Protocol

> **Exchange:** Hyperliquid (https://app.hyperliquid.xyz)
> **Focus:** USDC-margined perpetual futures trading
> **Inherits:** `protocols/core/MASTER_PROTOCOL.md`

---

## 1. Overview

HyperOPS is the original thesis-driven perpetual trading system for Hyperliquid. It shares the same methodology as ExtendOPS but targets Hyperliquid's native infrastructure and APIs.

**Symbol Format:** `BTC-PERP`, `ETH-PERP`, `SOL-PERP`, etc.

---

## 2. Key Differences from ExtendOPS

| Aspect | HyperOPS | ExtendOPS |
|--------|----------|-----------|
| Exchange | Hyperliquid | Extended Exchange |
| Symbol Format | BTC-PERP | BTC-USD |
| API | Hyperliquid SDK | Extended SDK (Stark) |
| Whale Intel | Native (same wallets) | Cross-reference HL data |

---

## 3. Account Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Default Equity | $100 | Adjust in ACTIVE_OPS.json |
| Max Risk/Trade | 20% | $20 on $100 account |
| Leverage Range | 9-12× | Verify notional ≤ $1200 |
| Max Positions | 2 | 40% total exposure |
| Entry Preference | Limit | Market allowed for urgency |

---

## 4. Daily Routine

*Same structure as ExtendOPS. Key differences:*

### Phase 1 Additions
- **Hyperliquid Native Data**
  - Use Hyperliquid API directly for funding, OI, liquidations
  - Orderbook depth (L2/L3), trade prints
  - Historical data for session analysis

### Phase 2 Whale Intel
- All whale intel platforms (Dextrabot, ApexLiquid, SuperX) track **Hyperliquid wallets**
- Data is directly applicable without cross-referencing

---

## 5. Setup Types

Same as ExtendOPS:
1. Funding Arbitrage
2. Momentum Catalyst
3. Liquidity Hunt
4. Mean Reversion
5. Smart Money Follow

---

## 6. API Integration

### Configuration
```json
// HyperOPS/config/trading_config.json
{
  "wallet_address": "0x...",
  "private_key": "...",
  "testnet": false
}
```

### Executor Usage
```python
from hyperliquid.sdk import HyperliquidAPI

api = HyperliquidAPI(wallet_address, private_key)
api.place_order(
    coin="SOL",
    is_buy=True,
    sz=0.5,
    limit_px=240.0,
    order_type={"limit": {"tif": "Gtc"}}
)
```

---

## 7. Data Sources

### Market Data
- **Primary:** Hyperliquid API
- **Backup:** CoinGlass, Laevitas

### Whale Intelligence
Same as ExtendOPS (Dextrabot, ApexLiquid, SuperX)

### Social/Catalyst
- X (Twitter) for real-time catalysts
- News aggregators for macro events

---

## 8. Grok Enhancement (HyperGrok)

When using Grok as the AI agent:

### Activation
Command: "HyperGrok Run the Daily"

### Enhancements
- Direct X/Twitter integration
- Real-time sentiment analysis
- Multi-modal chart analysis
- Faster reaction to breaking news

### Protocol
1. Execute standard HyperOPS phases
2. Add X/Social alpha mining priority
3. Cross-reference whale intel with social sentiment
4. Generate enhanced Daily Trading Brief

---

## 9. Risk Rules

Identical to ExtendOPS. See `protocols/ops/extend.md` Section 6.

---

## 10. Migration Note

HyperOPS was the original system. ExtendOPS was created for Extended Exchange with:
- Updated symbol format (BTC-USD vs BTC-PERP)
- Different SDK (Stark-based)
- Same core methodology

Both can be run simultaneously on different accounts.

---

**Execute with precision. Trade with thesis. Manage risk relentlessly.**
