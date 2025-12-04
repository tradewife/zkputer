# ExtendOPS: Extended Exchange Trading System

**ExtendOPS** is a specialized, high-performance trading system designed exclusively for [Extended Exchange](https://app.extended.exchange). It features a modular architecture, automated execution capabilities, and an advanced learning engine to optimize trading performance.

## 📂 System Architecture

The workspace is organized into domain-specific modules for clarity and maintainability:

```
ExtendOPS/
├── 📂 core/                # The heart of the system
│   ├── executor.py         # Main execution logic & API interaction
│   ├── trading_client.py   # SDK wrapper & client management
│   └── utils/              # Utility scripts (e.g., price check)
│
├── 📂 operations/          # Daily routine & execution scripts
│   ├── execute_trades.py   # Primary script for trade execution
│   └── run_session.py      # Daily session runner
│
├── 📂 intelligence/        # Data & Learning
│   ├── learning_engine.py  # Self-optimizing trading logic
│   └── knowledge_manager.py # Knowledge Graph management
│
├── 📂 strategies/          # Trading strategies (Momentum, MeanRev, etc.)
│
├── 📂 docs/                # Documentation & Knowledge Base
│   ├── handbook/           # Agent instructions & protocols
│   ├── knowledge_graph/    # Persistent data (Performance, Narratives)
│   └── research_logs/      # Daily research notes
│
├── � config/              # Configuration files
│   └── trading_config.json # API keys & settings
│
└── 📂 archive/             # Legacy scripts & tests
```

## 🚀 Getting Started

### 1. Environment Setup
ExtendOPS comes with a setup script to manage the Python environment:

```bash
# Initialize/Activate environment
source setup_env.sh
```

### 2. Configuration
Ensure your API keys are set in `config/trading_config.json`:
```json
{
  "account_address": "0x...",
  "api_key": "...",
  "stark_public_key": "...",
  "stark_private_key": "...",
  "vault_number": 0,
  "testnet": false,
  "legacy_signing": false
}
```

### 3. Daily Routine
Run the daily routine to scan markets and prepare trades:
```bash
python3 operations/run_session.py
```

### 4. Trade Execution
Execute planned trades (manual or automated):
```bash
python3 operations/execute_trades.py
```

## 🧠 Intelligence Module
The **Learning Engine** (`intelligence/`) continuously analyzes trade performance to:
- Optimize setup parameters (Stop Loss, TP, Size).
- Detect market regimes (Trending, Ranging, Choppy).
- Update the **Knowledge Graph** (`docs/knowledge_graph/`) with new insights.

## 📚 Documentation
- **[Agent Handbook](docs/handbook/AGENT_INSTRUCTIONS.md):** Core operating protocols.
- **[Daily OPS](docs/handbook/daily_OPS.md):** Step-by-step daily routine.
- **[API Reference](core/EXTENDED_API_REFERENCE_UPDATED.md):** Extended API documentation.

---
*Built for the Extended Exchange Ecosystem.*
