# 📋 Protocol Compliance Checklist (Solana)

## Purpose
This document ensures quality control and prevents failures in the PumpOPS scanning and execution process.

---

## ⚠️ CRITICAL RULE: MANDATORY PumpOPS PROTOCOL EXECUTION

**YOU MUST EXECUTE EVERY SECTION OF `daily_OPS.md` PART A (Core Protocol) DURING PHASE 2 DEEP DIVE.**

This is **NON-NEGOTIABLE**.

### Required PumpOPS Sections (MUST EXECUTE ALL):
1. ✅ **KILL ZONE FILTER** - Liquidity >$5k (Pump) / $50k (Ray), Vol >$10k/5m.
2. ✅ **CONTRACT VERIFICATION** - Mint Auth REVOKED, Freeze Auth REVOKED (RugCheck/Solscan).
3. ✅ **DEV CHECK** - Did dev sell? Did they bundle? (Solscan/GMGN).
4. ✅ **HOLDER ANALYSIS** - Top 10 < 30%, no obvious clusters.
5. ✅ **SOCIAL CHECK** - Twitter/Telegram sentiment verification.

### Enforcement:
- **BEFORE** presenting a "Menu" to the user, verify ALL above sections completed.
- **FLAG** any tokens that failed Security checks with specific reasons (e.g., "Mint Auth Enabled").

---

## Phase 0: Pre-Scan Checklist

### Preparation
- [ ] Read `daily_OPS.md` Part A (Core Protocol)
- [ ] Review `SOLANA_SNIPER_STRATEGY.md`
- [ ] Check `narratives.md` for current meta (e.g., AI Agents, Dogs)
- [ ] Verify ZEC balance for funding (if trading enabled)

---

## Phase 1: Scan & Filter Compliance

### Primary Source Verification
- [ ] **Padre.gg accessed** - Checked Trenches/New Pairs
- [ ] **Pump.Fun accessed** - Checked King of the Hill / Bonding Curve
- [ ] **Screenshots captured** - Saved to research_logs for fallback
- [ ] **Manual review performed** - If automation failed

### Data Quality Standards
- [ ] **Liquidity verified** (> $5k Pump / > $50k Ray)
- [ ] **Volume verified** (> $10k in last 5 mins)
- [ ] **Age check** - Is it fresh? (< 24h usually)

### Automation Failure Protocol
**IF browser automation hits tool limits:**
1. [ ] **STOP** - Do not continue with failing approach
2. [ ] **CAPTURE** - Take simple screenshots of Padre.gg
3. [ ] **ANALYZE** - Manually review screenshots
4. [ ] **DOCUMENT** - Log failure in failure_logs/

---

## Phase 2: Deep Dive Compliance

### Security Verification (RugCheck / Solscan)
- [ ] **Mint Authority** - MUST be Revoked (or flagged High Risk)
- [ ] **Freeze Authority** - MUST be Revoked
- [ ] **LP Burned/Locked** - Verified 100%
- [ ] **Top 10 Holders** - < 30% total supply

### Dev & Bundle Analysis
- [ ] **Dev Wallet** - Check for "Dump" behavior (sold all in 1 tx)
- [ ] **Bundling** - Check Block 0 for >40% supply sniper (Jito bundles)

### Scoring Module Application
1. [ ] **Narrative/Memeability** (0-5)
2. [ ] **Community/Cult** (0-5)
3. [ ] **Dev History** (0-5)
4. [ ] **Smart Money Flow** (0-5)
5. [ ] **Distribution** (0-5)

---

## Phase 3: Documentation Compliance

### Daily Brief Requirements
- [ ] **Created in** `📖 Other Components/research_logs/YYYY-MM-DD/`
- [ ] **Template followed** - "The Menu" format
- [ ] **Padre.gg Links** included
- [ ] **Risk Level** clearly stated (Degen vs Graduated)

### Knowledge Graph Updates
- [ ] **tokens.md updated**
- [ ] **narratives.md updated**
- [ ] **playbook.md updated**

---

## Phase 4: Execution Compliance (If Authorized)

### Pre-Execution Checks
- [ ] **User Command Received** - "Execute trade 1"
- [ ] **ZEC -> SOL Bridge** - Verified liquidity/path
- [ ] **Slippage Set** - 10% (Pump) / 5% (Ray)

---

## Quality Assurance Checklist

### Data Source Priority
**Tier 1 (Primary):**
1. ✅ Padre.gg
2. ✅ Pump.Fun
3. ✅ RugCheck.xyz

**Tier 2 (Confirmation):**
4. ✅ Solscan
5. ✅ GMGN.ai
6. ✅ Twitter (Search $TICKER)

### Common Violations to Avoid
- ❌ **Trading Mint Auth Enabled tokens** (Instant Rug Risk)
- ❌ **Ignoring Dev Sales** (Dev dumping on you)
- ❌ **Fading Community** (Solana is 90% community/hype)

---

**Compliance is the difference between a Sniper and a Gambler.**

