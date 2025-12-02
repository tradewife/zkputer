#!/usr/bin/env python3
"""
Trade Execution Template - Standardized for Future Use
Copy this file and modify the trade_list for new executions
"""

import sys
import os

# Add the project root to Python path
sys.path.append("/home/kt/Desktop/HyperOPS")

# Import with proper path handling
import importlib.util

spec = importlib.util.spec_from_file_location(
    "hyperliquid_executor_production",
    "/home/kt/Desktop/HyperOPS/📊 Core Trading System/hyperliquid_executor_production.py",
)
executor_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(executor_module)
HyperliquidExecutor = executor_module.HyperliquidExecutor


def execute_custom_trades(trade_list, description="Custom trade execution"):
    """
    Execute custom trades with standardized error handling

    Args:
        trade_list: List of trade dictionaries
            Example: [
                {"symbol": "XRP", "side": "buy", "size": 8.0, "price": 2.24},
                {"symbol": "SOL", "side": "buy", "size": 0.1, "price": 138.50}
            ]
        description: Description for logging purposes
    """
    print(f"🎯 {description}")
    print(f"📋 Trade Plan: {len(trade_list)} trades")

    for i, trade in enumerate(trade_list, 1):
        print(
            f"  {i}. {trade['side'].upper()} {trade['size']} {trade['symbol']} @ ${trade['price']}"
        )

    executor = HyperliquidExecutor()
    return executor.main(trade_list)


# EXAMPLE USAGE - Uncomment and modify for your trades:
if __name__ == "__main__":
    # Example trades from our analysis
    example_trades = [
        {"symbol": "XRP", "side": "buy", "size": 8.0, "price": 2.24},
        {"symbol": "SOL", "side": "buy", "size": 0.1, "price": 138.50},
    ]

    execute_custom_trades(example_trades, "Example ETF Momentum Trades")
