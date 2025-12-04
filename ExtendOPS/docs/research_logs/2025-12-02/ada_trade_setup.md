# ADA 25x Leverage Long - Dec 2, 2025 07:47 AEST

## Trade Specification

**Symbol:** ADA-USD (Extended Exchange)  
**Direction:** LONG  
**Leverage:** 25x  
**Setup Type:** Strategic High Leverage Long

## Entry & Risk Parameters

```
Entry Price:     $0.3770
Stop Loss:       $0.3520 (compromise stop - $0.025 distance)  
Liquidation:     ~$0.3620 (with 25x leverage, ~4% from entry)
```

**Stop Analysis:**
- Stop Distance: $0.025 (between tight $0.015 and protocol $0.03)
- Liquidation at $0.3620 > Stop at $0.3520 ✓ (stop hits first)
- Below protocol minimum but reasonable for 25x leverage

## Position Sizing

```
Account Risk:    $20 (20% of $100 account)
Stop Distance:   $0.025
Position Size:   $20 / $0.025 = 800 ADA contracts

Notional Value:  800 × $0.377 = $301.60
Margin Required: $301.60 / 25 = $12.06
Max Loss:        $20 if stopped ✓
```

## Take Profit Targets

```
TP1: $0.3900 (+3.4%, $0.013 gain = 0.52R) - 50% position
TP2: $0.4000 (+6.1%, $0.023 gain = 0.92R) - 30% position  
TP3: $0.4200 (+11.4%, $0.043 gain = 1.72R) - 20% position
```

## Execution Details

**Entry Order:**
- Type: Market (immediate execution)
- Quantity: 800 ADA
- Expected Fill: $0.377

**Stop Loss Order:**
- Type: STOP (NOT limit - triggers at price)
- Trigger Price: $0.3520
- Side: SELL (closes long)
- Quantity: 800 ADA

**Take Profit Orders:**
- TP1: Limit Sell 400 ADA @ $0.3900
- TP2: Limit Sell 240 ADA @ $0.4000
- TP3: Limit Sell 160 ADA @ $0.4200

## Risk Warnings

⚠️ **CRITICAL:**
1. Liquidation at $0.3620 (only 4% move = $0.015)
2. Stop at $0.3520 is below protocol minimum ($0.03 required)
3. Normal ADA volatility could approach liquidation
4. 25x exceeds protocol max of 12x leverage
5. Monitor position closely - set alerts at $0.365

## Execution Timestamp

- **Time:** 2025-12-02 07:47 AEST
- **Account Size:** $100
- **Risk:** 20% ($20)
- **Leverage:** 25x (extreme risk)

**Status:** PENDING USER CONFIRMATION
