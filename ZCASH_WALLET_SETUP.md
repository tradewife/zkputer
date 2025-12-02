# Zcash Wallet Setup - Official zcashd Integration

## Overview

ZKputer now uses **zcashd RPC** for real Zcash wallet functionality. This is the official, production-ready method.

## Quick Start

### Option 1: Use Existing Zashi Wallet (Recommended for Hackathon)

1. Download **Zashi**: https://electriccoin.co/zashi/
2. Fund your wallet with testnet ZEC
3. Use ZKputer for NEAR Intents swaps

### Option 2: Install zcashd (Full Integration)

#### 1. Install zcashd

```bash
# Add Zcash repository
sudo apt-get update
sudo apt-get install -y apt-transport-https wget gnupg2

# Download and install
wget https://z.cash/downloads/zcash-5.7.0-linux64-debian-stretch.tar.gz
tar -xzf zcash-5.7.0-linux64-debian-stretch.tar.gz
sudo cp zcash-5.7.0/bin/* /usr/local/bin/
```

#### 2. Configure zcashd

Create `~/.zcash/zcash.conf`:

```conf
# Testnet
testnet=1

# RPC Settings
rpcuser=zcash
rpcpassword=your_secure_password_here
rpcport=18232

# Enable shielded transactions
experimentalfeatures=1
```

#### 3. Start zcashd

```bash
# Start daemon
zcashd -daemon

# Check status
zcash-cli getinfo

# Wait for sync (can take hours)
zcash-cli getblockchaininfo
```

#### 4. Get Testnet ZEC

```bash
# Get new shielded address
zcash-cli z_getnewaddress sapling

# Request from faucet: https://faucet.testnet.z.cash/
# Wait for funds
zcash-cli z_getbalance
```

## ZKputer Integration

### Configure Environment

``bash
export ZCASH_RPC_USER=zcash
export ZCASH_RPC_PASSWORD=your_password
```

### Test Wallet

```python
from src.core.zcash_wallet import ZcashWallet

wallet = ZcashWallet()
print(f"Balance: {wallet.get_balance()} ZEC")
print(f"Address: {wallet.get_address()}")
```

### Send Shielded ZEC

```python
# Send to another address
tx_id = wallet.send(
    to_address="zs1recipient_address",
    amount=0.1,
    memo="ZKputer test"
)
```

## Architecture

```
ZKputer
  ↓
ZcashWallet (src/core/zcash_wallet.py)
  ↓
ZcashRPCClient (JSON-RPC)
  ↓
zcashd daemon
  ↓
Zcash Network (Testnet/Mainnet)
```

## Demo Mode

If zcashd is not running, wallet falls back to demo mode:
- Returns simulated balance (150 ZEC)
- Generates demo addresses
- Perfect for testing NEAR integration

## Production Checklist

- [  ] Install zcashd
- [ ] Configure zcash.conf with strong password
- [ ] Sync blockchain (testnet ~1-2 hours)
- [ ] Fund wallet with testnet ZEC
- [ ] Test send/receive
- [ ] Set environment variables
- [ ] Ready for NEAR Intents!

## Resources

- **zcashd Download:** https://z.cash/download/
- **Documentation:** https://zcash.readthedocs.io/
- **Testnet Faucet:** https://faucet.testnet.z.cash/
- **Block Explorer:** https://explorer.testnet.z.cash/
- **Zashi Wallet:** https://electriccoin.co/zashi/
