# HyperOPS Configuration Setup

## 📋 Configuration File Created

Your config file is ready at: `config/trading_config.json`

## 🔑 How to Fill It Out:

### 1. Get Your Wallet Address
- Go to https://app.hyperliquid.xyz/
- Connect your wallet
- Copy your wallet address (starts with 0x...)
- Replace `0xYOUR_WALLET_ADDRESS_HERE` with your address

### 2. Get Your Private Key
**⚠️ IMPORTANT SECURITY NOTES:**
- **NEVER** share your private key with anyone
- **NEVER** commit private keys to git
- **ONLY** use testnet keys initially
- Consider creating a separate API wallet

#### Option A: Use Existing Wallet Private Key
- From your wallet (MetaMask, etc.), export your private key
- Replace `YOUR_PRIVATE_KEY_HERE` with the key (without 0x prefix)

#### Option B: Create API Wallet (Recommended)
1. Go to https://app.hyperliquid.xyz/API
2. Click "Create New API Key"
3. Set permissions (trading only, no withdrawal)
4. Copy the private key
5. Use your MAIN wallet address as `account_address`
6. Use the API private key as `secret_key`

### 3. Testnet vs Mainnet
- `"testnet": true` - Use testnet (safe for testing)
- `"testnet": false` - Use mainnet (real money)

## 📝 Example Filled Config:

```json
{
  "account_address": "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b",
  "secret_key": "abc123def456ghi789jkl012mno345pqr678stu901vwx234yz",
  "testnet": true,
  "max_risk_percent": 0.20,
  "leverage_min": 9,
  "leverage_max": 12,
  "max_positions": 2
}
```

## 🚀 After Configuration:

```bash
# Test your configuration
python test_trading_system.py

# Run your first trading session
python hyperops_cli.py session
```

## ⚠️ Security Best Practices:

1. **Start with testnet** - Set `"testnet": true` initially
2. **Use small amounts** - Start with minimal capital on mainnet
3. **API wallet recommended** - Don't use your main wallet's private key
4. **Monitor closely** - Watch your first few trades manually
5. **Keep backups** - Save your config securely

## 🔍 Troubleshooting:

- **Address mismatch**: Ensure the address matches your private key
- **Invalid key**: Check private key format (remove 0x prefix if present)
- **Permission denied**: Ensure API key has trading permissions
- **Testnet issues**: Make sure testnet is enabled for testnet trading