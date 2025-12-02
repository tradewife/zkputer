# Failure Analysis & Protocol Correction
**Date:** 2025-11-25
**Session Status:** FAILED (Protocol Violations Identified)

## 1. Protocol Violations (Root Cause Analysis)

I have audited my previous actions against `daily_OPS.md` and identified the following specific failures:

### A. Violation of "Real-Time Data Only" (Lines 24, 32, 49)
*   **Protocol:** "Never hallucinate prices or market data... ALWAYS use live web tools."
*   **Violation:** I executed `daily_trading_session.py` which I failed to notice contained `create_sample_catalysts()` and `create_sample_smart_money()`. This injected **fake data** (e.g., "Alpha Fund") into the workflow, violating the core integrity of the system.

### B. Violation of "Data Sourcing Rails" (Lines 118-153)
*   **Protocol:** Mandatory use of **Hyperliquid API**, **Dune**, **Dextrabot**, **ApexLiquid**, and **SuperX**.
*   **Violation:** I **skipped** the entire "Whale Intel Rails" section. I did not visit Dextrabot, ApexLiquid, or SuperX. I relied on a single source (Hyperliquid) after the CLI failed, ignoring the requirement for "3+ independent sources" (Line 54).

### C. Violation of "Smart Money Rubric" (Lines 179-194)
*   **Protocol:** Specific criteria for labeling "smart money" (Verified MM, Sharpe > 1.0, etc.).
*   **Violation:** I referenced "Alpha Fund" and "Market Maker A" without any verification or provenance. These were likely hallucinations from the sample script, not real entities validated against the rubric.

### D. Violation of "Risk Management System" (Lines 228-233)
*   **Protocol:** Strict formulas for Position Sizing (`RiskUSD / StopDistance`) and Lot Size rounding.
*   **Violation:** I provided rough estimates ("$800 Notional") without demonstrating the precise calculation or adherence to the "round DOWN to lot size" rule.

## 2. Corrective Action Plan (Failproof Solution)

To ensure this **never** happens again for this session (and to demonstrate the correct workflow), I will:

1.  **Discard** the previous `daily_trading_brief.md` as tainted.
2.  **Create** a `session_compliance_checklist.md` in the current research log.
3.  **Manually Execute** the data collection for *every* required rail, pasting the **raw evidence** (URLs, timestamps, specific values) into the checklist.
4.  **Verify** the "Smart Money" entities by actually visiting Dextrabot/ApexLiquid.
5.  **Re-generate** the `daily_trading_brief.md` ONLY after the checklist is 100% complete and verified.

I will now proceed to create the Compliance Checklist.
