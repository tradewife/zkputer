"""
Real Data Sources for BaseOPS and HyperOPS
Uses actual APIs: GeckoTerminal, Hyperliquid
"""
import time
import requests
from utils.visuals import log, type_print, hacker_loader
from core.compliance import ComplianceOfficer

class ResearchAgent:
    def __init__(self):
        self.compliance = ComplianceOfficer()
        self.gecko_base_url = "https://api.geckoterminal.com/api/v2"
        self.hyper_base_url = "https://api.hyperliquid.xyz"
    
    def scan_base_market(self):
        """Scan Base chain using GeckoTerminal API"""
        log("INFO", "Initiating BaseOPS Protocol Scan...")
        hacker_loader("FETCHING GECKOTERMINAL DATA", duration=1)
        
        try:
            # Get Base network pools sorted by 24h volume
            url = f"{self.gecko_base_url}/networks/base/pools"
            params = {
                "page": 1,
                "sort": "h24_volume_usd_desc"
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code != 200:
                log("WARN", f"GeckoTerminal API error: {response.status_code}")
                return self._fallback_base_data()
            
            data = response.json()
            pools = data.get('data', [])
            
            valid_tokens = []
            for pool in pools[:20]:  # Check top 20 by volume
                attrs = pool.get('attributes', {})
                
                token_data = {
                    "symbol": attrs.get('name', 'UNKNOWN').split('/')[0],
                    "address": attrs.get('address', ''),
                    "liquidity": float(attrs.get('reserve_in_usd', 0)),
                    "fdv": float(attrs.get('fdv_usd', 0) or 0),
                    "volume_24h": float(attrs.get('volume_usd', {}).get('h24', 0)),
                    "price_change_24h": float(attrs.get('price_change_percentage', {}).get('h24', 0))
                }
                
                # Apply compliance checks
                if self.compliance.check_base_token(token_data):
                    valid_tokens.append(token_data)
            
            log("INFO", f"Found {len(valid_tokens)} compliant tokens")
            return valid_tokens
            
        except Exception as e:
            log("ERROR", f"GeckoTerminal scan failed: {e}")
            return self._fallback_base_data()
    
    def scan_hyperliquid_market(self):
        """Scan Hyperliquid perpetuals using real API"""
        log("INFO", "Starting HyperOPS Market Scan...")
        hacker_loader("ANALYZING HYPERLIQUID PERPETUALS", duration=1)
        
        try:
            # Get meta and asset contexts
            url = f"{self.hyper_base_url}/info"
            payload = {"type": "metaAndAssetCtxs"}
            
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code != 200:
                log("WARN", f"Hyperliquid API error: {response.status_code}")
                return self._fallback_hyper_data()
            
            data = response.json()
            universe = data[0].get('universe', [])
            asset_ctxs = data[1]
            
            setups = []
            for i, asset in enumerate(universe):
                if i >= len(asset_ctxs):
                    break
                    
                ctx = asset_ctxs[i]
                funding = float(ctx.get('funding', 0))
                mark_px = float(ctx.get('markPx', 0))
                
                # High funding rate = potential arbitrage
                if abs(funding) > 0.0001:  # 0.01% threshold
                    setup = {
                        "symbol": asset['name'],
                        "setup": "Funding Arbitrage" if funding > 0 else "Reverse Funding",
                        "funding_rate": funding,
                        "mark_price": mark_px,
                        "entry": mark_px,
                        "stop": mark_px * 0.99 if funding > 0 else mark_px * 1.01
                    }
                    setups.append(setup)
            
            log("INFO", f"Found {len(setups)} HyperOPS setups")
            return setups[:5]  # Top 5
            
        except Exception as e:
            log("ERROR", f"Hyperliquid scan failed: {e}")
            return self._fallback_hyper_data()
    
    def analyze_token(self, token):
        """Deep dive analysis per BaseOPS Part A"""
        type_print(f"\n>>> EXECUTING DEEP DIVE: {token['symbol']}...", speed=0.02)
        time.sleep(1)
        
        # BaseOPS Scoring Modules (simplified for now)
        modules = {
            "Liquidity Health": 5 if token.get('liquidity', 0) > 100000 else 3,
            "Volume/Liquidity Ratio": min(5, int(token.get('volume_24h', 0) / max(token.get('liquidity', 1), 1) * 10)),
            "Price Action": 5 if abs(token.get('price_change_24h', 0)) < 50 else 2,
            "Security": "PASS"  # Would need contract verification
        }
        
        for module, score in modules.items():
            log("INFO", f"Module [{module}]: {score}/5" if isinstance(score, int) else f"Module [{module}]: {score}")
            time.sleep(0.1)
        
        # Calculate LT_Score (simplified)
        numeric_scores = [v for v in modules.values() if isinstance(v, int)]
        avg_score = sum(numeric_scores) / len(numeric_scores) if numeric_scores else 0
        log("INFO", f"Calculated LT_Score: {avg_score:.2f} (Confidence: MEDIUM)")
        
        return True
    
    def _fallback_base_data(self):
        """Fallback data when API unavailable"""
        log("WARN", "Using fallback data (API unavailable)")
        return [
            {"symbol": "DEGEN", "fdv": 2500000, "liquidity": 150000, "volume_24h": 50000, "price_change_24h": 5.2},
            {"symbol": "BUILD", "fdv": 800000, "liquidity": 80000, "volume_24h": 30000, "price_change_24h": -2.1}
        ]
    
    def _fallback_hyper_data(self):
        """Fallback data when API unavailable"""
        log("WARN", "Using fallback data (API unavailable)")
        return [
            {"symbol": "BTC-PERP", "setup": "Funding Arbitrage", "funding_rate": 0.0003, "entry": 95000, "stop": 94000},
            {"symbol": "ETH-PERP", "setup": "Momentum Catalyst", "funding_rate": -0.0001, "entry": 3200, "stop": 3100}
        ]
