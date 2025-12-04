"""
Base (Coinbase CDP) Client - Production Trading
Uses cdp-sdk for on-chain swaps on Base L2
"""

import os
from typing import Dict, Optional
from dataclasses import dataclass
import logging
from dotenv import load_dotenv

from . import load_base_config

logger = logging.getLogger(__name__)

try:
    from cdp import Cdp, Wallet
except ImportError:
    raise ImportError("Install: pip install cdp-sdk")


@dataclass
class BaseSwap:
    from_asset: str      # e.g., "eth", "usdc"
    to_asset: str        # e.g., "usdc", "eth"
    amount: float        # Amount of from_asset
    slippage: float = 0.01


class BaseClient:
    """Production Base/Coinbase CDP client - MAINNET ONLY"""
    
    def __init__(self):
        self.config = load_base_config()
        self.wallet: Optional[Wallet] = None
        self._initialized = False
    
    def connect(self) -> bool:
        """Initialize connection to Coinbase CDP"""
        try:
            Cdp.configure(
                api_key_name=f"organizations/default/apiKeys/{self.config['api_key_id']}",
                private_key=self.config['api_key_secret']
            )
            self._initialized = True
            logger.info(f"Base CDP connected: {self.config['network']}")
            return True
        except Exception as e:
            logger.error(f"Base CDP connection failed: {e}")
            return False
    
    def create_wallet(self) -> str:
        """Create a new MPC wallet"""
        if not self._initialized:
            raise RuntimeError("Client not connected. Call connect() first.")
        
        self.wallet = Wallet.create(network_id=self.config["network"])
        address = self.wallet.default_address.address_id
        logger.info(f"Created wallet: {address}")
        return address
    
    def import_wallet(self, wallet_data: Dict) -> str:
        """Import existing wallet from export data"""
        if not self._initialized:
            raise RuntimeError("Client not connected. Call connect() first.")
        
        self.wallet = Wallet.import_data(wallet_data)
        address = self.wallet.default_address.address_id
        logger.info(f"Imported wallet: {address}")
        return address
    
    def get_address(self) -> str:
        """Get current wallet address"""
        if not self.wallet:
            raise RuntimeError("No wallet loaded. Create or import first.")
        return self.wallet.default_address.address_id
    
    def get_balance(self, asset: str = "eth") -> float:
        """Get balance of specific asset"""
        if not self.wallet:
            raise RuntimeError("No wallet loaded. Create or import first.")
        
        try:
            balance = self.wallet.balance(asset)
            return float(balance)
        except Exception as e:
            logger.error(f"Failed to get {asset} balance: {e}")
            return 0.0
    
    def get_all_balances(self) -> Dict[str, float]:
        """Get all asset balances"""
        if not self.wallet:
            raise RuntimeError("No wallet loaded. Create or import first.")
        
        try:
            balances = self.wallet.balances()
            return {
                asset_id: float(balance.amount)
                for asset_id, balance in balances.items()
            }
        except Exception as e:
            logger.error(f"Failed to get balances: {e}")
            return {}
    
    def swap(self, swap: BaseSwap) -> Dict:
        """
        Execute swap on Base chain
        
        Args:
            swap: BaseSwap specification
            
        Returns:
            Dict with status, tx_hash, or error
        """
        if not self.wallet:
            raise RuntimeError("No wallet loaded. Create or import first.")
        
        try:
            trade = self.wallet.trade(
                amount=swap.amount,
                from_asset_id=swap.from_asset,
                to_asset_id=swap.to_asset,
            )
            
            trade.wait()
            
            logger.info(f"Base swap complete: {swap.amount} {swap.from_asset} -> {swap.to_asset}")
            return {
                "status": "ok",
                "tx_hash": trade.transaction_hash,
                "from_asset": swap.from_asset,
                "to_asset": swap.to_asset,
                "amount": swap.amount,
            }
            
        except Exception as e:
            logger.error(f"Base swap failed: {e}")
            return {"status": "error", "error": str(e)}
    
    def transfer(self, to_address: str, amount: float, asset: str = "eth") -> Dict:
        """Transfer asset to another address"""
        if not self.wallet:
            raise RuntimeError("No wallet loaded. Create or import first.")
        
        try:
            transfer = self.wallet.transfer(
                amount=amount,
                asset_id=asset,
                destination=to_address,
            )
            
            transfer.wait()
            
            logger.info(f"Base transfer complete: {amount} {asset} -> {to_address[:10]}...")
            return {
                "status": "ok",
                "tx_hash": transfer.transaction_hash,
                "to": to_address,
                "amount": amount,
                "asset": asset,
            }
            
        except Exception as e:
            logger.error(f"Base transfer failed: {e}")
            return {"status": "error", "error": str(e)}
    
    def export_wallet(self) -> Dict:
        """Export wallet data for backup"""
        if not self.wallet:
            raise RuntimeError("No wallet loaded.")
        
        return self.wallet.export_data()


def test_connection():
    """Test Base CDP connection"""
    client = BaseClient()
    if client.connect():
        print("Connected to Base CDP")
        print(f"Network: {client.config['network']}")
        print("Note: Create or import wallet to check balances")
    else:
        print("Connection failed")


if __name__ == "__main__":
    test_connection()
