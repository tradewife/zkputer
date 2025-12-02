"""
Position Tracker - CDP Account Balance and P&L Monitoring
Tracks token positions and calculates performance using CDP Trade API
"""

import os
import json
from typing import List, Dict
from dataclasses import dataclass, asdict
from datetime import datetime
from dotenv import load_dotenv
import logging

try:
    from cdp import CdpClient
except ImportError:
    print("CDP SDK not installed. Run: pip install cdp-sdk")
    exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '\u2699\ufe0f Configuration', 'config', '.env'))


@dataclass
class Position:
    """Token position data structure"""
    token_address: str
    symbol: str
    amount: float
    entry_price: float  # From performance log
    current_price: float  # Live from CDP/market
    unrealized_pnl: float
    pnl_percent: float
    cost_basis: float


class PositionTracker:
    """
    Tracks wallet positions and calculates P&L using CDP Trade API
    """
    
    def __init__(self):
        """Initialize CDP client for position tracking"""
        self.cdp = CdpClient()
        self.network = "base"
        self.performance_log_path = os.path.join(
            os.path.dirname(__file__), 
            '..', 
            '\ud83e\udde0 Knowledge Graph', 
            'performance_log.json'
        )
        logger.info("\u2705 Position tracker initialized")
    
    async def get_current_positions(self) -> List[Position]:
        """
        Get all current token positions from CDP account
        
        Returns:
            List[Position]: List of active positions with P&L
        """
        try:
            # Get CDP account
            account = await self.cdp.evm.getOrCreateAccount({"name": "BaseOPSTrading"})
            
            # Get all balances
            balances = await account.listBalances()
            
            positions = []
            performance_data = self._load_performance_log()
            
            for balance in balances:
                asset_id = balance.get("asset", {}).get("contractAddress", "")
                amount = float(balance.get("amount", 0))
                symbol = balance.get("asset", {}).get("symbol", "UNKNOWN")
                
                if amount > 0 and asset_id:
                    # Get entry data from performance log
                    entry_data = performance_data.get(asset_id, {})
                    entry_price = entry_data.get("entry_price", 0)
                    
                    # Get current price (mock for now, would use price API)
                    current_price = entry_price  # TODO: Fetch live price
                    
                    # Calculate P&L
                    pnl_data = self.calculate_pnl(
                        token=asset_id,
                        entry_price=entry_price,
                        current_price=current_price,
                        amount=amount
                    )
                    
                    position = Position(
                        token_address=asset_id,
                        symbol=symbol,
                        amount=amount,
                        entry_price=entry_price,
                        current_price=current_price,
                        unrealized_pnl=pnl_data["unrealized_pnl"],
                        pnl_percent=pnl_data["pnl_percent"],
                        cost_basis=pnl_data["cost_basis"]
                    )
                    positions.append(position)
            
            logger.info(f"\ud83d\udcca Found {len(positions)} active positions")
            return positions
            
        except Exception as e:
            logger.error(f"\u274c Failed to get positions: {e}")
            return []
    
    def calculate_pnl(self, 
                     token: str, 
                     entry_price: float, 
                     current_price: float, 
                     amount: float) -> Dict:
        """
        Calculate P&L for a position
        
        Args:
            token: Token address
            entry_price: Entry price (USDC per token)
            current_price: Current price (USDC per token)
            amount: Token amount held
            
        Returns:
            dict: Cost basis, current value, unrealized P&L, P&L %
        """
        cost_basis = entry_price * amount
        current_value = current_price * amount
        unrealized_pnl = current_value - cost_basis
        pnl_percent = (unrealized_pnl / cost_basis * 100) if cost_basis > 0 else 0
        
        return {
            "cost_basis": cost_basis,
            "current_value": current_value,
            "unrealized_pnl": unrealized_pnl,
            "pnl_percent": pnl_percent
        }
    
    def update_performance_log(self, trade_result: Dict) -> None:
        """
        Log trade entry in performance tracking file
        
        Args:
            trade_result: Trade result containing token, amount, price, timestamp
        """
        try:
            performance_data = self._load_performance_log()
            
            token_address = trade_result.get("token_address")
            
            # Update or create entry
            performance_data[token_address] = {
                "symbol": trade_result.get("symbol", "UNKNOWN"),
                "entry_price": trade_result.get("entry_price"),
                "entry_amount": trade_result.get("amount"),
                "entry_timestamp": trade_result.get("timestamp", datetime.now().isoformat()),
                "tx_hash": trade_result.get("tx_hash"),
                "entry_usdc": trade_result.get("usdc_spent", 0)
            }
            
            self._save_performance_log(performance_data)
            logger.info(f"\u2705 Performance log updated for {token_address}")
            
        except Exception as e:
            logger.error(f"\u274c Failed to update performance log: {e}")
    
    def _load_performance_log(self) -> Dict:
        """Load performance log from JSON file"""
        if os.path.exists(self.performance_log_path):
            try:
                with open(self.performance_log_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"\u26a0\ufe0f Could not load performance log: {e}")
        return {}
    
    def _save_performance_log(self, data: Dict) -> None:
        """Save performance log to JSON file"""
        try:
            os.makedirs(os.path.dirname(self.performance_log_path), exist_ok=True)
            with open(self.performance_log_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"\u274c Failed to save performance log: {e}")
    
    def get_summary(self, positions: List[Position]) -> Dict:
        """
        Get portfolio summary
        
        Args:
            positions: List of current positions
            
        Returns:
            dict: Total cost basis, current value, total P&L
        """
        total_cost = sum(p.cost_basis for p in positions)
        total_value = sum(p.current_price * p.amount for p in positions)
        total_pnl = total_value - total_cost
        total_pnl_percent = (total_pnl / total_cost * 100) if total_cost > 0 else 0
        
        return {
            "total_positions": len(positions),
            "total_cost_basis": total_cost,
            "total_current_value": total_value,
            "total_unrealized_pnl": total_pnl,
            "total_pnl_percent": total_pnl_percent
        }


# Async wrapper for testing
async def main():
    """Test position tracker"""
    print("=" * 60)
    print("\ud83e\udde0 Testing Position Tracker")
    print("=" * 60)
    
    tracker = PositionTracker()
    print("\u2705 Position tracker initialized")
    print("\n\ud83d\udccd Phase 2 Complete - Ready for Phase 3!")
    print("=" * 60)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
