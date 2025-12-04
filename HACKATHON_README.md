# ZKputer: The Sovereign Shadow Trader

> **Zypherpunk Hackathon Submission**
> 
> Privacy-preserving AI trading framework that piggybacks on AI-native IDEs

---

## What is ZKputer?

ZKputer is **not an app**. It's a **protocol layer** that enables any AI coding assistant (Claude, Cursor, Antigravity, Grok, etc.) to become an expert crypto trader while maintaining:

1. **Full Auditability** - Every decision logged to append-only audit trail
2. **Protocol Compliance** - Machine-readable rules that AI agents must follow
3. **Human Authority** - No trade executes without explicit user approval
4. **Privacy-Preserving** - Optional ZEC funding via NEAR Intents

**The AI is the brain. ZKputer is the protocol.**

---

## Quick Start (For AI Agents)

When an AI agent opens this repository, it should:

```
1. Read .zkputer/AGENT_BOOTSTRAP.md
2. Check .zkputer/ACTIVE_OPS.json for current mode
3. Load protocols from protocols/core/ and protocols/ops/
4. Execute daily routine, logging to SESSION_LOG.jsonl
5. Present findings, wait for human approval before trading
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        ZKputer                              │
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   AI Agent  │───▶│  Protocols  │───▶│  Executor   │     │
│  │ (IDE/CLI)   │    │ (.zkputer/) │    │  (OPS API)  │     │
│  └─────────────┘    └─────────────┘    └──────┬──────┘     │
│                                               │             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Privacy Layer (Optional)                │   │
│  │  ┌──────────────┐         ┌──────────────────────┐  │   │
│  │  │ Zcash Wallet │────────▶│ NEAR Intents (TEE)   │  │   │
│  │  │  (Shielded)  │         │  Chain Signatures    │  │   │
│  │  └──────────────┘         └──────────────────────┘  │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## The Hook: `.zkputer/`

The `.zkputer/` directory is the entry point for any AI agent:

```
.zkputer/
├── AGENT_BOOTSTRAP.md    # First file any agent reads
├── ACTIVE_OPS.json       # Current mode, account config
└── SESSION_LOG.jsonl     # Append-only audit trail
```

### AGENT_BOOTSTRAP.md
Tells the AI agent:
- What ZKputer is and its core principles
- How to load protocols
- Command structure (Read Handbook, Run the Daily, Execute)
- What must be logged

### ACTIVE_OPS.json
Machine-readable configuration:
- Current OPS mode (BaseOPS, ExtendOPS, HyperOPS, PumpOPS)
- Account parameters (equity, risk limits)
- API config paths

### SESSION_LOG.jsonl
Append-only audit trail capturing:
- Every market scan
- Every trade signal
- Every user approval
- Every execution result
- Every compliance violation

---

## Protocols: Single Source of Truth

```
protocols/
├── core/
│   ├── MASTER_PROTOCOL.md      # Universal rules
│   ├── RISK_LIMITS.json        # Machine-readable limits
│   └── COMPLIANCE_SCHEMA.json  # Trade validation schema
│
└── ops/
    ├── base.md    # BaseOPS (Base chain gems)
    ├── extend.md  # ExtendOPS (Extended perps)
    ├── hyper.md   # HyperOPS (Hyperliquid perps)
    └── pump.md    # PumpOPS (Solana sniping)
```

### MASTER_PROTOCOL.md
Non-negotiable rules:
- Human-in-the-loop (no autonomous execution)
- Risk limits (20% max per trade, 12x leverage cap)
- Data integrity (no hallucinated prices)
- Audit requirements

### RISK_LIMITS.json
Machine-readable constraints loaded by `ComplianceOfficer`:
```json
{
  "universal": {
    "max_risk_per_trade_percent": 20,
    "max_leverage": 12,
    "max_concurrent_positions": 2
  },
  "ops_specific": {
    "BaseOPS": {"max_fdv_usd": 4000000, "min_liquidity_usd": 50000},
    "ExtendOPS": {"min_24h_volume_usd": 500000}
  }
}
```

---

## OPS Modes

### ExtendOPS (Default)
- **Exchange:** Extended Exchange
- **Focus:** USDC-margined perpetuals
- **Symbols:** BTC-USD, ETH-USD, SOL-USD
- **Strategy:** Thesis-driven trading with whale intel

### HyperOPS
- **Exchange:** Hyperliquid
- **Focus:** USDC-margined perpetuals
- **Symbols:** BTC-PERP, ETH-PERP, SOL-PERP
- **Strategy:** Same as ExtendOPS, different API

### BaseOPS
- **Chain:** Base (Coinbase L2)
- **Focus:** Early-stage gem discovery
- **Criteria:** FDV <$4M, Liquidity >$50K
- **Strategy:** LT_Score evaluation (5 modules)

### PumpOPS
- **Chain:** Solana
- **Focus:** High-speed token sniping
- **Venues:** Pump.fun, Jupiter, Raydium
- **Strategy:** Speed + rug detection

---

## Privacy Integration

### Zcash Funding
Fund ZKputer with shielded ZEC to break on-chain identity links:

```bash
# Setup (see ZCASH_WALLET_SETUP.md)
zcash-cli z_getnewaddress sapling
# Fund the address, then use for trades
```

### NEAR Intents
Cross-chain execution via TEE:

```
ZEC (Shielded) → NEAR Intents → Any Chain (Base, Solana, etc.)
```

**For Demo:** Using ExtendOPS directly (no ZEC required)

---

## Demo Flow

### 1. Initialize
```bash
python3 src/main.py
> Read Handbook
```
Agent loads protocols, confirms readiness.

### 2. Run Daily Routine
```bash
> Run the Daily
```
Agent scans markets, analyzes whale intel, generates setups.

### 3. Review Signals
Agent presents trade signals with full compliance checks.

### 4. Execute (Human Approval)
```bash
> Execute SOL-USD long
```
Agent executes only after explicit command.

### 5. Audit
Check `.zkputer/SESSION_LOG.jsonl` for full audit trail.

---

## Key Innovations

### 1. Agent-Agnostic Design
Works with any AI IDE/CLI that can read files and execute commands. No special integration needed.

### 2. Protocol-as-Code
Handbooks are the source of truth. AI agents load and follow them programmatically.

### 3. Append-Only Audit
Every decision logged. Immutable. Verifiable.

### 4. Privacy-First Architecture
Optional ZEC + NEAR Intents layer breaks identity links.

### 5. Human Authority
AI researches autonomously. Execution requires explicit approval.

---

## File Structure

```
ZKputer/
├── .zkputer/              # THE HOOK (agent entry point)
├── protocols/             # Single source of truth
│   ├── core/              # Universal rules
│   └── ops/               # OPS-specific protocols
├── ops/                   # OPS modules (legacy, for reference)
│   ├── BaseOPS/
│   ├── ExtendOPS/
│   ├── HyperOPS/
│   └── PumpOPS/
├── src/
│   └── core/
│       ├── handbook.py    # Protocol loader
│       ├── compliance.py  # Rule enforcement
│       ├── session_logger.py  # Audit trail
│       ├── zcash_wallet.py    # ZEC integration
│       └── near_intents.py    # Cross-chain execution
├── integrations/          # Privacy layer docs
│   ├── zcash/
│   └── near_intents/
└── demos/                 # Demo scripts
```

---

## Running the Demo

### Prerequisites
```bash
python3.12+
# Optional: zcashd for privacy layer
```

### Basic Demo (ExtendOPS)
```bash
cd ZKputer
python3 src/main.py
```

### With Privacy Layer
1. Setup Zcash wallet (see `ZCASH_WALLET_SETUP.md`)
2. Fund with ZEC
3. Enable NEAR Intents in `ACTIVE_OPS.json`
4. Run demo

---

## Hackathon Tracks

### Private DeFi & Trading
- Core use case: Privacy-preserving AI trading
- ZEC funding layer breaks on-chain identity

### Cross-Chain Privacy
- NEAR Intents enable trading on any chain
- No need to hold native gas tokens

### Zcash Integration
- Shielded wallet as funding source
- Full privacy from entry to exit

---

## Team

Built for the Zypherpunk Hackathon by the ZKputer team.

---

## License

MIT

---

**The AI is the brain. ZKputer is the protocol. The human is in control.**
