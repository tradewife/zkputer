# HyperOPS — Arena Elite Model Tracking Protocol
**Version:** 2025-11-30 (Elite Model Strategy)
**Objective:** Identify and track high-performing AI models on the Chronoeffector Arena to serve as "Smart Money" signals for HyperOPS trading.

---

## Part A: Core Philosophy

Instead of relying on the "consensus" of the crowd (which may be wrong), we focus on **Elite Model Discovery**. We treat top-performing AI models exactly like we treat whale wallets or leaderboard traders: as sources of high-quality alpha.

**The Edge:**
- **Performance Proven:** We only follow models with verified high Sharpe (>2.0) and consistent returns.
- **Regime Specific:** We look for models that perform well in the current market conditions.
- **Signal, Not Noise:** We ignore the noise of the average model and focus on the signal from the best.

---

## Part B: Elite Model Criteria

A model qualifies as an "Elite Model" if it meets **at least 2** of the following criteria:

1.  **Sharpe Ratio > 2.0:** Indicates high risk-adjusted returns.
2.  **Win Rate > 60%:** Consistent accuracy.
3.  **Max Drawdown < 10%:** Strong risk management.
4.  **Top 10 Leaderboard:** Currently ranked in the top 10 by PnL.

---

## Part C: Integration Workflow

### 1. Discovery (Weekly/Daily)
- **Visit:** https://arena.chronoeffector.ai
- **Scan:** Check the Leaderboard for new top performers.
- **Verify:** Click into model details. Check their equity curve and recent trade history.
- **Record:** Add qualifying models to `knowledge_graph/smart_money.md` with the tag `[ARENA-MODEL]`.

### 2. Monitoring (Real-Time)
- **Watch:** Monitor the trades of identified Elite Models.
- **Correlate:** If an Elite Model enters a trade that aligns with our technical setup, treat it as a **High Confidence Confirmation**.
- **Contrarian:** If multiple Elite Models are positioned against the crowd, pay attention.

### 3. Execution
- **Confirmation:** Use Elite Model trades to validate your own thesis.
- **Sizing:** If an Elite Model aligns with your setup, consider it a "Smart Money" confirmation (validating 20% risk allocation).
- **NO BLIND COPYING:** Never copy a trade solely because a model took it. It must align with your own technical analysis and risk rules.

---

## Part D: Data & Browser Usage

- **Manual Review:** Use the browser to periodically check the Arena leaderboard.
- **Screenshots:** Capture performance charts of new Elite Models for the research logs.
- **No Automation:** We do not use automated scrapers or oracles. We use human-in-the-loop analysis to verify model quality.

---

## Part E: Example Knowledge Graph Entry

```markdown
### [ARENA-MODEL] Claude-3-Opus-Alpha
- **Status:** Active / Elite
- **Sharpe:** 2.45
- **Win Rate:** 68%
- **Style:** Mean Reversion / Scalp
- **Bias:** Currently Long ETH
- **Notes:** Very accurate on 15m timeframe reversals.
```
