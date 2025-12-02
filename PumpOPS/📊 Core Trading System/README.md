# Solana Trading System - Setup Guide

## 🎯 Overview

PumpOPS uses a direct **Solana RPC + Jupiter Aggregator** integration for high-speed execution.

**Key Features:**
- ✅ **Direct RPC Execution** (Solders/Solana.py)
- ✅ **Jupiter Aggregator** (Best price routing)
- ✅ **MEV Protection** (Jito bundles supported via RPC)
- ✅ **Local Wallet Management** (Private Key in .env)

---

## 📦 Installation

1.  **Install Dependencies:**
    ```bash
    pip install solana solders requests python-dotenv
    ```

---

## 🚀 Configuration (USER ACTIONS REQUIRED)

### 1. Wallet Setup
1.  Export your Solana Private Key (Base58 string) from Phantom/Solflare.
2.  **Security Warning:** This key is stored locally in `.env`. Never share it.

### 2. Configure Environment
1.  Create/Edit `.env` in `⚙️ Configuration/config/`:
    ```bash
    SOLANA_PRIVATE_KEY=your_base58_private_key_here
    SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
    # Optional: Jito Block Engine URL for MEV protection
    # BLOCK_ENGINE_URL=https://mainnet.block-engine.jito.wtf
    ```

### 3. Test Connection
Run the connection test script:
```bash
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
