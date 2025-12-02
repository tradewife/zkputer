# Session Compliance Checklist (2025-11-25)

**Objective:** Enforce strict adherence to `daily_OPS.md` protocols by mandating raw evidence collection for every data rail.

## 1. Market Data Rails (Hyperliquid API/Web)
*Protocol: Section 120-126*
- [x] **BTC-USD Price:** $88,669 (Source: `hyperliquid.xyz`)
- [x] **BTC Funding Rate:** -0.0028% (Source: `hyperliquid.xyz`)
- [x] **ETH-USD Price:** $2,956.3 (Source: `hyperliquid.xyz`)
- [x] **ETH Funding Rate:** 0.0070% (Source: `hyperliquid.xyz`)
- [x] **Open Interest Trend:** Rising (Source: `hyperliquid.xyz` inferred from volume)

## 2. Whale Intel Rails (Dextrabot/ApexLiquid)
*Protocol: Section 132-153*
- [x] **Dextrabot Large Prints:** 
  - ETH Long 5X $1.20M (0x8ae...3d60, 22m ago)
  - SOL Long 5X $1.39M (0x8ae...3d60, 22m ago)
- [x] **Smart Money Activity:** Trader `0x9eec...daab`
- [x] **Wallet Label:** High PnL ($26.7M ALL PNL, 239% ROE) (Source: `apexliquid.bot`)

## 3. Catalyst Rails (X/Twitter)
*Protocol: Section 154-166*
- [x] **Sentiment Check:** Mixed (Greed 68, but Bearish undertones) (Source: `x.com` search "crypto market")
- [x] **Specific Catalyst:** "Bitcoin dips below key cost-basis level" (Source: Santiment)
- [x] **Verification:** `https://x.com/santimentfeed`

## 4. Risk Management Calculation
*Protocol: Section 228-233*
- [x] **Account Equity:** $100.00
- [x] **Max Risk (20%):** $20.00
- [ ] **Setup 1 Stop Distance:** [Calculate: Entry - Stop]
- [ ] **Setup 1 Position Size:** [Calculate: $20 / StopDistance]
- [ ] **Setup 1 Lot Size Rounding:** [Show rounding logic]

## 5. Output Verification
*Protocol: Section 72*
- [ ] **Order Followed?** [Snapshot -> Evidence -> On-Chain -> Playbook -> Trades -> X Post]
- [ ] **Provenance Included?** [All data points cited?]

---
**Status:** PENDING VERIFICATION
**Agent Signature:** [Antigravity]
