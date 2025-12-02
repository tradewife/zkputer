# ⚙️ BaseOPS Configuration Setup Guide

## Overview
This guide walks you through configuring BaseOPS for optimal performance.

---

## Step 1: Understanding Configuration Files

### Scanning Parameters (`⚙️ Configuration/config/scanning_config.json`)
This file controls all scan behavior:

- **FDV Range**: $200k-$4M (hard ceiling)
-  **Liquidity Minimums**: $50k (fundamental), $20k (casino)
- **Volume Thresholds**: $50k minimum 24h
- **Price-Action Filters**: Reject pumps >200% in 7d
- **Browser Automation**: 15 tool call limit, screenshot fallback enabled

**You can edit these values** to tune the scanning behavior, but maintain the $4M FDV hard ceiling.

### API Keys (`⚙️ Configuration/config/api_keys.json.example`)
Template for API credentials (Telegram, X/Twitter, optional services).

---

## Step 2: API Configuration (Optional)

If you want to enable broadcasting to Telegram or X:

```bash
# 1. Copy the template
cp "⚙️ Configuration/config/api_keys.json.example" "⚙️ Configuration/config/api_keys.json"

# 2. Edit with your credentials
# Replace placeholders with actual API keys
```

### Telegram Setup
1. Create a bot via [@BotFather](https://t.me/botfather)
2. Get your `bot_token`
3. Add bot to your channel
4. Update `api_keys.json` with token and channel ID

### X (Twitter) Setup
1. Apply for X Developer account
2. Create an app and get API credentials
3. Update `api_keys.json` with keys and tokens

**Security Note:** Never commit `api_keys.json` to version control. Add to `.gitignore`.

---

## Step 3: Adjust Scanning Parameters

### Common Adjustments

#### Tighten FDV Range (More Conservative)
```json
{
  "fdv_range": {
    "min": 500000,
    "max": 2000000
  }
}
```

#### Increase Liquidity Requirements (Lower Risk)
```json
{
  "liquidity_minimum": {
    "fundamental_plays": 100000,
    "casino_plays": 50000
  }
}
```

#### Relax Pump Filter (More Opportunities)
```json
{
  "price_action_filters": {
    "reject_pump_threshold_percent": 300
  }
}
```

---

## Step 4: Knowledge Graph Initialization

The knowledge graph files in `🧠 Learning Engine/knowledge_graph/` are already initialized. You can customize:

### Add Your Own Sectors (`narratives.md`)
```markdown
| **Your Sector** | 0 | ➡️ Neutral | Tracking new category | - | 2025-XX-XX |
```

### Add Known Wallets (`smart_money.md`, `wallets.md`)
If you know elite traders/wallets, add them to these files for tracking.

### Define Custom Setups (`playbook.md`)
Document your own proven patterns for the agent to hunt.

---

## Step 5: Verify Setup

### Check Directory Structure
```bash
cd /home/kt/Desktop/BaseOPS
tree -L 2 -I 'venv|HyperOPS|__pycache__'
```

**Expected:** Emoji directories visible (📚, 📊, 🧠, ⚙️, 📖)

### Verify Config Files
```bash
cat "⚙️ Configuration/config/scanning_config.json"
cat "⚙️ Configuration/config/api_keys.json" # (if created)
```

### Test Agent Access
In your agent:
```
Command: "Read Handbook"
```

**Expected:** Agent confirms handbook loaded and lists file locations.

---

## Step 6: Run First Scan

```
Command: "Run the Daily"
```

The agent will:
1. Review knowledge graph
2. Scan WhaleIntel + GeckoTerminal
3. Apply filters from `scanning_config.json`
4. Generate daily brief in `📖 Other Components/research_logs/`

---

## Troubleshooting

### Issue: Agent can't find files
**Solution:** Check that emoji directories exist. Linux/Mac should support emoji folder names natively.

### Issue: Browser automation fails
**Solution:** This is expected (tool call limits). Agent will automatically switch to screenshot + manual analysis per SOURCE_PRIORITY_PROTOCOL.md.

### Issue: No candidates found
**Solution:** Review `scanning_config.json` - parameters may be too strict. Also check failure_logs/ for documented issues.

### Issue: API keys not working
**Solution:** Verify `api_keys.json` is in correct location (`⚙️ Configuration/config/`) and credentials are valid.

---

## Advanced Configuration

### Custom Data Source Priorities
Edit `📚 Agent Handbook/SOURCE_PRIORITY_PROTOCOL.md` to add or reorder data sources in Tier 1-3.

### Custom Scoring Weights
Edit `⚙️ Configuration/config/scanning_config.json`:
```json
{
  "risk_deduction_weights": {
    "security_risk": 0.40,
    "distribution_risk": 0.30,
    "liquidity_risk": 0.20,
    "team_risk": 0.10
  }
}
```

### Automation Tuning
Adjust browser task limits:
```json
{
  "browser_automation": {
    "max_tool_calls_per_task": 20
  }
}
```

**Warning:** Higher limits may still hit platform maximums (~50-60 calls).

---

## Maintenance

### Weekly
- Review `📖 Status/PRODUCTION_STATUS.md` for known issues
- Update knowledge graph with learnings
- Refine `playbook.md` with successful setups

### Monthly
- Review and tune `scanning_config.json` based on performance
- Update `narratives.md` with sector evolution
- Archive old research_logs if needed

---

**Configuration complete! BaseOPS is ready for production use.**
