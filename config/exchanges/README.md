# Exchange Configuration

**SECURITY: These files contain LIVE MAINNET credentials. Never commit to git.**

## Active Exchanges

| Exchange | Config File | Network | Status |
|----------|-------------|---------|--------|
| Extended Exchange | `extended.json` | Mainnet | Active |
| Hyperliquid | `hyperliquid.json` | Mainnet | Active |
| Base (Coinbase) | `base.env` | Mainnet | Active |

## Configuration Structure

### Extended Exchange (`extended.json`)
```json
{
  "account_address": "0x...",
  "api_key": "...",
  "stark_public_key": "0x...",
  "stark_private_key": "0x...",
  "vault_number": 232387,
  "testnet": false
}
```
**SDK:** `x10-python-trading-starknet`

### Hyperliquid (`hyperliquid.json`)
```json
{
  "account_address": "0x...",
  "secret_key": "0x...",
  "testnet": false
}
```
**SDK:** `hyperliquid-python-sdk`

### Base/Coinbase (`base.env`)
```
CDP_API_KEY_ID=...
CDP_API_KEY_SECRET=...
CDP_NETWORK=base-mainnet
```
**SDK:** `cdp-sdk`

## Credential Verification

Before any trading session, verify configs exist and are valid:
```bash
python -c "from src.core.exchanges import verify_all_configs; verify_all_configs()"
```

## Key Rotation

When rotating keys:
1. Generate new keys on exchange UI
2. Update the respective config file
3. Test with `verify_all_configs()`
4. Archive old key (do not delete immediately)
