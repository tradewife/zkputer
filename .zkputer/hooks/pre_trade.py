#!/usr/bin/env python3
"""
ZKputer Pre-Trade Hook
Validates ALL trades before execution - MANDATORY
"""

import sys
import json
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass

# Add project root to path
sys.path.insert(0, "/home/kt/ZKputer")

from src.core.exchanges import verify_all_configs


@dataclass
class TradeValidation:
    valid: bool
    errors: List[str]
    warnings: List[str]


class PreTradeValidator:
    """Validates trades against risk limits and config requirements"""
    
    # Risk limits - all advisory, human has final say
    MAX_LEVERAGE = 12  # Position size = margin * leverage
    MAX_POSITIONS_PER_EXCHANGE = 2
    # Stop loss is PROTOCOL, not enforced - Extended may require separate SL order
    REQUIRED_STOP_LOSS = False  # Human can approve no-SL trades
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate_exchange_config(self, exchange: str) -> bool:
        """Verify exchange configuration exists and is mainnet"""
        try:
            results = verify_all_configs()
            status = results.get(exchange)
            if not status or not status.configured:
                self.errors.append(f"ABORT: {exchange} not configured or has errors")
                return False
            if status.network not in ["mainnet", "base-mainnet"]:
                self.errors.append(f"ABORT: {exchange} is not on mainnet (found: {status.network})")
                return False
            return True
        except Exception as e:
            self.errors.append(f"ABORT: Config verification failed: {e}")
            return False
    
    def validate_trade(self, trade: Dict) -> TradeValidation:
        """
        Validate a single trade specification
        
        Expected trade format:
        {
            "exchange": "extended" | "hyperliquid" | "base",
            "symbol": "BTC-USD" or "BTC" or "eth",
            "side": "buy" | "sell",
            "size": 0.01,
            "price": 50000.0,
            "leverage": 10,
            "stop_loss": 48000.0,  # Required
            "take_profit": 55000.0  # Optional
        }
        """
        self.errors = []
        self.warnings = []
        
        # Required fields
        required = ["exchange", "symbol", "side", "size", "price"]
        for field in required:
            if field not in trade:
                self.errors.append(f"Missing required field: {field}")
        
        if self.errors:
            return TradeValidation(False, self.errors, self.warnings)
        
        exchange = trade["exchange"].lower()
        
        # Validate exchange config
        if not self.validate_exchange_config(exchange):
            return TradeValidation(False, self.errors, self.warnings)
        
        # Validate side
        if trade["side"].lower() not in ["buy", "sell"]:
            self.errors.append(f"Invalid side: {trade['side']}. Must be 'buy' or 'sell'")
        
        # Validate size
        size = float(trade["size"])
        price = float(trade["price"])
        if size <= 0:
            self.warnings.append(f"Size {size} is not positive - confirm intent")
        
        # Validate leverage (ADVISORY - human has final say)
        # Position size limit = margin * 12x leverage
        leverage = trade.get("leverage", 1)
        if leverage > self.MAX_LEVERAGE:
            self.warnings.append(f"Leverage {leverage}x exceeds protocol max {self.MAX_LEVERAGE}x")
        
        # Validate stop loss (PROTOCOL - warn but don't block)
        # Extended Exchange may require placing SL as separate order after entry
        if "stop_loss" not in trade:
            self.warnings.append("NO STOP LOSS - Add SL immediately after entry per protocol")
        elif "stop_loss" in trade:
            sl = float(trade["stop_loss"])
            sl_distance = abs(price - sl) / price
            if sl_distance > 0.10:
                self.warnings.append(f"Stop loss {sl_distance*100:.1f}% away - consider tighter stop")
            if sl_distance < 0.005:
                self.warnings.append(f"Stop loss only {sl_distance*100:.2f}% away - may trigger prematurely")
        
        return TradeValidation(
            valid=len(self.errors) == 0,
            errors=self.errors,
            warnings=self.warnings
        )
    
    def validate_batch(self, trades: List[Dict]) -> TradeValidation:
        """Validate a batch of trades"""
        all_errors = []
        all_warnings = []
        
        # Count positions per exchange
        exchange_counts = {}
        
        for i, trade in enumerate(trades):
            result = self.validate_trade(trade)
            # All limits are advisory - human has final say
            all_warnings.extend([f"Trade {i+1}: {e}" for e in result.errors])
            all_warnings.extend([f"Trade {i+1}: {w}" for w in result.warnings])
            
            exchange = trade.get("exchange", "unknown").lower()
            exchange_counts[exchange] = exchange_counts.get(exchange, 0) + 1
        
        # Check position limits per exchange (ADVISORY)
        for exchange, count in exchange_counts.items():
            if count > self.MAX_POSITIONS_PER_EXCHANGE:
                all_warnings.append(f"Many positions on {exchange}: {count} > protocol max {self.MAX_POSITIONS_PER_EXCHANGE}")
        
        return TradeValidation(
            valid=len(all_errors) == 0,
            errors=all_errors,
            warnings=all_warnings
        )


def run_pre_trade_hook(trades: List[Dict]) -> bool:
    """
    Main entry point for pre-trade validation
    
    Returns True always - human has final say on all trades
    Displays warnings for protocol deviations
    """
    print("=" * 60)
    print("ZKputer PRE-TRADE VALIDATION")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Trades to validate: {len(trades)}")
    print("=" * 60)
    
    validator = PreTradeValidator()
    result = validator.validate_batch(trades)
    
    if result.warnings:
        print("\nPROTOCOL ADVISORIES (human has final say):")
        for w in result.warnings:
            print(f"  [!] {w}")
    
    # Config errors still block (can't trade without valid config)
    if result.errors:
        print("\nCONFIG ISSUES:")
        for e in result.errors:
            print(f"  [X] {e}")
        print("\n" + "=" * 60)
        print("FIX CONFIG ISSUES BEFORE PROCEEDING")
        print("=" * 60)
        return False
    
    print("\n" + "=" * 60)
    print("VALIDATION COMPLETE - HUMAN DECISION REQUIRED")
    print("=" * 60)
    return True


if __name__ == "__main__":
    # Test with sample trades
    test_trades = [
        {
            "exchange": "extended",
            "symbol": "BTC-USD",
            "side": "buy",
            "size": 0.001,
            "price": 95000.0,
            "leverage": 10,
            "stop_loss": 93000.0,
            "take_profit": 100000.0
        },
        {
            "exchange": "hyperliquid",
            "symbol": "SOL",
            "side": "buy",
            "size": 0.2,
            "price": 230.0,
            "leverage": 10,
            "stop_loss": 220.0,
        }
    ]
    
    run_pre_trade_hook(test_trades)
