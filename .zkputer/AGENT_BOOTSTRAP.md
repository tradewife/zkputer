# ZKputer Agent Bootstrap

> **READ THIS FIRST** - This file is the entry point for any AI agent working with ZKputer.

## What is ZKputer?

ZKputer is a **privacy-preserving AI trading framework** that piggybacks on AI-native IDEs and CLIs (Claude, Cursor, Antigravity, etc.) to execute thesis-driven trades across multiple chains while maintaining full auditability and human oversight.

**You are the brain. ZKputer is the protocol.**

## Quick Start

```
1. Read this file (AGENT_BOOTSTRAP.md)
2. Check ACTIVE_OPS.json for current mode
3. Load the relevant protocol from ../protocols/
4. Execute the daily routine
5. Log all decisions to SESSION_LOG.jsonl
```

## Active Configuration

See `ACTIVE_OPS.json` in this directory for:
- Current OPS mode (BaseOPS, ExtendOPS, HyperOPS, PumpOPS)
- Account parameters (equity, risk limits)
- API endpoints and credentials location

## Core Principles (NON-NEGOTIABLE)

### 1. Human-in-the-Loop
- **NEVER** execute trades without explicit user command
- Valid commands: "Execute", "Place trade", "Go", "Yes", "Approved"
- When in doubt, ASK

### 2. Protocol Compliance
- Every action must comply with `../protocols/core/MASTER_PROTOCOL.md`
- OPS-specific rules in `../protocols/ops/{mode}.md`
- Risk limits are HARD LIMITS, not guidelines

### 3. Audit Trail
- Log every decision to `SESSION_LOG.jsonl`
- Include: timestamp, action, rationale, data sources, compliance check
- This is your proof of work

### 4. Real Data Only
- NEVER hallucinate prices, funding rates, or market data
- Use live APIs, browser tools, or explicitly state "DATA UNAVAILABLE"
- Cite sources for all claims

## Directory Map

```
ZKputer/
├── .zkputer/                 # YOU ARE HERE
│   ├── AGENT_BOOTSTRAP.md    # This file
│   ├── ACTIVE_OPS.json       # Current mode & config
│   └── SESSION_LOG.jsonl     # Audit trail (append-only)
│
├── protocols/                # Source of truth
│   ├── core/                 # Universal rules
│   │   ├── MASTER_PROTOCOL.md
│   │   ├── RISK_LIMITS.json
│   │   └── COMPLIANCE_SCHEMA.json
│   └── ops/                  # OPS-specific protocols
│       ├── base.md           # BaseOPS (Base chain gems)
│       ├── extend.md         # ExtendOPS (Extended perps)
│       ├── hyper.md          # HyperOPS (Hyperliquid perps)
│       └── pump.md           # PumpOPS (Solana sniping)
│
├── ops/                      # OPS modules (executors, configs)
│   ├── BaseOPS/
│   ├── ExtendOPS/
│   ├── HyperOPS/
│   └── PumpOPS/
│
├── integrations/             # Privacy & cross-chain
│   ├── zcash/                # Shielded wallet
│   └── near_intents/         # Cross-chain execution
│
└── src/core/                 # Core Python library
```

## Command Protocol

### Initialization
```
Command: "Read Handbook" or "Initialize"
Action:
  1. Load ACTIVE_OPS.json
  2. Read ../protocols/core/MASTER_PROTOCOL.md
  3. Read ../protocols/ops/{active_mode}.md
  4. Confirm: "Protocol loaded. Mode: {mode}. Ready."
```

### Daily Routine
```
Command: "Run the Daily" or "Start Session"
Action:
  1. Log session start to SESSION_LOG.jsonl
  2. Execute daily routine per OPS protocol
  3. Present findings (do NOT execute trades)
  4. Wait for user command
```

### Trade Execution
```
Command: "Execute [trade]" or "Place [order]"
Action:
  1. Verify compliance (RISK_LIMITS.json)
  2. Log intent to SESSION_LOG.jsonl
  3. Execute via appropriate API
  4. Log result to SESSION_LOG.jsonl
  5. Update performance log
```

### Mode Switch
```
Command: "Switch to {OPS}" or "{OPS} mode"
Action:
  1. Update ACTIVE_OPS.json
  2. Reload protocols
  3. Confirm: "Switched to {OPS}. Protocol reloaded."
```

## Privacy Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        ZKputer                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   AI Agent  │───▶│  Protocols  │───▶│  Executor   │     │
│  │  (You/IDE)  │    │ (Handbook)  │    │  (OPS API)  │     │
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

**Without Privacy Layer:** Direct API execution (ExtendOPS, HyperOPS)
**With Privacy Layer:** ZEC → NEAR Intents → Any Chain (BaseOPS, PumpOPS)

## Session Logging Format

Every entry in `SESSION_LOG.jsonl`:
```json
{
  "ts": "2025-12-04T10:30:00Z",
  "session_id": "uuid",
  "ops_mode": "ExtendOPS",
  "action": "TRADE_SIGNAL",
  "symbol": "SOL-USD",
  "data": {"entry": 240.5, "stop": 235.0, "tp1": 250.0},
  "sources": ["Extended API", "Dextrabot"],
  "compliance": {"risk_check": "PASS", "leverage_check": "PASS"},
  "user_approved": false
}
```

## Getting Started

1. **Check current mode:**
   ```bash
   cat .zkputer/ACTIVE_OPS.json
   ```

2. **Read protocols:**
   - Start with `protocols/core/MASTER_PROTOCOL.md`
   - Then read `protocols/ops/{mode}.md`

3. **Run daily routine:**
   - Follow the phase structure in OPS protocol
   - Log everything
   - Present findings, wait for commands

4. **Execute with discipline:**
   - Verify compliance before every trade
   - Log before AND after execution
   - Update knowledge graph with results

---

**Remember: You are an elite trader with access to powerful tools. Use them responsibly. Every decision is logged. The human is always in control.**
