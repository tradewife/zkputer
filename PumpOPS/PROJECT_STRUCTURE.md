# 📂 PumpOPS Project Structure

```
PumpOPS/
├── ⚙️ Configuration/
│   └── config/
│       ├── trading_config.json       # Solana & Jupiter settings
│       ├── scanning_config.json      # GeckoTerminal & Pump.fun settings
│       └── api_keys.json             # API keys (GitIgnored)
│
├── 📊 Core Trading System/
│   ├── solana_trade_executor.py      # Solana transaction execution
│   ├── jupiter_swap_module.py        # Jupiter Aggregator integration
│   ├── position_tracker.py           # Portfolio & PnL tracking
│   └── place_stops_tps.py            # Risk management
│
├── 📊 Core Research System/
│   └── (Research modules to be added)
│
├── 🧠 Learning Engine/
│   └── (AI models and learning logs)
│
├── 📚 Agent Handbook/
│   ├── AGENT_INSTRUCTIONS.md         # Core directives
│   └── daily_routine.md              # Operational checklist
│
├── 📖 Other Components/
│   ├── knowledge_graph/              # Market intelligence
│   └── research_logs/                # Daily briefs and analysis
│
├── venv_trading/                     # Python environment
├── README.md                         # Project overview
└── target_socials.md                 # List of tracked KOLs
```
