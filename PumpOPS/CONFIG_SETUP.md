# ⚙️ PumpOPS Configuration Setup Guide

## Overview
This guide walks you through configuring PumpOPS for optimal Solana sniping performance.

---

## Step 1: Understanding Configuration Files

### Scanning Parameters (`⚙️ Configuration/config/scanning_config.json`)
This file controls scan behavior for Solana:

- **FDV Range**: $50k-$500k (Pump.Fun/early Raydium)
- **Liquidity Minimums**: >$5k (Pump.Fun), >$50k (Raydium)
- **Volume Thresholds**: >$10k in 5 mins (Momentum filter)
- **Security**: Mint/Freeze Auth MUST be revoked

**You can edit these values** to tune scanning, but maintain strict security filters.

### Wallet Configuration (`.env`)
Store your private key and RPC URL:
```
SOLANA_PRIVATE_KEY=your_base58_key
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
```

---

## Step 2: Solana Wallet Setup

1. **Export Private Key** from Phantom/Solflare (Base58 format)
2. **Create `.env` file** in `⚙️ Configuration/config/`
3. **Paste credentials** (see above)
4. **⚠️ Security:** Use a dedicated hot wallet with limited funds (5 SOL max)

---

## Step 3: Adjust Scanning Parameters

### Common Adjustments

#### Focus on Bonding Curve (Higher Risk)
```json
{
  "mcap_range": {
    "min": 10000,
    "max": 100000
  }
}
```

#### Focus on Raydium (Lower Risk)
```json
{
  "liquidity_minimum": {
    "raydium": 100000
  }
}
```

---

## Step 4: Knowledge Graph Initialization

The knowledge graph files in `🧠 Learning Engine/knowledge_graph/` are initialized with Solana templates.

### Add KOLs (`target_socials.md`)
Add Solana influencers to track for alpha.

### Add Smart Wallets (`smart_money.md`, `wallets.md`)
Document known sniper/insider wallets.

### Define Setups (`playbook.md`)
Add your own proven Solana memecoin patterns.

---

## Step 5: Verify Setup

### Test Solana Connection
```bash
python "PumpOPS/📊 Core Trading System/test_solana_connection.py"
```

**Expected:**
```
✅ Connected to Solana Mainnet
💰 Balance: X SOL
```

---

## Step 6: Run First Scan

```
Command: "Run the Daily"
```

The agent will:
1. Scan Padre.gg + Pump.Fun
2. Apply security filters
3. Generate "The Menu" of 1-4 opportunities

---

## Troubleshooting

### Issue: Wallet not loading
**Solution:** Check that `SOLANA_PRIVATE_KEY` is valid Base58 in `.env`

### Issue: RPC errors
**Solution:** Use a premium RPC (Helius/QuickNode) for faster execution

---

**Configuration complete! PumpOPS is ready for Solana sniping.**
