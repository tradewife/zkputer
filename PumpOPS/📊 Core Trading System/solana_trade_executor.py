import os
import json
import logging
from typing import Dict, Any, Optional
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.api import Client
from solana.rpc.api import Client
from solders.transaction import Transaction
from spl.token.instructions import get_associated_token_address
from .jupiter_swap_module import JupiterSwapModule

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SolanaTradeExecutor")

class SolanaTradeExecutor:
    def __init__(self, config_path: str = None):
        if config_path is None:
            # Default to absolute path based on project structure
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(base_dir, "⚙️ Configuration", "config", "trading_config.json")
        
        self.config = self._load_config(config_path)
        self.rpc_url = self.config.get("rpc_url", "https://api.mainnet-beta.solana.com")
        self.client = Client(self.rpc_url)
        self.keypair = self._load_wallet()
        self.jupiter = JupiterSwapModule(self.config.get("jupiter_api_url", "https://quote-api.jup.ag/v6"))

    def _load_config(self, path: str) -> Dict[str, Any]:
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {}

    def _load_wallet(self) -> Optional[Keypair]:
        # TODO: Implement secure wallet loading from env or file
        # For now, this is a placeholder
        private_key = os.getenv("SOLANA_PRIVATE_KEY")
        if private_key:
            try:
                return Keypair.from_base58_string(private_key)
            except Exception as e:
                logger.error(f"Failed to load wallet: {e}")
        return None

    def get_balance(self) -> float:
        if not self.keypair:
            return 0.0
        try:
            balance = self.client.get_balance(self.keypair.pubkey())
            return balance.value / 1e9
        except Exception as e:
            logger.error(f"Failed to get balance: {e}")
            return 0.0

    def execute_buy(self, token_address: str, amount_sol: float) -> Optional[str]:
        """
        Execute a BUY order (SOL -> Token) using Jupiter.
        """
        logger.info(f"Executing BUY for {token_address} with {amount_sol} SOL")
        
        if not self.keypair:
            logger.error("No wallet loaded. Cannot execute trade.")
            return None

        try:
            # 1. Get Quote
            # SOL Mint: So11111111111111111111111111111111111111112
            sol_mint = "So11111111111111111111111111111111111111112"
            amount_lamports = int(amount_sol * 1e9)
            
            quote = self.jupiter.get_quote(
                input_mint=sol_mint,
                output_mint=token_address,
                amount=amount_lamports,
                slippage_bps=self.config.get("slippage_bps", 50)
            )
            
            if not quote:
                logger.error("Failed to get quote from Jupiter")
                return None

            # 2. Get Swap Transaction
            swap_tx_base64 = self.jupiter.get_swap_transaction(
                quote_response=quote,
                user_public_key=str(self.keypair.pubkey())
            )
            
            if not swap_tx_base64:
                logger.error("Failed to get swap transaction from Jupiter")
                return None

            # 3. Deserialize, Sign and Send
            # Jupiter returns a base64 encoded VersionedTransaction
            import base64
            from solders.transaction import VersionedTransaction
            
            tx_bytes = base64.b64decode(swap_tx_base64)
            transaction = VersionedTransaction.from_bytes(tx_bytes)
            
            # Sign the transaction
            # Note: VersionedTransaction signing is different from legacy
            # We need to create a signature and set it
            signature = self.keypair.sign_message(transaction.message.to_bytes_versioned(transaction.message))
            signed_tx = VersionedTransaction.populate(transaction.message, [signature])

            # Send transaction
            opts = self.client.commitment
            result = self.client.send_transaction(signed_tx, opts=opts)
            
            tx_sig = str(result.value)
            logger.info(f"✅ Buy Transaction Sent: {tx_sig}")
            return tx_sig

        except Exception as e:
            logger.error(f"❌ Buy Execution Failed: {e}")
            return None

    def execute_sell(self, token_address: str, percentage: float) -> Optional[str]:
        """
        Execute a SELL order (Token -> SOL) using Jupiter.
        """
        logger.info(f"Executing SELL for {token_address} ({percentage}%)")
        
        if not self.keypair:
            logger.error("No wallet loaded. Cannot execute trade.")
            return None

        try:
            # 1. Get Token Balance
            # We need to find the specific token account for this mint
            # This is a simplified check, in production use get_token_accounts_by_owner
            # For now, we assume we can get the balance if we implemented a full balance checker
            # But since we don't have that yet, we'll fail if we can't determine amount
            
            # TODO: Implement robust token balance check
            # For now, we will assume the user knows what they are doing or fail gracefully
            logger.warning("Token balance check not fully implemented. Proceeding with caution.")
            
            # Placeholder: We need the actual token amount to sell. 
            # Without a balance check, we can't calculate 'percentage'.
            # This requires an RPC call to get_token_accounts_by_owner
            
            from spl.token.instructions import get_associated_token_address
            
            # Get ATA
            token_pubkey = Pubkey.from_string(token_address)
            ata = get_associated_token_address(self.keypair.pubkey(), token_pubkey)
            
            # Get Balance of ATA
            balance_resp = self.client.get_token_account_balance(ata)
            if not balance_resp.value:
                logger.error("No balance found for token")
                return None
                
            total_amount = int(balance_resp.value.amount)
            amount_to_sell = int(total_amount * (percentage / 100))
            
            if amount_to_sell == 0:
                logger.error("Amount to sell is 0")
                return None

            # 2. Get Quote
            sol_mint = "So11111111111111111111111111111111111111112"
            
            quote = self.jupiter.get_quote(
                input_mint=token_address,
                output_mint=sol_mint,
                amount=amount_to_sell,
                slippage_bps=self.config.get("slippage_bps", 50)
            )
            
            if not quote:
                logger.error("Failed to get quote from Jupiter")
                return None

            # 3. Get Swap Transaction
            swap_tx_base64 = self.jupiter.get_swap_transaction(
                quote_response=quote,
                user_public_key=str(self.keypair.pubkey())
            )
            
            if not swap_tx_base64:
                logger.error("Failed to get swap transaction from Jupiter")
                return None

            # 4. Deserialize, Sign and Send
            import base64
            from solders.transaction import VersionedTransaction
            
            tx_bytes = base64.b64decode(swap_tx_base64)
            transaction = VersionedTransaction.from_bytes(tx_bytes)
            
            signature = self.keypair.sign_message(transaction.message.to_bytes_versioned(transaction.message))
            signed_tx = VersionedTransaction.populate(transaction.message, [signature])

            result = self.client.send_transaction(signed_tx)
            
            tx_sig = str(result.value)
            logger.info(f"✅ Sell Transaction Sent: {tx_sig}")
            return tx_sig

        except Exception as e:
            logger.error(f"❌ Sell Execution Failed: {e}")
            return None
