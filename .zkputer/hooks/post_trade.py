#!/usr/bin/env python3
"""
ZKputer Post-Trade Hook
Logs trade results for audit trail
"""

import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, "/home/kt/ZKputer")

AUDIT_LOG = Path("/home/kt/ZKputer/logs/trade_audit.jsonl")


def log_trade_result(trade: Dict, result: Dict):
    """Log a trade result to the audit trail"""
    
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "trade": trade,
        "result": result,
        "success": result.get("status") == "ok"
    }
    
    with open(AUDIT_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    
    status = "SUCCESS" if entry["success"] else "FAILED"
    print(f"[{status}] {trade.get('exchange')}/{trade.get('symbol')} {trade.get('side')} logged")


def log_session_summary(trades: List[Dict], results: List[Dict]):
    """Log session summary"""
    
    successes = sum(1 for r in results if r.get("status") == "ok")
    failures = len(results) - successes
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "type": "session_summary",
        "total_trades": len(trades),
        "successes": successes,
        "failures": failures,
        "success_rate": successes / len(trades) if trades else 0
    }
    
    with open(AUDIT_LOG, "a") as f:
        f.write(json.dumps(summary) + "\n")
    
    print(f"\nSession Summary: {successes}/{len(trades)} trades successful")


def run_post_trade_hook(trades: List[Dict], results: List[Dict]) -> bool:
    """
    Main entry point for post-trade logging
    
    Args:
        trades: List of trade specifications that were attempted
        results: List of results from execution
    """
    print("=" * 60)
    print("ZKputer POST-TRADE LOGGING")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 60)
    
    for trade, result in zip(trades, results):
        log_trade_result(trade, result)
    
    log_session_summary(trades, results)
    
    print(f"\nAudit log: {AUDIT_LOG}")
    return True


if __name__ == "__main__":
    # Test with sample data
    test_trades = [
        {"exchange": "extended", "symbol": "BTC-USD", "side": "buy", "size": 0.001, "price": 95000},
    ]
    test_results = [
        {"status": "ok", "order_id": "12345", "fill_price": 94999.5}
    ]
    run_post_trade_hook(test_trades, test_results)
