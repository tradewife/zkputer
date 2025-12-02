# 🎯 Source Priority Protocol

## Purpose
This protocol defines the hierarchy of data sources and fallback procedures to ensure accurate research and prevent automation failures like the 2025-11-26 incident.

---

## Data Source Hierarchy

### Tier 1: Primary Sources (MUST USE FIRST)

#### 1. WhaleIntel.ai (https://whaleintel.ai/)
**Use For:**
- Token FDV, market cap, price
- Liquidity and volume metrics
- Holder distribution and whale activity
- Virtuals Protocol integration data

**Access Method:**
- Browser navigation to specific sections
- Screenshot capture for fallback
- Manual extraction if automation fails

**Quality Standard:**
- ✅ Real-time data (<5 minutes old)
- ✅ Direct from platform API
- ✅ Cross-referenced with Tier 2

#### 2. GeckoTerminal (https://www.geckoterminal.com/base)
**Use For:**
- Pool-level liquidity and volume confirmation
- Price charts and technical analysis
- New pool discovery
- Contract address verification

**Access Method:**
- Direct pool page navigation
- Filter-based searches
- Screenshot capture for analysis

**Quality Standard:**
- ✅ Independent confirmation of WhaleIntel data
- ✅ Visual chart analysis for price action
- ✅ Pool age and liquidity depth verification

---

### Tier 2: Confirmation Sources (REQUIRED FOR DEEP DIVE)

#### 3. Basescan (https://basescan.org/)
**Use For:**
- Contract address verification (full 42 chars)
- LP lock status and locker address
- Top holder analysis
- Tax/fee configuration
- Proxy and mint function detection

**Access Method:**
- Direct contract address lookup
- Token holder page review
- Transaction history analysis

**Quality Standard:**
- ✅ Full contract verification completed
- ✅ Security risks documented
- ✅ LP lock confirmed or flagged

#### 4. Project Official Website
**Use For:**
- Product documentation
- Team information
- Roadmap and milestones
- Official announcements

**Access Method:**
- Direct website navigation
- Documentation review
- Link verification from token pages

**Quality Standard:**
- ✅ Website professional and functional
- ✅ Documentation clear and detailed
- ✅ Roadmap realistic and specific

#### 5. X (Twitter) / Social Media
**Use For:**
- Development activity updates
- Community sentiment
- Influencer mentions
- Project announcements

**Access Method:**
- Search for project handle
- Review recent posts
- Community engagement assessment

**Quality Standard:**
- ✅ Recent activity (<7 days)
- ✅ Authentic engagement (not bot driven)
- ✅ Developer communication present

---

### Tier 3: Fallback Sources (ONLY IF TIER 1-2 UNAVAILABLE)

#### 6. DexScreener
**Use For:**
- Additional price/volume confirmation
- Alternative liquidity data
- Supplementary chart analysis

**When To Use:**
- WhaleIntel data unavailable
- GeckoTerminal missing specific pool
- Need third-party confirmation

**Quality Standard:**
- ⚠️ Flag as secondary source
- ⚠️ Document why Tier 1-2 failed
- ⚠️ Lower confidence weight

#### 7. Web Search (General)
**Use For:**
- Project background research
- Team verification
- News and announcements

**When To Use:**
- Specific information not on primary sources
- Historical context needed
- Supplementary research only

**Quality Standard:**
- ⚠️ Must cite specific sources
- ⚠️ Cross-reference with other tiers
- ⚠️ Flag as lowest confidence

#### 8. Internal Knowledge / Memory
**Use For:**
- General crypto concepts
- Common patterns
- Historical context

**When To Use:**
- No external source available
- General market knowledge
- Supplementary context

**Quality Standard:**
- ⚠️⚠️ ALWAYS flag as "internal knowledge"
- ⚠️⚠️ NEVER use for specific token data
- ⚠️⚠️ Lowest confidence level

---

## Automation Failure Protocol

### When Browser Automation Fails

**Symptoms:**
- Tool call limit reached (typically 50-60 calls)
- Browser subagent returns incomplete data
- Complex filtering/navigation not completing

**IMMEDIATE RESPONSE:**

1. **STOP Complex Automation**
   ```
   ❌ DO NOT: Continue trying same approach
   ❌ DO NOT: Conclude "no data available"
   ❌ DO NOT: Switch to Tier 3 sources immediately
   ```

2. **SWITCH to Screenshot Mode**
   ```
   ✅ DO: Take simple screenshots of data tables
   ✅ DO: Capture visible token listings
   ✅ DO: Save to research_logs for analysis
   ```

3. **PERFORM Manual Analysis**
   ```
   ✅ DO: Review all captured screenshots
   ✅ DO: Extract token names, FDVs, liquidity  manually
   ✅ DO: Create candidate list from visual data
   ```

4. **DOCUMENT Failure and Recovery**
   ```
   ✅ DO: Log in failure_logs/ with timestamp
   ✅ DO: Note what approach failed
   ✅ DO: Document successful recovery method
   ✅ DO: Update protocols with lessons
   ```

5. **PROCEED with Verified Candidates**
   ```
   ✅ DO: Use manually extracted candidates
   ✅ DO: Apply normal deep dive process
   ✅ DO: Flag as "manual verification" in brief
   ```

### Example Recovery Process

**Failed Approach:**
```
Browser task: "Scan WhaleIntel, filter FDV $200k-$4M, extract all
data, navigate pages, click tokens, get full details"
→ Hits 60 tool call limit at page 2
→ Incomplete data
```

**Successful Recovery:**
```
1. Screenshot WhaleIntel Overview page (5 tool calls)
2. Screenshot scrolled views showing tokens (3-4 screenshots)
3. Manual review: Extract HANA ($762k), SAGE ($744k), ZOOF ($679k)
4. Targeted research on each (10-15 calls per token)
5. Complete analysis with verified data
```

---

## Source Verification Checklist

### For Every Claim, Document:
- [ ] **Source Name** (WhaleIntel, GeckoTerminal, Basescan, etc.)
- [ ] **Source Tier** (1, 2, or 3)
- [ ] **Timestamp** (when data was retrieved)
- [ ] **URL** (direct link to data)
- [ ] **Confidence** (High/Medium/Low based on tier)

### When Sources Conflict:
1. **Prefer Tier 1** over Tier 2
2. **Use conservative value** (lower FDV, lower liquidity)
3. **Document both values** with sources
4. **Flag discrepancy** in research notes
5. **Investigate reason** for conflict if significant

### Example Citation Format:
```markdown
**FDV:** $762k (WhaleIntel - Tier 1 - 2025-11-26 07:15 AEST)  
_Confirmed: $760k (GeckoTerminal - Tier 2 - 2025-11-26 07:16 AEST)_
```

---

## Quality Standards by Tier

### Tier 1 Standards
- ✅ **Freshness:** <5 minutes old
- ✅ **Verification:** Direct platform access
- ✅ **Cross-reference:** Checked against Tier 2
- ✅ **Confidence:** HIGH

### Tier 2 Standards
- ✅ **Freshness:** <15 minutes old
- ✅ **Verification:** Manual confirmation
- ✅ **Cross-reference:** Aligns with Tier 1
- ✅ **Confidence:** MEDIUM-HIGH

### Tier 3 Standards
- ⚠️ **Freshness:** <1 hour old
- ⚠️ **Verification:** Multiple sources required
- ⚠️ **Cross-reference:** Checked against Tier 1-2 if available
- ⚠️ **Confidence:** MEDIUM-LOW

---

## Common Mistakes to Avoid

### ❌ Tier Jumping
**Wrong:**
```
1. Open WhaleIntel → automation fails
2. Immediately search "HANA token FDV" on Google
3. Use first result without verification
```

**Right:**
```
1. Open WhaleIntel → automation fails
2. Capture screenshots of visible data
3. Manually extract token data from screenshots
4. Verify with GeckoTerminal (Tier 2)
5. Only then use Tier 3 if needed for gaps
```

### ❌ Single Source Dependency
**Wrong:**
```
Found $HANA on WhaleIntel with $762k FDV
→ Immediately proceed to deep dive without confirmation
```

**Right:**
```
Found $HANA on WhaleIntel with $762k FDV
→ Confirm on GeckoTerminal: $760k FDV
→ Both sources align, proceed with confidence
```

### ❌ Lazy Automation
**Wrong:**
```
Browser task hits limit → "No data available, moving on"
```

**Right:**
```
Browser task hits limit → Screenshot mode → Manual extraction →
Targeted research → Complete analysis
```

---

## Success Metrics

### Compliance Rate
- **100%** - Tier 1 sources checked before Tier 3
- **≥90%** - Tier 2 confirmation for all Deep Dive picks
- **≥95%** - Proper source citation in all briefs

### Automation Recovery Rate
- **100%** - Screenshot fallback when automation fails
- **≥80%** - Manual analysis completes successfully
- **100%** - Failures documented in failure_logs/

### Data Quality
- **<5%** - Discrepancy rate between Tier 1 and Tier 2
- **0** - Unsourced claims in published briefs
- **100%** - Full contract verification for top picks

---

**Follow the hierarchy. Verify independently. Document thoroughly.**
