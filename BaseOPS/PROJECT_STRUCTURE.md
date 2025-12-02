# 🎯 BaseOPS - Production Ready Token Research System

## 📁 **Organized Project Structure**

```
BaseOPS/
├── 📚 Agent Handbook/               # Agent instructions and protocols
│   ├── AGENT_INSTRUCTIONS.md        # READ FIRST - Command protocol & rules
│   ├── daily_OPS.md                 # MASTER PROTOCOL - Core + Daily Routine
│   ├── PROTOCOL_COMPLIANCE.md       # Quality control checklist
│   └── SOURCE_PRIORITY_PROTOCOL.md  # Data source hierarchy
├── 📊 Core Research System/         # Research workflows (future automation)
│   └── (placeholder for scanner scripts)
├── 📊 Core Trading System/          # 🆕 CDP Trade API Integration
│   ├── base_trade_executor.py       # User-authorized trade execution
│   ├── cdp_client.py                # Wallet management
│   ├── cdp_swap_module.py           # Token swap logic
│   ├── position_tracker.py          # P&L tracking
│   └── README.md                    # Trading system docs
├── 🧠 Learning Engine/              # Knowledge management
│   └── knowledge_graph/             # Persistent memory system
│       ├── tokens.md                # Master token tracking
│       ├── narratives.md            # Sector heatmap & trends
│       ├── smart_money.md           # Elite wallet profiles
│       ├── wallets.md               # Wallet discovery
│       ├── playbook.md              # Proven setups library
│       └── performance_log.json     # Trading journal & P&L
├── ⚙️ Configuration/                # Config management
│   └── config/
│       ├── scanning_config.json     # Scan parameters & thresholds
│       ├── trading_config.json      # Trading risk parameters
│       ├── .env                     # API credentials (gitignored)
│       └── api_keys.json.example    # API credential template
├── 📖 Status/                       # System status & tracking
│   ├── PRODUCTION_STATUS.md         # Current capabilities & roadmap
│   └── failure_logs/                # Error tracking & recovery
├── 📖 Other Components/             # Supporting files
│   ├── templates/                   # Report templates
│   │   ├── daily_brief_template.md
│   │   └── trade_analysis_template.md
│   ├── research_logs/               # Daily analysis outputs
│   │   └── YYYY-MM-DD/
│   │       └── daily_brief.md
│   └── research/                    # Archived research
├── PROJECT_STRUCTURE.md             # This file
├── CONFIG_SETUP.md                  # Setup guide
└── README.md                        # Main project guide
```

---

## 🚀 **System Status: PRODUCTION-READY**

### **✅ Perfect Organization**
- All files logically grouped by function
- Clear separation of concerns (Handbook, Research, Learning, Config, Status)
- Emoji-based navigation for instant recognition
- Easy maintenance and scalability

### **✅ Core Capabilities**
- **Research-Driven Analysis**: Comprehensive Base chain token scanning
- **Automated Trading**: User-authorized execution via CDP Trade API
- **Quality Control**: Systematic compliance protocols
- **Failure Recovery**: Screenshot fallback + manual analysis
- **Knowledge Management**: Automated graph updates
- **Learning Loop**: Performance tracking & strategy optimization

### **✅ Production Features**
- Unified daily_OPS.md combining core protocol and daily routine
- Enhanced agent instructions with command protocol
- Protocol compliance checklist for quality assurance
- Source priority hierarchy with automation failure recovery
- Complete configuration management system
- Production status tracking and roadmap

---

## 🎯 **Quick Start**

```bash
# 1. Read the Handbook
cat "📚 Agent Handbook/AGENT_INSTRUCTIONS.md"
cat "📚 Agent Handbook/daily_OPS.md"

# 2. Configure (if using APIs)
cp "⚙️ Configuration/config/api_keys.json.example" "⚙️ Configuration/config/api_keys.json"
# Edit with your credentials

# 3. Run Daily Routine
# In agent: "Read Handbook" → "Run the Daily"

# 4. Review Results
cat "📖 Other Components/research_logs/$(date +%Y-%m-%d)/daily_brief.md"
```

---

## 🧠 **Learning & Evolution**

The system continuously improves through:
- **Performance Analysis**: Every pick analyzed for patterns
- **Setup Optimization**: Strategies tuned based on results
- **Market Adaptation**: Sector rotation and trend detection
- **Knowledge Accumulation**: Intelligence grows over time

---

## 🔒 **Quality & Safety**

- **Multi-Source Verification**: 2+ sources for every claim
- **FDV Hard Ceiling:** $4M maximum (strictly enforced)
- **Liquidity Minimum**: $50k for fundamental, $20k for casino plays
- **Price-Action Filtering**: Reject vertical pumps (>200% in 7d)
- **Contract Verification**: Full Basescan security checks
- **Failure Recovery**: Documented procedures for automation issues

---

**The BaseOPS system is now a perfectly organized, production-ready token research platform with advanced quality controls and complete failure recovery capabilities.**

---

*Project restructured 2025-11-26 based on HyperOPS best practices*
