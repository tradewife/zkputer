# ZKputer: Privacy-Preserving AI Trading Infrastructure

**Institutional-grade AI trading system combining collaborative intelligence with cryptographic privacy**

Built on Zcash shielded transactions, NEAR AI trusted execution, and NEAR Intents cross-chain protocol. Implements a **pair-programming model** where AI handles research execution and privacy logistics while humans maintain strategic control and risk authorization.

**Hackathon:** Zypherpunk 2025 | **Tracks:** Cross-Chain Privacy ($20k) + Privacy-Preserving AI ($25k)

## What Makes This Different

### Collaborative Intelligence, Not Black Box Autonomy

**The AI handles:**
- Multi-platform data aggregation (WhaleIntel, GeckoTerminal, Padre.gg via browser)
- Pattern recognition across persistent knowledge graph (6 specialized modules)
- Privacy-preserving execution routing (Zcash → NEAR AI → NEAR Intents)
- Documentation and audit trail generation

**Humans control:**
- Strategic direction and opportunity prioritization
- Risk authorization (all trades require explicit approval)
- Compliance oversight and quality assurance
- Communication and disclosure decisions

### Institutional Research Protocols

Each strategy module (PumpOPS, BaseOPS, HyperOPS) implements systematic due diligence:

- **Multi-source verification** with documented fallbacks
- **Browser-based research** for authentic data (screenshot audit trails)
- **On-chain validation** via block explorer verification
- **Social sentiment checks** (X/Twitter, Telegram)
- **Provenance documentation** for all claims

### Knowledge Graph Learning System

Persistent memory enabling continuous improvement:

- `tokens.md` - Historical performance with win/loss attribution
- `narratives.md` - Sector trends and regime identification  
- `smart_money.md` - Wallet profiling and behavior patterns
- `playbook.md` - Setup library with documented outcomes
- `performance_log.md` - Trade journal and attribution

Pre-scan review → Pattern extraction → Execution → Feedback loop

### Built-In Compliance Framework

**Execution gates:** Explicit authorization required for all capital deployment  
**Risk limits:** Module-specific position sizing and liquidity thresholds  
**Quality standards:** Multi-source verification, failure documentation, audit trails  
**Authorization protocol:** Command-based execution preventing unauthorized trades

## Privacy Stack

```
Zcash Shielded → NEAR AI TEE → NEAR Intents → Multi-Chain Settlement
```

**Zcash:** Zero-knowledge funding layer (no on-chain linkage)  
**NEAR AI:** Hardware-attested inference (NVIDIA H100 TEEs)  
**NEAR Intents:** Cross-chain privacy-preserving execution  

### Cypherpunk Access Control

**Disguised calculator interface** - ZKputer directory hidden behind functional calculator GUI:

```bash
# Launch calculator (looks like normal calculator app)
python3 zkputer_calculator.py

# Enter secret code: 3-1-4-1-5-9 (π digits)
# Toggles ZKputer ↔ .ZKputer (visible/hidden)
```

Privacy by design: Directory access requires secret knowledge, no obvious security UI.  

## Technical Implementation

### Core Components

```python
# src/core/zcash_wallet.py - Zcashd RPC integration
class ZcashRPCClient:
    """Mainnet-ready shielded transactions"""

# src/core/near_ai_agent.py - NEAR AI Cloud wrapper  
class NEARAIAgent:
    """TEE inference with attestation verification"""

# src/core/near_intents.py - Official 1Click API
class NearIntentsClient:
    """Cross-chain swap execution"""
```

### Strategy Modules

**PumpOPS (Solana):** Memecoin analysis via Padre.gg KOL tracking  
**BaseOPS (Base):** <$4M FDV gems with 9-module scoring  
**HyperOPS (Hyperliquid):** Perps with funding rate analysis

Each includes agent handbook, knowledge graph, compliance checklists, privacy integration.

## Quick Start

```bash
# Setup
export NEAR_AI_API_KEY="<from https://cloud.near.ai>"
export ZCASH_RPC_USER="zcash"
export ZCASH_RPC_PASSWORD="<password>"

# Run demo
python3 demo_near_ai.py

# Or launch virtual desktop
docker-compose up --build -d
# Access: http://localhost:6080
```

## Hackathon Compliance

### Cross-Chain Privacy ($20k)

✅ NEAR Intents 1Click API integration  
✅ Zcash shielded transactions (partial support)  
✅ Privacy-preserving cross-chain to Solana/Base  

### Privacy-Preserving AI ($25k)

✅ NEAR AI Cloud (NVIDIA H100 TEEs)  
✅ Hardware attestation verification  
✅ Natural language trading interface  

## Project Structure

```
ZKputer/
├── src/core/              # Privacy stack integration
│   ├── zcash_wallet.py
│   ├── near_ai_agent.py
│   └── near_intents.py
├── PumpOPS/               # Solana strategy + knowledge graph
├── BaseOPS/               # Base strategy + knowledge graph
├── HyperOPS/              # Hyperliquid strategy + knowledge graph
└── docker/                # Virtual desktop environment
```

## Documentation

- `ZCASH_WALLET_SETUP.md` - Installation guide
- `hackathon_audit.md` - Compliance verification
- `implementation_plan.md` - Technical architecture
- `near_ai_walkthrough.md` - Integration details

---

**Built for Zypherpunk Hackathon 2025**  
*Privacy-First Collaborative Intelligence for DeFi*
