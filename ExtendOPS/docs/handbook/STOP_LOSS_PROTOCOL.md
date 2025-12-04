# Stop Loss Placement Protocol (MANDATORY)

## Created: 2025-12-01
## Trigger: AVAX trade stopped out due to inadequate stop placement

## Rule: ATR-Based Stop Loss Calculation

### Before EVERY trade, MUST calculate:

1. **24h ATR (Average True Range)**
   - Use: `(High - Low)` for last 24h
   - Or: Standard ATR(14) if available

2. **Minimum Stop Distance**
   - Trending market: `0.8 × ATR`
   - Ranging market: `1.2 × ATR`
   
3. **Asset-Specific Minimums**
   ```
   BTC:     $200-300
   ETH:     $80-120
   SOL:     $2-3
   AVAX:    $0.40-0.60
   ADA:     $0.03-0.05
   Low-cap: 3-5% of entry
   ```

4. **Technical Level Override**
   - If nearby support/resistance exists within 10% of ATR stop
   - Use the technical level instead
   - Example: ATR says $13.50, but support at $13.00 → use $13.00

### Stop Placement Process:

```python
# Step 1: Get ATR
atr_24h = calculate_atr(symbol, period=24h)

# Step 2: Calculate minimum distance
min_stop_distance = atr_24h * 0.8  # or 1.2 for ranging

# Step 3: Apply asset minimum
asset_minimums = {
    "BTC": 200,
    "ETH": 80,
    "SOL": 2,
    "AVAX": 0.40,
    # ...
}
min_stop_distance = max(min_stop_distance, asset_minimums[symbol])

# Step 4: Check technical levels
nearby_support = find_support(symbol, entry_price)
if abs(entry_price - nearby_support) < (min_stop_distance * 1.1):
    stop_price = nearby_support
else:
    stop_price = entry_price - min_stop_distance

# Step 5: Validate
assert (entry_price - stop_price) >= min_stop_distance
```

### Enforcement:

**EVERY trade recommendation MUST include:**
1. 24h ATR value
2. Calculated stop distance
3. Technical level justification (if used)

**Example:**
```
Entry: $13.31
ATR 24h: $0.45
Min Stop Distance: $0.45 × 0.8 = $0.36
Asset Min (AVAX): $0.40
Support Level: $13.00
→ Stop: $13.00 (technical level, $0.31 away)
```

## Violations:

- ❌ Dec 1, 2025: AVAX stop @ $13.15 (only $0.16 away, no ATR check)
  
## This replaces arbitrary percentage-based stops.
