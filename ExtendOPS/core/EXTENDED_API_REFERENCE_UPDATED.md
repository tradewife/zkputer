# Extended Exchange API Reference

## Key Findings (Dec 4, 2025)

### Order Management
- **Stark Key Signature:** Required for all order management endpoints.
- **Price Parameter:** MANDATORY for ALL orders, including "Market" orders.
- **Fee Parameter:** MANDATORY. Use maker fee for Post-only, taker fee for others.
- **Expiration:** MANDATORY. Epoch timestamp in ms. Max 90 days (Mainnet).
- **Market Orders:** NOT natively supported. Must be simulated as **Limit IOC** with price buffer (Buy: Best Ask * 1.0075, Sell: Best Bid * 0.9925).

### SDK Configuration
- `MAINNET_CONFIG`: For new accounts.
- `MAINNET_CONFIG_LEGACY_SIGNING_DOMAIN`: For accounts created on legacy `app.x10.exchange`.

### Common Pitfalls
- **Hanging Orders:** Likely due to missing mandatory parameters (Price, Fee, Expiration) in SDK call which might be waiting for a response that never comes or failing silently in the signing process.
- **Websockets:** SDK relies on websockets for updates. If blocked, it might hang.

## Actionable Fixes for Executor
1. **Explicitly set `time_in_force`**: Use `IOC` for market orders, `GTT` for limit.
2. **Explicitly set `price`**: Even for market orders (use calculated buffer).
3. **Explicitly set `fee`**: If SDK doesn't handle it automatically (SDK *should* handle it, but good to verify).
4. **Disable Websockets (if possible)**: Or ensure async loop is clean.
