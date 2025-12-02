# 🟣 PumpOPS: Solana Research & Sniping Command Center

**Welcome to the trenches.**

PumpOPS is not a bot. It is a **Workspace** designed for you to pair-program with an advanced AI Agent to dominate the Solana ecosystem (Pump.Fun, Raydium, Jupiter).

Instead of relying on black-box automation, PumpOPS leverages **Research-Driven Discovery** with institutional-grade risk management and optional execution at machine speed.

**The Engine:**
Under the hood, this workspace is powered by **ZKputer's Privacy Stack**:
-   **Funding:** Zcash (Shielded Pool)
-   **Execution:** Near Intents (Chain Abstraction)
-   **Result:** You trade on Solana without ever exposing your main wallet or IP.

---

## 🎯 The Mission

To dominate the Solana trenches by identifying and capitalizing on early-stage memecoins and high-momentum tokens using a **Collaborative Intelligence** approach.

We follow the **PumpOPS Protocol** (`daily_OPS.md`)—a strict set of rules for discovering alpha with systematic research and optional user-authorized sniping.

---

## 🛠 How to Use This Project

### 1. The Setup
Open this folder in an Agentic IDE (Cursor, Windsurf, or similar). The Agent will automatically detect `AGENT_INSTRUCTIONS.md` and understand its role as your **Institutional-Grade Solana Research Partner**.

### 2. The Workflow (Daily Research Routine)
This project uses a strict **Command-Response** workflow.

#### Step 1: Initialize
Start every session by commanding:
> *"Read Handbook"*

The Agent will read the `📚 Agent Handbook/` to load its instructions and protocols.

#### Step 2: Execute Routine
Choose your mode:

**Standard Daily Run**
> *"Run the Daily"*

Agent follows `daily_OPS.md` for systematic token discovery and analysis.

#### Step 3: Review Outputs
The Agent will generate a **Daily Research Brief** with high-conviction picks.

#### Step 4: Execute Trades (Optional)
**You must explicitly command:**
> *"Execute trade 1"* or *"Execute all trades"*

Trades are **never** executed automatically. You maintain complete control.

### 3. The Outputs
*   **Daily Research Briefs:** Comprehensive Solana analysis with actionable token picks
*   **Knowledge Graph:** A persistent database of research intelligence:
    *   `tokens.md`: All tracked tokens with full fundamentals analysis
    *   `narratives.md`: Sector themes and trend tracking
    *   `smart_money.md`: Elite wallet profiles and whale activity  
    *   `wallets.md`: Wallet discovery lists
    *   `playbook.md`: Proven setup library with success rates
    *   `performance_log.json`: Detailed P&L tracking (if trading enabled)
*   **Trade Analysis:** Deep dives into each entry for continuous improvement

---

## 📊 Workflow Overview


```
Phase 0: Review & Learn (10 mins)
└→ Check performance_log.md, narratives.md, playbook.md

Phase 1: The Radar (20 mins)
├→ Padre.gg (Trenches scan)
├→ Pump.Fun (King of the Hill)
└→ Twitter/X KOL tracking

Phase 2: The Filter (10 mins)
├→ Kill Zone check (Liq, Vol, Mcap)
├→ Security verification (RugCheck)
└→ Dev wallet analysis (Solscan)

Phase 3: The Presentation (5 mins)
├→ Construct "The Menu" (1-4 opportunities)
└→ Await user command

Phase 3.5: Execute Trades (Optional - On Command)
├→ User says "Execute trade 1"  
├→ Jupiter swap execution
└→ Track positions & P&L

Phase 4: Broadcast (On Command)
└→ Telegram/X posting (requires explicit user approval)
```


---

## 📂 Directory Structure

| File/Folder | Purpose |
| :--- | :--- |
| **`AGENT_INSTRUCTIONS.md`** | **The Brain.** The system prompt for the Research Agent role. |
| **`daily_OPS.md`** | **The Master Protocol.** Combined Core Protocol (Part A) and Daily Routine (Part B). |
| **`📊 Core Trading System/`** 🆕 | **The Executor.** CDP Trade API integration for optional spot trading. |
| **`🧠 Learning Engine/knowledge_graph/`** | **The Memory.** Persistent storage for research intelligence and performance. |
| **`📖 Other Components/research_logs/`** | **The Output.** Where daily briefs and analyses are saved. |
| **`⚙️ Configuration/`** | **The Settings.** Scanning parameters, API keys, trading config. |
| **`📖 Status/`** | **The Tracker.** Production status, roadmap, and known issues. |

---

## 💡 Philosophy

*   **Research-Driven Discovery:** Every pick backed by systematic fundamentals analysis
*   **Multi-Source Verification:** WhaleIntel + GeckoTerminal + Basescan cross-checks
*   **Dual Strategy:** Foundation (long-term) + Casino (high-risk) for balanced exposure
*   **Continuous Learning:** We track every pick, optimize criteria, adapt strategies
*   **User-Authorized Trading:** Agent **never** executes trades without your explicit command

**Key Parameters:**
- **Universe:** Solana tokens, FDV ≤ $500k (Pump.Fun/Raydium)
- **Liquidity Minimum:** $50k (Foundation), $20k (Casino)
- **Max Risk:** 20% per trade (if trading enabled)
- **Max Positions:** 3 simultaneous  
- **Execution:** Agent trades **only upon your explicit instruction**
- **Trading:** Optional spot trading via CDP Trade API (no leverage)

---

## 🚀 Getting Started

### 1. Research Mode (No Trading)
1. Command: `"Read Handbook"` to initialize agent
2. Command: `"Run the Daily"` to execute research routine
3. Review Daily Brief in `📖 Other Components/research_logs/`
4. Track picks in Knowledge Graph

### 2. Trading Mode (Optional)
1. **Setup CDP API Keys:**
   ```bash
   # 1. Get API keys from portal.cdp.coinbase.com
   # 2. Copy .env.example to .env  
   # 3. Add your CDP_API_KEY_ID and CDP_API_KEY_SECRET
   ```

2. **Fund Your Wallet:**
   - Transfer SOL to your Solana wallet (Private key in .env)
   - Minimum $50 recommended for testing

3. **Execute Research & Trading:**
   - Agent runs daily routine, generates picks
   - Agent prepares trades with quotes
   - **You review and command**: `"Execute trade 1"` or `"Execute all trades"`
   - Agent executes via CDP Trade API, tracks positions

4. **Monitor Performance:**
   - Check positions: `"Show positions"`  
   - P&L tracked in `performance_log.json`
   - Knowledge graph auto-updates

### Technical Details (Trading)
- **Platform:** Coinbase Developer Platform (CDP)
- **Trade API:** Sub-500ms execution, automatic DEX routing
- **Supported DEXs:** Jupiter (aggregates Raydium, Orca, etc.)
- **Gas Costs:** ~$0.50-2 per trade (Base L2)
- **Slippage Protection:** Default 1% (100 bps)

**For Detailed Setup:** See [`📊 Core Trading System/README.md`](📊%20Core%20Trading%20System/README.md)

---

## 🔒 Safety & Risk Management

### Hard Rules (Research)
- ❌ Never recommend <$50k liquidity (unless <1h old)
- ❌ Never exceed $4M FDV ceiling
- ❌ Always verify contracts on Basescan
- ❌ Always check for honeypot risks (taxes, locks)

### Hard Rules (Trading)
- ❌ Max 20% account balance per trade
- ❌ Max 3 positions simultaneously
- ❌ Never execute without user command
- ❌ Verify token contract before trading
- ❌ Minimum $50k liquidity required

### Quality Assurance
- **Protocol Compliance**: Mandatory checklist for every scan
- **Source Priority**: Tier 1-2-3 hierarchy strictly enforced (WhaleIntel → GeckoTerminal → others)
- **Failure Recovery**: Documented procedures for automation issues
- **Learning Loop:** Every mistake logged and prevented

---

## 📈 Performance Tracking

All picks are tracked in `performance_log.json` (trading) or `performance_log.md` (research-only) with:
- Entry/current FDV
- ROI calculation  
- Status (Active/Rugged/Mooned)
- Lessons learned

The system uses this data to optimize future selections through the learning loop.

---

## 🎉 What's New (v1.0.0 - 2025-11-26)

✨ **Complete restructure** based on HyperOPS best practices:
- Emoji-based directory organization  
- Unified `daily_OPS.md` (core protocol + routine)
- Enhanced agent instructions with command protocol
- Protocol compliance & source priority docs
- Configuration management system

🆕 **CDP Trading Integration:**
- Optional spot trading on Base via CDP Trade API
- User-authorized execution ("Execute trade 1")
- Position tracking & P&L monitoring
- Risk management (20% max, 3 positions)
- Automatic DEX routing (Jupiter Aggregator)

🐛 **Fixed 2025-11-26 scan failure:**
- Implemented screenshot fallback protocol
- Added automation failure recovery procedures
- Created comprehensive quality checklists

---

## 📞 Support

### Common Commands
- **"Read Handbook"** - Initialize agent with all protocols
- **"Run the Daily"** - Execute full daily research routine
- **"Deep Dive [TOKEN]"** - Focused analysis on specific token
- **"Execute trade 1"** 🆕 - Buy specific token (trading mode)
- **"Execute all trades"** 🆕 - Execute all prepared trades
- **"Show positions"** 🆕 - View current holdings
- **"Cancel pending trades"** 🆕 - Clear trade queue

### Troubleshooting
1. Check [`📖 Status/PRODUCTION_STATUS.md`](📖%20Status/PRODUCTION_STATUS.md) for known issues
2. Review `📖 Status/failure_logs/` for recent problems
3. Verify configuration in `⚙️ Configuration/config/`
4. Consult [`📚 Agent Handbook/PROTOCOL_COMPLIANCE.md`](📚%20Agent%20Handbook/PROTOCOL_COMPLIANCE.md) for quality standards

---

## 🔗 Key Links

- [WhaleIntel.ai](https://whaleintel.ai/) - Primary data source
- [GeckoTerminal (Base)](https://www.geckoterminal.com/base) - Pool analytics
- [Basescan](https://basescan.org/) - Contract verification
- [GMGN.ai (Base)](https://gmgn.ai/discover?chain=base) - Smart wallet tracking
- [CDP Portal](https://portal.cdp.coinbase.com/) - Trading API setup

---

## 📜 License & Disclaimer

**Not Financial Advice**: This system is for research purposes only. All outputs include "NFA/DYOR" disclaimers.

**Use Responsibly**: Always verify information independently. The agent can make mistakes.

**Trading Risk**: Spot trading involves risk of capital loss. Only trade with funds you can afford to lose.

---

**BaseOPS - Research with depth. Execute with discipline. Learn continuously.**
