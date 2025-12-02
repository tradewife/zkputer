"""
Position Tracker - Solana Account Balance and P&L Monitoring
Tracks token positions and calculates performance using Solana RPC
"""

import os
import json
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
from solana.rpc.api import Client
from solders.pubkey import Pubkey
from spl.token.instructions import get_associated_token_address

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SolanaPositionTracker")

@dataclass
class Position:
    """Token position data structure"""
    token_address: str
    symbol: str
    amount: float
    entry_price: float  # From performance log
    current_price: float  # Live from Jupiter/Birdeye (Mock for now)
    unrealized_pnl: float
    pnl_percent: float
    cost_basis: float

class PositionTracker:
    def __init__(self, rpc_url: str = "https://api.mainnet-beta.solana.com"):
        self.client = Client(rpc_url)
        self.performance_log_path = os.path.join(
            os.path.dirname(__file__), 
            '..', 
            '🧠 Learning Engine', 
            'knowledge_graph',
            'performance_log.md'
        )
        self.state_file = os.path.join(os.path.dirname(__file__), "positions.json")
        logger.info("✅ Solana Position Tracker initialized")

    def get_balance(self, wallet_address: str, token_mint: str) -> float:
        """Get balance for SOL or SPL token"""
        try:
            if token_mint == "So11111111111111111111111111111111111111112":
                # Native SOL
                resp = self.client.get_balance(Pubkey.from_string(wallet_address))
                return resp.value / 1e9
            
            # SPL Token - Get ATA
            ata = get_associated_token_address(
                Pubkey.from_string(wallet_address), 
                Pubkey.from_string(token_mint)
            )
            resp = self.client.get_token_account_balance(ata)
            if resp.value:
                return float(resp.value.amount) / (10 ** resp.value.decimals)
            return 0.0
        except Exception as e:
            logger.error(f"Failed to get balance for {token_mint}: {e}")
            return 0.0

    def load_positions(self) -> Dict:
        """Load positions from JSON state file"""
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {}

    def save_positions(self, positions: Dict):
        """Save positions to JSON state file"""
        with open(self.state_file, 'w') as f:
            json.dump(positions, f, indent=2)

    def update_position(self, token_mint: str, symbol: str, entry_price: float, amount: float):
        """Update or create a position with weighted average entry price"""
        positions = self.load_positions()
        
        if token_mint not in positions:
            positions[token_mint] = {
                "symbol": symbol,
                "entry_price": entry_price,
                "amount": amount,
                "timestamp": datetime.now().isoformat()
            }
        else:
            # Weighted average entry price
            current = positions[token_mint]
            total_cost = (current["entry_price"] * current["amount"]) + (entry_price * amount)
            new_amount = current["amount"] + amount
            positions[token_mint]["entry_price"] = total_cost / new_amount if new_amount > 0 else 0
            positions[token_mint]["amount"] = new_amount
            
        self.save_positions(positions)
        logger.info(f"✅ Updated position for {symbol} ({token_mint})")

    def calculate_pnl(self, entry_price: float, current_price: float, amount: float) -> Dict:
        """Calculate P&L for a position"""
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

    def get_all_positions(self, wallet_address: str) -> List[Position]:
        """Get all positions with live balances and P&L"""
        positions_data = self.load_positions()
        positions = []
        
        for token_mint, data in positions_data.items():
            # Get live balance
            live_balance = self.get_balance(wallet_address, token_mint)
            
            if live_balance > 0:
                # TODO: Fetch current price from Jupiter/Birdeye
                current_price = data["entry_price"]  # Mock for now
                
                pnl = self.calculate_pnl(
                    data["entry_price"],
                    current_price,
                    live_balance
                )
                
                position = Position(
                    token_address=token_mint,
                    symbol=data["symbol"],
                    amount=live_balance,
                    entry_price=data["entry_price"],
                    current_price=current_price,
                    unrealized_pnl=pnl["unrealized_pnl"],
                    pnl_percent=pnl["pnl_percent"],
                    cost_basis=pnl["cost_basis"]
                )
                positions.append(position)
        
        return positions

if __name__ == "__main__":
    tracker = PositionTracker()
    print("✅ Solana Position Tracker Initialized")
    print("📊 Ready to track positions on Solana")
