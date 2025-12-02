# OpenBB CLI Installation Guide - Linux Mint

## Quick Start Installation

### Step 1: Install System Prerequisites
```bash
# Update package manager
sudo apt update

# Install webkit dependency (required for OpenBB CLI)
sudo apt install libwebkit2gtk-4.0-dev

# Install Rust and Cargo (if not already installed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env

# Verify Rust installation
rustc --version
cargo --version
```

### Step 2: Create Python Virtual Environment
```bash
cd /home/kt/Desktop/HyperOPS

# Create venv for OpenBB (Python 3.10-3.13 required)
python3 --version  # Verify version

# If you need Python 3.11+ and don't have it:
# sudo add-apt-repository ppa:deadsnakes/ppa
# sudo apt install python3.11 python3.11-venv

# Create virtual environment
python3 -m venv venv_openbb
source venv_openbb/bin/activate
```

### Step 3: Install OpenBB CLI
```bash
# With venv activated
pip install openbb-cli

# Verify installation
openbb --version
```

###Step 4: Launch OpenBB CLI
```bash
# Start the CLI
openbb

# You should see the OpenBB Terminal interface
```

---

## Using OpenBB CLI for HyperOPS

### Free Data Sources (No API Keys Required)

**Economic Data (FRED):**
```
/economy/fred --symbol DFF          # Federal Funds Rate
/economy/fred --symbol T10Y2Y       # 10Y-2Y Yield Spread
/economy/fred --symbol VIXCLS       # VIX
/economy/fred --symbol M2SL         # Money Supply M2
```

**Crypto Data:**
```
/crypto/load BTC
/crypto/load ETH
/crypto/chart BTC --vs USD
```

**Congress Trading:**
```
/stocks/gov/lasttrades
/stocks/gov/topbuys
/stocks/gov/topsells
```

---

## Integration with HyperOPS Workflow

### Manual Workflow (Phase 1)
1. **Morning Routine:**
   - Launch OpenBB CLI
   - Check FRED macro indicators
  - Note key metrics in daily brief

2. **Pre-Trading Scan:**
   - Run `/economy/fred --symbol DFF,T10Y2Y,VIXCLS`
   - Export data to clipboard or file
   - Paste into macro section of trading brief

### Python Integration (Phase 2 - Optional)
Create helper scripts to automate CLI data fetching:

```python
# openbb_helper.py
import subprocess
import json

def get_fred_data(symbols):
    """Fetch FRED data via OpenBB CLI"""
    cmd = f"openbb /economy/fred --symbol {symbols} --export json"
    result = subprocess.run(cmd, shell=True, capture_output=True)
    return json.loads(result.stdout)

# Usage in daily routine
macro_data = get_fred_data("DFF,T10Y2Y,VIXCLS")
```

---

## Useful Commands for Trading

### Market Regime Detection
```bash
# Fed Policy
/economy/fred --symbol DFF,DFEDTARU,DFEDTARL

# Yield Curve
/economy/fred --symbol T10Y2Y,T10Y3M

# Volatility
/economy/fred --symbol VIXCLS,VIXMAX,VIXMIN

# Credit Spreads
/economy/fred --symbol BAMLH0A0HYM2
```

### Crypto Market Data
```bash
# Price Charts
/crypto/chart BTC --vs USD --days 30
/crypto/chart ETH --vs USD --days 30

# Market Overview
/crypto/overview
```

---

## Cost: $0/month
All data sources listed above are **FREE** and require no API keys!

---

## Troubleshooting

**Error: "Rust not found"**
```bash
source $HOME/.cargo/env
# Or add to ~/.bashrc permanently:
echo 'source $HOME/.cargo/env' >> ~/.bashrc
```

**Error: "libwebkit not found"**
```bash
sudo apt install libwebkit2gtk-4.0-dev
```

**Python version incompatible:**
```bash
# Install Python 3.11
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.11 python3.11-venv
python3.11 -m venv venv_openbb
```

---

## Next Steps

1. Install OpenBB CLI using commands above
2. Test basic FRED data retrieval
3. Manually integrate into daily brief template
4. (Optional) Create Python helper scripts for automation

**Ready to install? Run the commands in order above!**
