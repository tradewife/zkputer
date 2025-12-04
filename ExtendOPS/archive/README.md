# Archived Scripts

This directory contains historical one-off trading scripts that were moved from the root directory during the 2025-12-02 cleanup.

## Purpose
These scripts represent specific trade executions, position management tasks, and SDK testing from past trading sessions. They are preserved for reference but should not be used for current trading operations.

## Categories

### Trade Execution Scripts (Historical)
- `execute_ada_25x_NOW.py` - ADA 25x leverage entry
- `execute_hype_long.py` - HYPE long position entry
- `execute_daily_trades.py` - Daily trade execution batch
- `execute_sol_avax_conservative.py`, `execute_sol_avax_final.py`, `execute_trades_sol_avax.py` - SOL/AVAX trade executions

### Position Management Scripts
- `buy_avax_now.py`, `manage_avax_position.py` - AVAX position management
- `close_sol_fixed.py`, `close_sol_limit.py`, `close_sol_position.py`, `close_sol_utility.py` - SOL closing variations
- `place_avax_adjusted.py`, `place_avax_final.py`, `place_avax_simple.py` - AVAX placement scripts
- `place_hype_entry_only.py`, `place_sol_reduced.py`, `place_sol_short.py` - Other position placement

### SDK Testing/Debugging
- `inspect_sdk.py`, `inspect_sdk_2.py`, `inspect_sdk_3.py` - Extended SDK inspection

## Current Best Practices

For current trading operations, use:
- **Account Status**: `📊 Core Trading System/utilities/quick_status.py`
- **Position Management**: `📊 Core Trading System/trading_module.py` (canonical API)
- **Trade Execution**: `📊 Core Trading System/extended_executor_production.py`
- **Order Management**: `📊 Core Trading System/utilities/cancel_all_orders.py`

## Archive Date
2025-12-02

These scripts are kept for historical reference and learning from past trading sessions.
