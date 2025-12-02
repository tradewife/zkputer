# 📋 Protocol Compliance Checklist

## Purpose
This document ensures quality control and prevents failures like the 2025-11-26 scan where browser automation hitting limits led to incorrect "no opportunities" conclusion.

---

## ⚠️ CRITICAL RULE: MANDATORY BaseOPS PROTOCOL EXECUTION

**YOU MUST EXECUTE EVERY SECTION OF `daily_OPS.md` PART A (Core Protocol) DURING PHASE 2 DEEP DIVE.**

This is **NON-NEGOTIABLE**. The user has specifically flagged that agents have been skipping the systematic execution of BaseOPS instructions in previous runs. This MUST NOT happen.

### Required BaseOPS Sections (MUST EXECUTE ALL):
1. ✅ **MCAP & PRICE-ACTION FILTER** - Classify every candidate: [NEW & UNDERVALUED], [EARLY UPTREND], or [REJECT - ALREADY PUMPED]
2. ✅ **VERIFICATION & ADDRESS** - Full 42-char CA, Basescan verification, clone check
3. ✅ **FUNDAMENTALS MODULES (0-5)** - Score ALL 9 modules for EVERY Deep Dive candidate
4. ✅ **HOLD-INCENTIVE INDEX (0-5)** - Evaluate burn/staking/utility mechanisms
5. ✅ **SECURITY & RISK GATING** - Check ALL 6 block conditions, MANDATORY Basescan checks
6. ✅ **LONG-TERM SCORE** - Calculate FundamentalsCore, BaseScore, Risk Deduction, LT_Score

### Enforcement:
- **BEFORE** publishing daily brief, verify ALL above sections completed for each Deep Dive token
- **DOCUMENT** scores explicitlyin brief (not just narrative)
- **FLAG** any tokens that failed Security & Risk Gating with specific block reasons

---

## Phase 0: Pre-Scan Checklist

### Preparation
- [ ] Read `daily_OPS.md` Part A (Core Protocol)
- [ ] Review `performance_log.md` for past learnings
- [ ] Check `narratives.md` for current sector strength
- [ ] Select active setup from `playbook.md`
- [ ] Verify account equity and position limits

---

## Phase 1: Scan & Filter Compliance

### Primary Source Verification
- [ ] **WhaleIntel.ai accessed** - Checked Overview/Virtuals section
- [ ] **GeckoTerminal accessed** - Checked new pools on Base
- [ ] **Screenshots captured** - Saved to research_logs for fallback
- [ ] **Manual review performed** - If automation failed

### Data Quality Standards
- [ ] **FDV verified from 2+ sources** (WhaleIntel + GeckoTerminal)
- [ ] **Liquidity ≥$50k confirmed** for all candidates
- [ ] **Volume ≥$50k (24h) confirmed** for fundamental picks
- [ ] **Price charts reviewed** - State classification applied

### Automation Failure Protocol
**IF browser automation hits tool limits:**
1. [ ] **STOP** - Do not continue with failing approach
2. [ ] **CAPTURE** - Take simple screenshots of data tables
3. [ ] **ANALYZE** - Manually review screenshots for candidates
4. [ ] **DOCUMENT** - Log the failure and recovery in failure_logs/
5. [ ] **PROCEED** - Continue with manual-verified candidates

**NEVER conclude "no opportunities" without:**
- [ ] Manual review of all captured screenshots
- [ ] Cross-referencing at least 2 data sources
- [ ] Expanding search parameters if initial scan thin

### Candidate Identification
- [ ] **Minimum 3-5 candidates** identified (or documented why fewer)
- [ ] **FDV range verified** - All within $200k-$4M
- [ ] **Price-action filter applied** - Rejected vertical pumps (>200% in 7d)
- [ ] **Mix strategy** - 1-2 Fundamental + 1-2 High-Risk

---

## Phase 2: Deep Dive Compliance

### Contract Verification (Basescan)
- [ ] **Full 42-char address** obtained
- [ ] **Contract verified** - No proxy risks, mint functions checked
- [ ] **Tax/fee analysis** - Taxes <5% or documented
- [ ] **LP lock verified** - Locker address and duration noted
- [ ] **Holder distribution** - No single wallet >5% (excl. contracts)

### Tokenomics Analysis
- [ ] **Deflation mechanism** - Burn/buyback identified or marked N/A
- [ ] **Yield mechanism** - Staking/rewards identified or marked N/A
- [ ] **Real utility** - Use case beyond speculation documented
- [ ] **Supply dynamics** - Total vs circulating supply noted
- [ ] **Emission schedule** - Vesting/unlock timeline checked

### Scoring Module Application (All 9 Required)
1. [ ] **Product/Innovation** (0-5) - Real product existence verified
2. [ ] **Traction Quality** (0-5) - Usage metrics documented
3. [ ] **Tokenomics** (0-5) - Burn/yield/utility scored
4. [ ] **Liquidity Health** (0-5) - LP depth and lock assessed
5. [ ] **Governance/Control** (0-5) - Decentralization level noted
6. [ ] **Distribution & Community** (0-5) - Holder diversity checked
7. [ ] **Website/UX & Docs** (0-5) - Professionalism evaluated
8. [ ] **Runway/Funding** (0-5) - Grants/accelerators documented
9. [ ] **Price-Action** (0-5) - Chart structure classified

### LT_Score Calculation
- [ ] **FundamentalsCore** = avg(Modules 1-8) / 5
- [ ] **PriceActionFactor** = Module 9 / 5
- [ ] **Risk Deduction** calculated (Security, Distribution, Liquidity, Team)
- [ ] **LT_Score** = BaseScore × (1 - RiskDeduction)
- [ ] **Confidence level** assigned (ULTRA/HIGH/MED/LOW)

### Social Verification
- [ ] **X/Twitter reviewed** - Dev activity and community vibes
- [ ] **Project website visited** - Product documentation checked
- [ ] **GitHub activity** (if applicable) - Recent commits verified
- [ ] **Community sentiment** assessed - Hype vs quality differentiated

---

## Phase 3: Documentation Compliance

### Daily Brief Requirements
- [ ] **Created in** `📖 Other Components/research_logs/YYYY-MM-DD/`
- [ ] **Template followed** - All sections completed
- [ ] **Telegram Snippet** included at top
- [ ] **Provenance documented** - All sources cited
- [ ] **Screenshots embedded** - If UI changes demonstrated

### Knowledge Graph Updates
- [ ] **tokens.md updated** - New tokens added with full details
- [ ] **narratives.md updated** - Sector strength and catalysts
- [ ] **playbook.md updated** - Setup performance noted
- [ ] **performance_log.md updated** - Trades and learnings logged
- [ ] **smart_money.md updated** (if applicable) - New whales documented

### Failure Documentation (If Applicable)
- [ ] **failure_log.md created** in `📖 Status/failure_logs/`
- [ ] **Root cause identified** - What went wrong
- [ ] **Resolution documented** - How it was fixed
- [ ] **Prevention plan** - How to avoid in future
- [ ] **Lessons learned** - Key takeaways for improvement

---

## Phase 4: Broadcast Compliance

### Pre-Broadcast Checks
- [ ] **User permission requested** - Explicit "Ready to broadcast?" asked
- [ ] **User confirmation received** - Wait for "Yes" or "Go ahead"
- [ ] **Message reviewed** - Telegram snippet checked for accuracy
- [ ] **Disclaimer included** - "Not financial advice" present

### Post-Broadcast Verification
- [ ] **Message posted successfully**
- [ ] **Appearance confirmed** - Verified in channel
- [ ] **Format correct** - No broken links or formatting issues

---

## Quality Assurance Checklist

### Data Source Priority (Must Follow)
**Tier 1 (Primary - MUST USE):**
1. ✅ WhaleIntel.ai
2. ✅ GeckoTerminal

**Tier 2 (Confirmation):**
3. ✅ Basescan
4. ✅ Project Website
5. ✅ X/Twitter

**Tier 3 (Fallback - Only if Tier 1-2 fail):**
6. ⚠️ Web Search
7. ⚠️ General Knowledge (flagged as low confidence)

### Common Violations to Avoid
- ❌ **Browser automation persistence** - Continuing after hitting limits
- ❌ **Premature conclusions** - "No opportunities" without manual review
- ❌ **Missing provenance** - Claims without source citations
- ❌ **Incomplete scoring** - Skipping any of the 9 modules
- ❌ **Path errors** - Using old directory paths
- ❌ **Lazy research** - Not checking Basescan for contracts

---

## Success Criteria

### Minimum Acceptable Standards
- **≥80%** of checklist items completed per phase
- **100%** of Tier 1 sources checked before Tier 3 fallback
- **100%** of candidates have full contract verification
- **100%** of scoring modules applied to all Deep Dive candidates

### Excellence Standards
- **≥95%** of checklist items completed
- **≥3** candidates identified and analyzed
- **≥2** independent source confirmations per claim
- **Zero** premature conclusions or lazy research instances

---

## Continuous Improvement

### After Each Scan
1. Review this checklist
2. Note any violations or near-misses
3. Update playbook with learnings
4. Refine process for next scan

### Weekly Review
- Count checklist compliance rate
- Identify most common violations
- Update protocols to prevent repeat issues
- Celebrate improvements and wins

---

**Compliance is not bureaucracy - it's the foundation of quality research.**
