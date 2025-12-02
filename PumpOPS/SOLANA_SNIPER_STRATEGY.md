# 🎯 Institutional-Grade Solana Sniper Strategy

## 1. 🧠 Philosophy: "The Sniper's Edge"
To win in the Solana trenches, we do not gamble. We **execute**. We trade probability, not hope. Our edge comes from speed, information asymmetry, and ruthless risk management.

## 2. ⚙️ Execution Settings (The "Kill Zone")

### ⚡ Transaction Parameters
*   **Slippage**:
    *   **Bonding Curve (Pump.Fun)**: `5% - 15%` (Standard), `20%` (High Volatility/KOL Pump).
    *   **Raydium (Post-Migration)**: `2% - 5%` (Stable), `10%` (Breakout).
*   **Priority Fees (Jito/MEV)**:
    *   **Standard**: `0.005 SOL`
    *   **Turbo (High Conviction)**: `0.01 SOL`
    *   **MEV Protection**: **ALWAYS ON** (via Jito bundles where possible).

### 🛡️ Safety Filters (The "Rug Screen")
*   **Liquidity**:
    *   **Pump.Fun**: > $5k (avoid dust).
    *   **Raydium**: > $50k (minimum for institutional entry).
*   **Holder Distribution**:
    *   **Top 10 Holders**: MUST be `< 30%` of supply.
    *   **Dev Wallet**: MUST have sold < 10% of supply (unless fully exited).
*   **Contract Security**:
    *   **Mint Authority**: **REVOKED** (Non-negotiable).
    *   **Freeze Authority**: **REVOKED** (Non-negotiable).
    *   **Socials**: Must have at least 1 active social link (Twitter/Telegram).

## 3. 📡 Signal Intelligence (The "Alpha")

### 🐋 Smart Money Tracking
*   **"The Insiders"**: Wallets that buy < 5 mins after launch and sell > 10x.
*   **"The Rotators"**: Wallets that consistently move profits from one runner to the next.
*   **Action**: Copy-trade wallets with > 60% win rate over 30 days.

### 🐦 Social Sentiment (The "Hype")
*   **KOL Tracking**: Monitor specific influencers (from `target_socials.md`).
*   **Volume/Mention Ratio**: High volume + Low mentions = **Insider Accumulation** (Bullish).
*   **Viral Check**:
    *   Twitter Search: `$TOKEN` (Latest).
    *   Look for organic memes, not just "shill" posts.

## 4. 🔫 The Setup: "The Bonding Curve Breakout"

### 🟢 Entry Triggers
1.  **The "90% Rule"**: Token reaches 90% bonding curve completion on Pump.Fun.
2.  **Volume Spike**: 5-minute volume > $10k.
3.  **Smart Money Inflow**: At least 2 "Smart Wallets" enter.

### 🔴 Exit Strategy (Ruthless Discipline)
*   **Initial Take Profit (TP1)**: Sell **50%** at **2x** (Risk Free).
*   **Secondary Take Profit (TP2)**: Sell **25%** at **5x**.
*   **Moonbag (TP3)**: Hold **25%** for **10x+** or migration to Raydium.
*   **Stop Loss (SL)**:
    *   **Hard Stop**: **-30%** from entry.
    *   **Time Stop**: If price doesn't move > 20% in 15 mins, **CUT IT**.

## 5. 🔄 The Loop (Daily Workflow)
1.  **Scan**: Padre.gg / Photon for new pairs matching filters.
2.  **Verify**: RugCheck.xyz + Holder Analysis.
3.  **Snipe**: Execute via `solana_trade_executor.py`.
4.  **Manage**: Set TP/SL immediately.
5.  **Log**: Record result in `performance_log.md`.
