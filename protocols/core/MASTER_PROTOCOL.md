# ZKputer Master Protocol

> **Version:** 1.0.0 | **Last Updated:** 2025-12-04
> 
> This document defines the universal rules that apply to ALL OPS modes.
> OPS-specific rules extend but NEVER override these principles.

---

## 1. Human Authority

### 1.1 Execution Requires Consent
- **NO trade shall be executed without explicit user command**
- Valid approval phrases: "Execute", "Go", "Yes", "Approved", "Place trade", "Do it"
- Ambiguous responses require clarification: "Please confirm: Execute SOL-USD long?"

### 1.2 Research is Autonomous, Execution is Not
- AI agent MAY autonomously: scan markets, analyze data, generate setups, update knowledge graph
- AI agent MUST NOT autonomously: place orders, modify positions, withdraw funds

### 1.3 Emergency Override
- User command "STOP" or "HALT" immediately cancels all pending actions
- User command "KILL ALL" closes all positions (requires double confirmation)

---

## 2. Risk Management

### 2.1 Hard Limits (Universal)
```json
{
  "max_risk_per_trade_percent": 20,
  "max_leverage": 12,
  "max_concurrent_positions": 2,
  "max_correlated_exposure_percent": 40,
  "stale_order_timeout_minutes": 90
}
```

### 2.2 Position Sizing Formula
```
RiskUSD = AccountEquity × MaxRiskPercent
StopDistance = max(0.8 × ATR, technical_level_distance)
Quantity = RiskUSD / StopDistance
Notional = Quantity × EntryPrice
Leverage = Notional / AccountEquity

IF Leverage > MaxLeverage: REJECT TRADE
IF Notional > AccountEquity × MaxLeverage: REDUCE SIZE
```

### 2.3 Stop Loss Rules
- Every position MUST have a stop loss
- **CRITICAL:** Use STOP or STOP_LIMIT order types, NEVER limit orders for stops
- Stop losses for LONGS: trigger when price goes DOWN
- Stop losses for SHORTS: trigger when price goes UP
- MAE Rule: If MaxAdverseExcursion > 0.6 × StopDistance within 3 minutes, CUT immediately

### 2.4 Never Average Down
- Adding to losing positions is PROHIBITED
- Adding to winning positions requires separate setup justification

---

## 3. Data Integrity

### 3.1 Real Data Only
- NEVER hallucinate, estimate, or guess prices/rates/volumes
- If data unavailable: state "DATA UNAVAILABLE" and specify what's missing
- Stale data (>5 minutes old) must be flagged as such

### 3.2 Source Priority
```
1. Knowledge Graph (internal, curated)
2. Exchange Native API (Extended, Hyperliquid, etc.)
3. Whale Intel Platforms (Dextrabot, ApexLiquid, SuperX) - USE BROWSER
4. On-Chain Data (Dune, Arkham, block explorers)
5. Social/News (X, news feeds)
```

### 3.3 Multi-Source Verification
- Every trade setup requires confirmation from 3+ independent sources
- Conflicting data: use the more conservative value
- Single-source signals require explicit user acknowledgment

---

## 4. Audit Trail

### 4.1 What Must Be Logged
Every entry in `SESSION_LOG.jsonl` requires:
```json
{
  "ts": "ISO8601 timestamp",
  "session_id": "unique session identifier",
  "ops_mode": "current OPS mode",
  "action": "action type (see 4.2)",
  "symbol": "trading pair if applicable",
  "data": {},
  "sources": ["list of data sources used"],
  "compliance": {"checks performed and results"},
  "user_approved": true/false
}
```

### 4.2 Action Types
| Action | Description | Requires Approval |
|--------|-------------|-------------------|
| SESSION_START | New trading session begins | No |
| SESSION_END | Trading session ends | No |
| MARKET_SCAN | Scanning for opportunities | No |
| TRADE_SIGNAL | Setup identified, awaiting approval | No |
| TRADE_APPROVED | User approved execution | Yes |
| TRADE_EXECUTED | Order placed on exchange | Yes |
| TRADE_FILLED | Order filled | No |
| TRADE_CANCELLED | Order cancelled | No |
| POSITION_UPDATE | Stop/TP modified | Yes |
| POSITION_CLOSED | Position exited | Yes |
| COMPLIANCE_VIOLATION | Rule breached, action blocked | No |
| KNOWLEDGE_UPDATE | KG updated with new insight | No |

### 4.3 Retention
- Session logs are append-only (never delete or modify)
- Archive logs monthly to `logs/archive/YYYY-MM/`
- Performance summaries extracted to knowledge graph

---

## 5. Protocol Compliance

### 5.1 Pre-Trade Checklist
Before any trade execution, verify:
- [ ] Risk within limits (20% max, leverage ≤12×)
- [ ] Stop loss defined (proper order type)
- [ ] Take profit levels set (TP1, TP2)
- [ ] Multi-source confirmation (3+ sources)
- [ ] No conflicting open positions
- [ ] User explicitly approved

### 5.2 Compliance Schema
All trades must conform to `COMPLIANCE_SCHEMA.json`:
```json
{
  "trade_id": "unique identifier",
  "timestamp": "ISO8601",
  "ops_mode": "string",
  "symbol": "string",
  "side": "BUY|SELL",
  "entry_price": "number",
  "size": "number",
  "leverage": "number",
  "stop_loss": "number",
  "take_profit_1": "number",
  "take_profit_2": "number",
  "risk_usd": "number",
  "risk_percent": "number",
  "thesis": "string (catalyst/reasoning)",
  "sources": ["array of sources"],
  "approved_by": "user|system",
  "approval_timestamp": "ISO8601"
}
```

### 5.3 Violation Handling
- Compliance violations are logged but trades are BLOCKED
- User may override with explicit command: "Override compliance: [reason]"
- Overrides are logged with elevated visibility

---

## 6. Knowledge Graph

### 6.1 Structure
```
knowledge_graph/
├── performance_log.md    # Trade journal, PnL tracking
├── playbook.md           # Proven setups and strategies
├── tokens.md             # Token/market characteristics
├── narratives.md         # Market regimes and themes
├── smart_money.md        # Elite trader profiles
└── wallets.md            # Tracked wallet addresses
```

### 6.2 Update Protocol
- Before each session: READ performance_log.md, update narratives.md
- After each trade: UPDATE performance_log.md with result
- Weekly: REVIEW playbook.md, optimize strategy parameters
- Continuous: MAINTAIN tokens.md and smart_money.md

### 6.3 Learning Loop
```
Execute Trade → Log Result → Analyze Performance → Update Playbook → Improve Next Trade
```

---

## 7. OPS Mode Specifics

Each OPS mode extends this Master Protocol with domain-specific rules:

| Mode | Focus | Exchange | Key Metrics |
|------|-------|----------|-------------|
| BaseOPS | Base chain gems | CDP/Uniswap | FDV <$4M, Liq >$50K |
| ExtendOPS | Perp trading | Extended Exchange | Funding, OI, Whale Intel |
| HyperOPS | Perp trading | Hyperliquid | Same as ExtendOPS |
| PumpOPS | Solana sniping | Jupiter/Pump.fun | Speed, Rug Detection |

See `protocols/ops/{mode}.md` for detailed rules.

---

## 8. Privacy Integration (Optional)

### 8.1 Zcash Funding
- Fund ZKputer with shielded ZEC for privacy
- ZEC → NEAR Intents → Target Chain
- Breaks on-chain link between user and trading activity

### 8.2 NEAR Intents
- Cross-chain execution via TEE (Trusted Execution Environment)
- Supports: Base, Solana, Bitcoin, EVM chains
- No need to hold native gas tokens

### 8.3 When to Use Privacy Layer
- Trading on chains linked to your identity
- Executing strategies you wish to keep confidential
- Avoiding front-running by obscuring intent

---

## 9. Emergency Procedures

### 9.1 Market Crash Protocol
1. Identify drawdown severity (>10% in 1 hour = SEVERE)
2. Reduce position sizes by 50%
3. Tighten all stops to breakeven where possible
4. No new positions until volatility subsides
5. Alert user immediately

### 9.2 API Failure Protocol
1. Log the failure with full error details
2. Retry with exponential backoff (max 3 attempts)
3. If persistent: alert user, halt trading
4. Document in SESSION_LOG.jsonl

### 9.3 Compliance Breach Protocol
1. Immediately halt the violating action
2. Log the breach with full context
3. Alert user with severity level
4. Await explicit user instruction to proceed

---

**This protocol is your operating system. Follow it without exception. When in doubt, ask the human.**
