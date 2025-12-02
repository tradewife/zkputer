"""
CDP Client - Coinbase Developer Platform Integration
Manages wallet creation, initialization, and Base chain connection
"""

import os
import json
from typing import Optional, Dict
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
load_dotenv()


class CDPClient:
    """
    Manages Coinbase Developer Platform connection and wallet operations
    """
    
    def __init__(self, network: str = "base-mainnet"):
        """
        Initialize CDP client
        
        Args:
            network: Network to use (base-mainnet or base-sepolia)
        """
        self.network = network
        self.wallet: Optional[Wallet] = None
        
        # Load CDP credentials from environment
        api_key_name = os.getenv("CDP_API_KEY_NAME")
        private_key = os.getenv("CDP_PRIVATE_KEY")
        
        if not api_key_name or not private_key:
            raise ValueError(
                "CDP_API_KEY_NAME and CDP_PRIVATE_KEY must be set in .env file. "
                "Get these from portal.cdp.coinbase.com"
            )
        
        # Configure CDP SDK
        try:
            Cdp.configure(api_key_name, private_key)
            logger.info(f"✅ CDP configured for {network}")
        except Exception as e:
            logger.error(f"❌ Failed to configure CDP: {e}")
            raise
    
    def create_wallet(self) -> Wallet:
        """
        Create a new MPC wallet on Base chain
        
        Returns:
            Wallet: New CDP wallet instance
        """
        try:
            self.wallet = Wallet.create(network_id=self.network)
            logger.info(f"✅ Created new wallet: {self.wallet.default_address.address_id}")
            return self.wallet
        except Exception as e:
            logger.error(f"❌ Failed to create wallet: {e}")
            raise
    
    def import_wallet(self, wallet_data: str) -> Wallet:
        """
        Import existing wallet from seed/export data
        
        Args:
            wallet_data: Wallet export data (JSON string)
            
        Returns:
            Wallet: Imported CDP wallet instance
        """
        try:
            wallet_dict = json.loads(wallet_data)
            self.wallet = Wallet.import_data(wallet_dict)
            logger.info(f"✅ Imported wallet: {self.wallet.default_address.address_id}")
            return self.wallet
        except Exception as e:
            logger.error(f"❌ Failed to import wallet: {e}")
            raise
    
    def export_wallet(self) -> str:
        """
        Export wallet data for backup
        
        Returns:
            str: Wallet export data (JSON string)
        """
        if not self.wallet:
            raise ValueError("No wallet loaded. Create or import a wallet first.")
        
        try:
            wallet_data = self.wallet.export_data()
            logger.info("✅ Wallet exported successfully")
            return json.dumps(wallet_data)
        except Exception as e:
            logger.error(f"❌ Failed to export wallet: {e}")
            raise
    
    def get_address(self) -> str:
        """
        Get wallet's Base address
        
        Returns:
            str: Wallet address (0x...)
        """
        if not self.wallet:
            raise ValueError("No wallet loaded. Create or import a wallet first.")
        
        return self.wallet.default_address.address_id
    
    def get_balance(self, asset_id: str = "eth") -> float:
        """
        Get balance of specific asset in wallet
        
        Args:
            asset_id: Asset to check (eth, usdc, or token contract address)
            
        Returns:
            float: Balance amount
        """
        if not self.wallet:
            raise ValueError("No wallet loaded. Create or import a wallet first.")
        
        try:
            balance = self.wallet.balance(asset_id)
            logger.info(f"💰 {asset_id.upper()} balance: {balance}")
            return float(balance)
        except Exception as e:
            logger.error(f"❌ Failed to get balance: {e}")
            return 0.0
    
    def get_all_balances(self) -> Dict[str, float]:
        """
        Get all asset balances in wallet
        
        Returns:
            dict: Asset ID -> balance mapping
        """
        if not self.wallet:
            raise ValueError("No wallet loaded. Create or import a wallet first.")
        
        try:
            balances = self.wallet.balances()
            balance_dict = {
                asset_id: float(balance.amount) 
                for asset_id, balance in balances.items()
            }
            logger.info(f"📊 Wallet balances: {balance_dict}")
            return balance_dict
        except Exception as e:
            logger.error(f"❌ Failed to get balances: {e}")
            return {}


def create_sample_config():
    """Create sample .env file for CDP configuration"""
    sample_env = """# Coinbase Developer Platform Configuration
# Get these credentials from portal.cdp.coinbase.com

# CDP API Credentials
CDP_API_KEY_NAME=organizations/{org_id}/apiKeys/{key_id}
CDP_PRIVATE_KEY=-----BEGIN EC PRIVATE KEY-----\\n...\\n-----END EC PRIVATE KEY-----

# Optional: Basescan API for contract verification
BASESCAN_API_KEY=your_basescan_api_key_here

# Network (base-mainnet or base-sepolia for testnet)
CDP_NETWORK=base-mainnet
"""
    
    with open(".env.example", "w") as f:
        f.write(sample_env)
    
    logger.info("✅ Created .env.example - Copy to .env and add your CDP credentials")


if __name__ == "__main__":
    # Example usage
    print("CDP Client Module")
    print("=" * 50)
    
    # Create sample config
    create_sample_config()
    
    print("\n📝 Next steps:")
    print("1. Copy .env.example to .env")
    print("2. Go to portal.cdp.coinbase.com and create API keys")
    print("3. Add your API key name and private key to .env")
    print("4. Run this module again to test wallet creation")
