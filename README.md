# ZKputer: Sovereign Shadow Trader

Privacy-first, cross-chain power-up that keeps **research, execution, and funding inside a zero-knowledge perimeter**. ZKputer leverages browser-native AI pair-programmers with shielded Zcash capital, NEAR AI trusted execution, and NEAR Intents orchestration so every move remains private yet auditable.

**Hackathon:** Zypherpunk 2025 | **Focus:** privacy-first trading automation and attestable AI operations.

---

## 1. Mission Snapshot

1. **Absolute Privacy:** Zcash shielded wallets fund every action, NEAR AI enclaves attest inference, and NEAR Intents delivers cross-chain legs without leaking intent.
2. **Human Command:** AI executes research protocols end-to-end but cannot deploy capital without signed approval that's logged to `.zkputer/SESSION_LOG.jsonl`.
3. **Protocol-as-Code:** Machine-readable rules in `protocols/core` and `protocols/ops` govern risk, compliance, and OPS-specific playbooks so any AI IDE can follow them deterministically.

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────┐
│          AI Pair-Programmer Runtime         │
│  (Cursor, Antigravity, Claude Desktop, …)   │
└──────────────────────────────┬──────────────┘
                               │ reads
                .zkputer/AGENT_BOOTSTRAP.md
                               │ loads
┌───────────────────────────────▼────────────────────────────┐
│                ZKputer Protocol Spine                      │
│  • protocols/core – master rules, risk JSON, compliance    │
│  • protocols/ops  – BaseOPS / ExtendOPS / HyperOPS / Pump │
│  • src/core/handbook.py – loader with audit hooks          │
│  • src/core/compliance.py – enforcement + schema checks    │
└──────────────┬─────────────────────────────────────────────┘
               │ executes authorized trades
┌──────────────▼──────────────┐     ┌─────────────────────────┐
│  Zcash Shielded Wallet      │────▶│    NEAR AI (TEE)        │
│  (zcashd RPC / Sapling)     │     │  Attested inference     │
└──────────────┬──────────────┘     └──────────────┬──────────┘
               │                                   │ intents
               ▼                                   ▼
          NEAR Intents ───────────────▶ Target venues (Base, Solana, Hyperliquid)
```

---

## 3. Privacy Stack (Non-Optional)

1. **Shielded Treasury:** `src/core/zcash_wallet.py` interfaces with `zcashd` so every funding leg originates from Sapling notes with no transparent leakage.
2. **Trusted Inference:** `src/core/near_ai_agent.py` signs each analytical cycle with NEAR AI attestation so judges can verify it ran inside NVIDIA H100 TEEs.
3. **Cross-Chain Intent Router:** `src/core/near_intents.py` publishes encrypted instructions to NEAR Intents, which fans out to Base, Solana, Hyperliquid, or any venue encoded in `ACTIVE_OPS.json`.
4. **Audit-Ready Logging:** `src/core/session_logger.py` appends every signal, approval, and execution outcome to `.zkputer/SESSION_LOG.jsonl` for forensics without exposing positions publicly.

---

## 4. Operating Flow for Pair-Programmers

1. **Unlock Workspace (Calculator Gate):** Run the disguised calculator app on the secure desktop; entering the correct six-digit PIN reveals the hidden ZKputer directory while maintaining a fully functional calculator UI for anyone else.
2. **Bootstrap:** AI opens `.zkputer/AGENT_BOOTSTRAP.md`, reads the mission brief, loads `ACTIVE_OPS.json`, and initializes the relevant OPS playbook.
3. **Daily Routine:** Follow `protocols/ops/<mode>.md` to harvest data (browser automation, WhaleIntel, GeckoTerminal, Padre, etc.), score setups, and log reasoning.
4. **Human Checkpoint:** AI presents signals with compliance reports; execution only proceeds after an explicit user approval command that is recorded.
5. **Execution & Settlement:** Approved trades travel through the Zcash → NEAR AI → NEAR Intents pathway, ensuring shielded funding, attested compute, and private cross-chain settlement.

---

## 5. Human Commands Reference

**The human has final say on all trades.** AI pair-programmers must wait for explicit commands before executing.

### Starting a Session
```
"Check my accounts"                    → Show balances across all exchanges
"Find me a trade setup"                → Analyze markets and propose a trade
"What's the market doing?"             → Get live prices and sentiment
"Show me my positions"                 → Display open positions and PnL
```

### Trade Approval
```
"Execute"                              → Place the proposed trade
"Execute on Extended"                  → Use Extended Exchange specifically
"Execute on Hyperliquid"               → Use Hyperliquid specifically
```

### Trade Modification
```
"Make it smaller"                      → Reduce position size
"Make it bigger"                       → Increase position size
"Tighter stop"                         → Move stop loss closer to entry
"Wider stop"                           → Move stop loss further from entry
"Change TP to $X"                      → Set specific take profit price
```

### Trade Rejection
```
"Cancel"                               → Abort the proposed trade
"No"                                   → Reject and wait for new instruction
"Show me ETH instead"                  → Request different asset analysis
```

### Position Management
```
"Close my SOL position"                → Exit specific position
"Add a stop loss at $X"                → Place stop loss order
"Move my stop to breakeven"            → Adjust existing stop loss
"Take profit on half"                  → Partial position exit
```

### Example Session Flow
```
╔══════════════════════════════════════════════════════════════╗
║  HUMAN: "Check my accounts and find me a good trade"        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  [✓] Extended    $500.00 equity    0 positions               ║
║  [✓] Hyperliquid $500.00 equity    0 positions               ║
║  [✓] Base        Connected         Ready                     ║
║                                                              ║
║  LIVE PRICES:  BTC $92,000  ETH $3,100  SOL $140             ║
║                                                              ║
║  ┌────────────────────────────────────────────────────────┐  ║
║  │  RECOMMENDED: LONG SOL @ $140.50                       │  ║
║  │  Stop Loss:   $136.29 (-3%)                            │  ║
║  │  Take Profit: $148.93 (+6%)                            │  ║
║  │  Size: 3.5 SOL ($492)  Risk: $14.74 (3%)               │  ║
║  └────────────────────────────────────────────────────────┘  ║
║                                                              ║
║  AWAITING COMMAND: Execute / Cancel / Modify                 ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║  HUMAN: "Execute"                                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  [✓] Order placed: LONG 3.5 SOL @ $140.50                    ║
║  [✓] Stop loss set: $136.29                                  ║
║  [✓] Logged to SESSION_LOG.jsonl                             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 6. OPS Modes (Single Source of Truth)

| Mode | Venue | Focus | Notes |
|------|-------|-------|-------|
| **ExtendOPS** | Extended Exchange perps | Thesis-driven, whale-aligned leverage | Volume floors, 20% max risk, screenshot verification |
| **HyperOPS** | Hyperliquid perps | Same thesis, different API surface | Funding skew + depth monitoring |
| **BaseOPS** | Base L2 | FDV < $4M, liquidity > $50K | LT_Score matrix + privacy-protected intel |
| **PumpOPS** | Solana (Pump.fun, Jupiter, Raydium) | High-speed token launches | Rug detection checklist + mandatory debrief |

All directives live inside `protocols/ops/` and are enforced by `ComplianceOfficer` against `protocols/core/RISK_LIMITS.json` and `COMPLIANCE_SCHEMA.json`.

---

## 7. Zypherpunk Track Coverage

| Hackathon Tier | Requirement (per zypherpunk.xyz) | ZKputer Capability |
|----------------|----------------------------------|--------------------|
| **Cross-Chain Privacy Solutions** | Build bridges / interoperability that carry Zcash privacy into other ecosystems | Shielded ZEC treasury + NEAR Intents router deliver private settlement onto Base, Solana, Hyperliquid with no gas pre-funding or address leakage. |
| **Private DeFi & Trading** | Create DeFi/trading tools leveraging Zcash privacy tech | OPS stack automates research, compliance, and execution of private swaps/perps, maintaining full audit trails while hiding strategy flow. |
| **Privacy-Preserving AI & Computation** | Combine privacy tech with AI/secure compute | AI pair-programmer runs inside NEAR AI TEEs with attested inference, translating human directives into shielded actions without exposing prompts or data. |

---

## 8. Demo & Validation

```bash
# 1. Configure environment
export ZCASH_RPC_USER="zcash"
export ZCASH_RPC_PASSWORD="<rpc-password>"
export NEAR_AI_API_KEY="<from https://cloud.near.ai>"

# 2. Run privacy-first demo (ExtendOPS)
python3 demo_near_ai.py  # initiates shielded funding mock + NEAR AI attested routine

# 3. Optional: launch air-gapped desktop for calculator gate workflow
docker-compose up --build -d
# Access the virtual desktop at http://localhost:6080 and start the calculator launcher.
```

Validation checklist:
- [ ] `.zkputer/SESSION_LOG.jsonl` shows boot, scans, approvals, executions.
- [ ] Compliance reports reference `protocols/core/COMPLIANCE_SCHEMA.json` fields.
- [ ] NEAR AI attestation attached to each execution cycle.
- [ ] ZEC funding txids remain shielded (view keys stored offline).

---

## 9. File Map

```
ZKputer/
├── .zkputer/
│   ├── AGENT_BOOTSTRAP.md   # READ THIS FIRST - mandatory entry brief
│   ├── ACTIVE_OPS.json      # current mode + account config
│   ├── SESSION_LOG.jsonl    # append-only audit log
│   └── hooks/               # execution hooks
│       ├── pre_trade.py     # validates trades before execution
│       └── post_trade.py    # logs results to audit trail
├── config/exchanges/        # LIVE CREDENTIALS (gitignored)
│   ├── extended.json        # Extended Exchange API keys
│   ├── hyperliquid.json     # Hyperliquid API keys
│   └── base.env             # Coinbase CDP credentials
├── protocols/
│   ├── core/
│   │   ├── API_EXECUTION.md # master playbook for trade execution
│   │   ├── MASTER_PROTOCOL.md
│   │   ├── RISK_LIMITS.json
│   │   └── COMPLIANCE_SCHEMA.json
│   └── ops/
│       ├── base.md
│       ├── extend.md
│       ├── hyper.md
│       └── pump.md
├── src/core/
│   ├── exchanges/           # unified trading clients
│   │   ├── extended_client.py
│   │   ├── hyperliquid_client.py
│   │   └── base_client.py
│   ├── handbook.py          # loader for the protocol spine
│   ├── compliance.py        # enforcement + schema validation
│   ├── session_logger.py    # audit channel writer
│   ├── zcash_wallet.py      # Sapling RPC client
│   └── near_intents.py      # cross-chain executor
├── demo_near_ai.py          # end-to-end routine demo
└── docker/                  # virtual desktop + calculator launcher
```

---

## 10. Communication Rules for Judges & Reviewers

- Never expose shielded addresses or viewing keys in plaintext logs. Demonstrations use mocked data unless the judge requests live funds.
- Calculator gate description is provided here, but the actual PIN is handed over verbally for on-site verification only.
- Audit everything: if a step fails, log the failure reason and remediation window before proceeding.

---

**Built for the Zypherpunk Hackathon — proving that private AI traders can be accountable without surrendering sovereignty.**
