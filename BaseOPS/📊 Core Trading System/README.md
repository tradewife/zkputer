# CDP Trading System - Setup Guide

## 🎯 Overview

BaseOPS now supports automated token trading on Base chain using Coinbase Developer Platform (CDP) SDK.

**Key Features:**
- ✅ Secure MPC wallets (no private key management)
- ✅ Built-in token swaps via `wallet.trade()`
- ✅ Automatic DEX routing (Uniswap/Aerodrome)
- ✅ Risk-based position sizing (20% max per trade)
- ✅ User-authorized execution only

---

## 📦 Installation Complete

✅ Virtual environment created: `venv_trading/`  
✅ CDP SDK installed: `cdp-sdk@1.33.3`  
✅ Dependencies installed: `python-dotenv`, `web3`, etc.

---

## 🚀 Next Steps (USER ACTIONS REQUIRED)

### 1. Get CDP API Credentials

1. Go to **https://portal.cdp.coinbase.com/**
2. Sign up / Log in with your Coinbase account
3. Create a new API key:
   - Click "API Keys" → "Create API Key"
   - Download the JSON file (contains your private key)
   - **IMPORTANT:** Save this file securely - you can only download it once!

### 2. Configure Environment

1. Copy the example file:
   ```bash
   cp "⚙️ Configuration/config/.env.example" "⚙️ Configuration/config/.env"
   ```

2. Edit `.env` and add your CDP credentials from the downloaded JSON:
   ```
   CDP_API_KEY_NAME=organizations/xxxx/apiKeys/xxxx
   CDP_PRIVATE_KEY=-----BEGIN EC PRIVATE KEY-----
   ...
   -----END EC PRIVATE KEY-----
   ```

3. Set network (testnet recommended for initial testing):
   ```
   CDP_NETWORK=base-sepolia  # or base-mainnet for production
   ```

### 3. Test CDP Connection

Run the client module to verify everything works:

```bash
cd /home/kt/Desktop/BaseOPS
./venv_trading/bin/python "📊 Core Trading System/cdp_client.py"
```

**Expected output:**
```
✅ CDP configured for base-mainnet
✅ Created new wallet: 0x...
💰 ETH balance: 0.0
```

---

## 📂 File Structure

```
BaseOPS/
├── 📊 Core Trading System/
│   └── cdp_client.py         ✅ CREATED - Wallet management
├── ⚙️ Configuration/
│   └── config/
│       ├── .env.example      ✅ CREATED - Template
│       └── trading_config.json ✅ CREATED - Settings
└── venv_trading/             ✅ CREATED - Virtual env
```

---

## 🔐 Security Notes

- ⚠️ **Never commit `.env` to git** - add to `.gitignore`
- ⚠️ **Never share your CDP private key**
- ✅ CDP uses MPC wallets - more secure than traditional private keys
- ✅ All trades require explicit user command ("Execute trade 1")

---

## 🧪 Testing Plan

1. **Testnet First:** Use `base-sepolia` to test with fake tokens
2. **Small Amounts:** Start with $5-10 on mainnet
3. **Verify Positions:** Check wallet balances after each trade
4. **Monitor Gas:** Base L2 gas is ~$0.50-2 per trade

---

## Next Implementation Phase

**Phase 2: Trading & Position Tracking**
- [ ] Create `cdp_swap_module.py` - Token buy/sell logic
- [ ] Create `position_tracker.py` - P&L tracking
- [ ] Test swaps on testnet

**Waiting for:** User to complete CDP setup (Steps 1-3 above)
