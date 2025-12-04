from utils.visuals import log, RED, GREEN
from pathlib import Path
import json

class ComplianceOfficer:
    """
    Enforces protocol compliance across all OPS modes.
    Now loads limits from protocols/core/RISK_LIMITS.json when available.
    """
    
    def __init__(self, mode="ExtendOPS"):
        self.mode = mode
        self._load_risk_limits()
    
    def _load_risk_limits(self):
        """Load risk limits from JSON or use defaults"""
        base_path = Path(__file__).parent.parent.parent
        risk_limits_path = base_path / "protocols" / "core" / "RISK_LIMITS.json"
        
        if risk_limits_path.exists():
            with open(risk_limits_path, 'r') as f:
                limits = json.load(f)
            
            # Universal limits
            universal = limits.get("universal", {})
            self.max_risk_percent = universal.get("max_risk_per_trade_percent", 20) / 100
            self.max_leverage = universal.get("max_leverage", 12)
            self.max_concurrent_positions = universal.get("max_concurrent_positions", 2)
            self.mae_cut_threshold = universal.get("mae_cut_threshold", 0.6)
            
            # BaseOPS specific
            base_limits = limits.get("ops_specific", {}).get("BaseOPS", {})
            self.base_max_fdv = base_limits.get("max_fdv_usd", 4000000)
            self.base_min_liquidity = base_limits.get("min_liquidity_usd", 50000)
            self.base_min_age_hours = base_limits.get("min_age_hours", 0)
            
            # ExtendOPS/HyperOPS specific
            extend_limits = limits.get("ops_specific", {}).get("ExtendOPS", {})
            self.extend_account_equity = extend_limits.get("default_account_equity_usd", 100)
            self.extend_min_volume = extend_limits.get("min_24h_volume_usd", 500000)
            self.extend_min_oi = extend_limits.get("min_open_interest_usd", 1000000)
            
            # PumpOPS specific
            pump_limits = limits.get("ops_specific", {}).get("PumpOPS", {})
            self.pump_max_position = pump_limits.get("max_position_size_usd", 100)
            self.pump_max_slippage = pump_limits.get("max_slippage_percent", 5)
            
            log("INFO", f"Risk limits loaded from RISK_LIMITS.json")
        else:
            # Fallback to hardcoded defaults
            self.base_min_liquidity = 50000
            self.base_max_fdv = 4000000
            self.base_min_age_hours = 0
            self.max_risk_percent = 0.20
            self.max_leverage = 12
            self.max_concurrent_positions = 2
            self.extend_account_equity = 100
            log("WARN", "Using hardcoded risk limits (RISK_LIMITS.json not found)")

    def check_base_token(self, token_data):
        """
        Enforces BaseOPS Part A: Core Protocol.
        """
        symbol = token_data.get('symbol', 'UNKNOWN')
        fdv = token_data.get('fdv', float('inf'))
        liquidity = token_data.get('liquidity', 0)
        
        # Rule: FDV Hard Ceiling $4M
        if fdv > self.base_max_fdv:
            log("WARN", f"Compliance Reject {symbol}: FDV ${fdv:,.0f} > $4M Limit")
            return False
            
        # Rule: Liquidity Floor $50k
        if liquidity < self.base_min_liquidity:
            log("WARN", f"Compliance Reject {symbol}: Liquidity ${liquidity:,.0f} < $50k Floor")
            return False
            
        log("INFO", f"Compliance Pass {symbol}: FDV ${fdv:,.0f}, Liq ${liquidity:,.0f}")
        return True

    def check_hyper_trade(self, trade_params):
        """
        Enforces HyperOPS/ExtendOPS Risk Management System.
        """
        risk_amount = trade_params.get('risk_amount', 0)
        leverage = trade_params.get('leverage', 1)
        account_equity = trade_params.get('account_equity', self.extend_account_equity)
        
        # Rule: Max Risk 20% of Equity
        max_risk = account_equity * self.max_risk_percent
        if risk_amount > max_risk:
            log("ERROR", f"Risk Reject: ${risk_amount} > ${max_risk} ({int(self.max_risk_percent*100)}% Limit)")
            return False, {"violation": "risk_limit", "value": risk_amount, "limit": max_risk}
            
        # Rule: Max Leverage
        if leverage > self.max_leverage:
            log("ERROR", f"Risk Reject: {leverage}x > {self.max_leverage}x Limit")
            return False, {"violation": "leverage_limit", "value": leverage, "limit": self.max_leverage}
        
        log("INFO", f"Trade compliance PASSED: Risk ${risk_amount:.2f}, Leverage {leverage}x")
        return True, {"risk_check": "PASS", "leverage_check": "PASS"}
    
    def validate_trade(self, trade_data):
        """
        Full trade validation against compliance schema.
        Returns (is_valid, compliance_report)
        """
        report = {
            "risk_limit": {"passed": False, "value": 0, "limit": 0},
            "leverage_limit": {"passed": False, "value": 0, "limit": 0},
            "stop_loss_valid": {"passed": False, "order_type": None},
            "multi_source_verified": {"passed": False, "source_count": 0, "required": 3}
        }
        
        # Risk check
        risk_percent = trade_data.get('risk_percent', 100)
        report["risk_limit"]["value"] = risk_percent
        report["risk_limit"]["limit"] = self.max_risk_percent * 100
        report["risk_limit"]["passed"] = risk_percent <= (self.max_risk_percent * 100)
        
        # Leverage check
        leverage = trade_data.get('leverage', 1)
        report["leverage_limit"]["value"] = leverage
        report["leverage_limit"]["limit"] = self.max_leverage
        report["leverage_limit"]["passed"] = leverage <= self.max_leverage
        
        # Stop loss check
        stop_loss = trade_data.get('stop_loss', {})
        order_type = stop_loss.get('order_type', 'UNKNOWN')
        valid_types = ['STOP', 'STOP_LIMIT', 'STOP_MARKET']
        report["stop_loss_valid"]["order_type"] = order_type
        report["stop_loss_valid"]["passed"] = order_type in valid_types
        
        # Multi-source verification
        sources = trade_data.get('sources', [])
        report["multi_source_verified"]["source_count"] = len(sources)
        report["multi_source_verified"]["passed"] = len(sources) >= 3
        
        # Overall result
        all_passed = all(check["passed"] for check in report.values())
        
        return all_passed, report
