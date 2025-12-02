from utils.visuals import log, RED, GREEN

class ComplianceOfficer:
    def __init__(self):
        # BaseOPS Constraints
        self.base_min_liquidity = 50000
        self.base_max_fdv = 4000000
        self.base_min_age_hours = 0 # Exception for new launches if liquidity > $50k
        
        # HyperOPS Constraints
        self.hyper_max_risk_percent = 0.20
        self.hyper_max_leverage = 12
        self.hyper_account_equity = 100 # Default for HyperOPS

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
        Enforces HyperOPS Risk Management System.
        """
        risk_amount = trade_params.get('risk_amount', 0)
        leverage = trade_params.get('leverage', 1)
        
        # Rule: Max Risk 20% of Equity
        max_risk = self.hyper_account_equity * self.hyper_max_risk_percent
        if risk_amount > max_risk:
            log("ERROR", f"Risk Reject: ${risk_amount} > ${max_risk} (20% Limit)")
            return False
            
        # Rule: Max Leverage 12x
        if leverage > self.hyper_max_leverage:
            log("ERROR", f"Risk Reject: {leverage}x > {self.hyper_max_leverage}x Limit")
            return False
            
        return True
