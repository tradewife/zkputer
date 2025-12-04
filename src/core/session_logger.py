"""
ZKputer Session Logger
Provides append-only audit trail for all agent decisions and actions.
"""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any
import uuid


class SessionLogger:
    """
    Append-only session logging for ZKputer audit trail.
    All entries are written to SESSION_LOG.jsonl in the .zkputer directory.
    """
    
    def __init__(self, base_path: Optional[str] = None):
        if base_path is None:
            base_path = Path(__file__).parent.parent.parent
        self.base_path = Path(base_path)
        self.log_path = self.base_path / ".zkputer" / "SESSION_LOG.jsonl"
        self.session_id = str(uuid.uuid4())[:8]
        self.ops_mode = "unknown"
        
        # Ensure directory exists
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
    
    def set_ops_mode(self, mode: str):
        """Set the current OPS mode for logging"""
        self.ops_mode = mode
    
    def _write_entry(self, entry: Dict[str, Any]):
        """Append a single entry to the log file"""
        entry["ts"] = datetime.now(timezone.utc).isoformat()
        entry["session_id"] = self.session_id
        entry["ops_mode"] = self.ops_mode
        
        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
    
    def log_session_start(self, account_equity: float = 100):
        """Log session start"""
        self._write_entry({
            "action": "SESSION_START",
            "data": {
                "account_equity": account_equity,
                "version": "1.0.0"
            },
            "sources": [],
            "compliance": {},
            "user_approved": True
        })
    
    def log_session_end(self, summary: Optional[Dict] = None):
        """Log session end"""
        self._write_entry({
            "action": "SESSION_END",
            "data": summary or {},
            "sources": [],
            "compliance": {},
            "user_approved": True
        })
    
    def log_market_scan(self, symbols: List[str], sources: List[str], findings: Dict):
        """Log market scan activity"""
        self._write_entry({
            "action": "MARKET_SCAN",
            "data": {
                "symbols_scanned": symbols,
                "findings": findings
            },
            "sources": sources,
            "compliance": {},
            "user_approved": False
        })
    
    def log_trade_signal(
        self,
        symbol: str,
        side: str,
        entry: float,
        stop: float,
        tp1: float,
        tp2: Optional[float],
        size: float,
        leverage: float,
        thesis: str,
        sources: List[str],
        compliance_checks: Dict
    ):
        """Log a trade signal (setup identified, awaiting approval)"""
        self._write_entry({
            "action": "TRADE_SIGNAL",
            "symbol": symbol,
            "data": {
                "side": side,
                "entry": entry,
                "stop": stop,
                "tp1": tp1,
                "tp2": tp2,
                "size": size,
                "leverage": leverage,
                "thesis": thesis
            },
            "sources": sources,
            "compliance": compliance_checks,
            "user_approved": False
        })
    
    def log_trade_approved(self, symbol: str, command: str):
        """Log user approval of a trade"""
        self._write_entry({
            "action": "TRADE_APPROVED",
            "symbol": symbol,
            "data": {"command": command},
            "sources": [],
            "compliance": {},
            "user_approved": True
        })
    
    def log_trade_executed(
        self,
        symbol: str,
        side: str,
        order_id: str,
        fill_price: Optional[float],
        fill_size: Optional[float],
        status: str
    ):
        """Log trade execution result"""
        self._write_entry({
            "action": "TRADE_EXECUTED",
            "symbol": symbol,
            "data": {
                "side": side,
                "order_id": order_id,
                "fill_price": fill_price,
                "fill_size": fill_size,
                "status": status
            },
            "sources": ["exchange_api"],
            "compliance": {},
            "user_approved": True
        })
    
    def log_trade_closed(
        self,
        symbol: str,
        exit_price: float,
        exit_reason: str,
        pnl_usd: float,
        pnl_percent: float
    ):
        """Log position closure"""
        self._write_entry({
            "action": "POSITION_CLOSED",
            "symbol": symbol,
            "data": {
                "exit_price": exit_price,
                "exit_reason": exit_reason,
                "pnl_usd": pnl_usd,
                "pnl_percent": pnl_percent
            },
            "sources": ["exchange_api"],
            "compliance": {},
            "user_approved": True
        })
    
    def log_compliance_violation(
        self,
        action_attempted: str,
        violation_type: str,
        details: Dict
    ):
        """Log a compliance violation (action blocked)"""
        self._write_entry({
            "action": "COMPLIANCE_VIOLATION",
            "data": {
                "attempted_action": action_attempted,
                "violation_type": violation_type,
                "details": details
            },
            "sources": [],
            "compliance": {"blocked": True, "reason": violation_type},
            "user_approved": False
        })
    
    def log_knowledge_update(self, file_updated: str, update_type: str, details: Dict):
        """Log knowledge graph update"""
        self._write_entry({
            "action": "KNOWLEDGE_UPDATE",
            "data": {
                "file": file_updated,
                "update_type": update_type,
                "details": details
            },
            "sources": [],
            "compliance": {},
            "user_approved": False
        })
    
    def log_mode_switch(self, old_mode: str, new_mode: str):
        """Log OPS mode switch"""
        old = self.ops_mode
        self.ops_mode = new_mode
        self._write_entry({
            "action": "MODE_SWITCH",
            "data": {
                "from": old_mode,
                "to": new_mode
            },
            "sources": [],
            "compliance": {},
            "user_approved": True
        })
    
    def log_custom(self, action: str, data: Dict, sources: List[str] = None, user_approved: bool = False):
        """Log custom action"""
        self._write_entry({
            "action": action,
            "data": data,
            "sources": sources or [],
            "compliance": {},
            "user_approved": user_approved
        })
    
    def get_session_entries(self) -> List[Dict]:
        """Get all entries for current session"""
        entries = []
        if self.log_path.exists():
            with open(self.log_path, "r") as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        if entry.get("session_id") == self.session_id:
                            entries.append(entry)
                    except json.JSONDecodeError:
                        continue
        return entries
    
    def get_all_entries(self, limit: int = 100) -> List[Dict]:
        """Get all log entries (most recent first)"""
        entries = []
        if self.log_path.exists():
            with open(self.log_path, "r") as f:
                for line in f:
                    try:
                        entries.append(json.loads(line.strip()))
                    except json.JSONDecodeError:
                        continue
        return entries[-limit:][::-1]


# Singleton instance
_logger = None

def get_logger() -> SessionLogger:
    """Get the singleton session logger instance"""
    global _logger
    if _logger is None:
        _logger = SessionLogger()
    return _logger


if __name__ == "__main__":
    # Test logging
    logger = SessionLogger()
    logger.set_ops_mode("ExtendOPS")
    logger.log_session_start(100)
    logger.log_market_scan(
        symbols=["BTC-USD", "ETH-USD", "SOL-USD"],
        sources=["Extended API", "Dextrabot"],
        findings={"setups_found": 2}
    )
    logger.log_trade_signal(
        symbol="SOL-USD",
        side="LONG",
        entry=240.0,
        stop=235.0,
        tp1=250.0,
        tp2=260.0,
        size=0.5,
        leverage=10,
        thesis="Funding arb + whale accumulation",
        sources=["Extended API", "Dextrabot", "ApexLiquid"],
        compliance_checks={
            "risk_check": {"passed": True, "value": 20, "limit": 20},
            "leverage_check": {"passed": True, "value": 10, "limit": 12}
        }
    )
    print("Test entries logged to SESSION_LOG.jsonl")
