"""
Base Token Swap Module - CDP Trade API Integration
Handles token buy/sell operations on Base chain using Coinbase Trade API
"""

import os
from typing import Dict, Optional
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
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '⚙️ Configuration', 'config', '.env'))

# Base chain token addresses
WETH_BASE = "0x4200000000000000000000000000000000000006"
USDC_BASE = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"


class BaseSwapModule:
    """
    Manages token swaps on Base chain using CDP Trade API
    """
    
    def __init__(self):
        """Initialize CDP client for Trade API"""
        # CDP client auto-loads from CDP_API_KEY_ID and CDP_API_KEY_SECRET env vars
        self.cdp = CdpClient()
        self.network = "base"
        logger.info("✅ Trade API client initialized")
    
    async def get_quote(self, 
                       from_token: str, 
                       to_token: str, 
                       amount: float,
                       taker_address: str) -> Dict:
        """
        Get swap price quote without executing
        
        Args:
            from_token: Token address to swap from
            to_token: Token address to swap to
            amount: Amount in smallest unit (wei for ETH, 6 decimals for USDC)
            taker_address: Wallet address executing swap
            
        Returns:
            dict: Price quote with toAmount, minToAmount, liquidityAvailable
        """
        try:
            swap_price = await self.cdp.evm.getSwapPrice({
                "fromToken": from_token,
                "toToken": to_token,
                "fromAmount": int(amount),
                "network": self.network,
                "taker": taker_address
            })
            
            if swap_price.get("liquidityAvailable"):
                logger.info(f"💰 Quote: {amount} → {swap_price.get('toAmount')} "
                          f"(min: {swap_price.get('minToAmount')})")
                return swap_price
            else:
                logger.warning("⚠️ Insufficient liquidity")
                return {"liquidityAvailable": False}
                
        except Exception as e:
            logger.error(f"❌ Failed to get quote: {e}")
            raise
    
    async def buy_token(self,
                       token_address: str,
                       amount_usdc: float,
                       slippage_bps: int = 100) -> Dict:
        """
        Buy token with USDC using Trade API
        
        Args:
            token_address: Contract address of token to buy
            amount_usdc: Amount of USDC to spend (in USDC, not wei)
            slippage_bps: Slippage tolerance in basis points (100 = 1%)
            
        Returns:
            dict: Swap result with transaction hash
        """
        # Convert USDC amount to smallest unit (6 decimals)
        amount_in_wei = int(amount_usdc * 1_000_000)
        
        try:
            # Get or create CDP account
            account = await self.cdp.evm.getOrCreateAccount({"name": "BaseOPSTrading"})
            
            # Create swap quote
            swap_quote = await account.quoteSwap({
                "network": self.network,
                "fromToken": USDC_BASE,
                "toToken": token_address,
                "fromAmount": amount_in_wei,
                "slippageBps": slippage_bps
            })
            
            if not swap_quote.get("liquidityAvailable"):
                raise ValueError("Insufficient liquidity for swap")
            
            logger.info(f"📊 Buying token with {amount_usdc} USDC")
            logger.info(f"   Expected: {swap_quote.get('toAmount')} tokens")
            logger.info(f"   Minimum: {swap_quote.get('minToAmount')} tokens")
            
            # Execute swap
            swap_result = await account.executeSwap(swap_quote)
            
            logger.info(f"✅ Buy executed: {swap_result.get('transactionHash')}")
            return swap_result
            
        except Exception as e:
            logger.error(f"❌ Buy failed: {e}")
            raise
    
    async def sell_token(self,
                        token_address: str,
                        amount_tokens: float,
                        token_decimals: int = 18,
                        slippage_bps: int = 100) -> Dict:
        """
        Sell token for USDC using Trade API
        
        Args:
            token_address: Contract address of token to sell
            amount_tokens: Amount of tokens to sell (in token units)
            token_decimals: Token decimal places (default 18)
            slippage_bps: Slippage tolerance in basis points (100 = 1%)
            
        Returns:
            dict: Swap result with transaction hash
        """
        # Convert token amount to smallest unit
        amount_in_wei = int(amount_tokens * (10 ** token_decimals))
        
        try:
            # Get or create CDP account
            account = await self.cdp.evm.getOrCreateAccount({"name": "BaseOPSTrading"})
            
            # Create swap quote
            swap_quote = await account.quoteSwap({
                "network": self.network,
                "fromToken": token_address,
                "toToken": USDC_BASE,
                "fromAmount": amount_in_wei,
                "slippageBps": slippage_bps
            })
            
            if not swap_quote.get("liquidityAvailable"):
                raise ValueError("Insufficient liquidity for swap")
            
            usdc_out = swap_quote.get('toAmount', 0) / 1_000_000  # Convert from wei
            logger.info(f"📊 Selling {amount_tokens} tokens")
            logger.info(f"   Expected USDC: ${usdc_out:.2f}")
            
            # Execute swap
            swap_result = await account.executeSwap(swap_quote)
            
            logger.info(f"✅ Sell executed: {swap_result.get('transactionHash')}")
            return swap_result
            
        except Exception as e:
            logger.error(f"❌ Sell failed: {e}")
            raise
    
    def calculate_position_size(self,
                               account_balance: float,
                               risk_percent: float,
                               token_price_usdc: float) -> float:
        """
        Calculate position size based on risk management
        
        Args:
            account_balance: Total USDC balance
            risk_percent: Risk per trade (0.20 = 20%)
            token_price_usdc: Current token price in USDC
            
        Returns:
            float: Amount of USDC to allocate
        """
        max_risk_amount = account_balance * risk_percent
        
        # Don't exceed max 3 positions (reserve 1/3 for each)
        position_limit = account_balance / 3
        
        usdc_allocation = min(max_risk_amount, position_limit)
        
        logger.info(f"💼 Position sizing:")
        logger.info(f"   Account: ${account_balance:.2f}")
        logger.info(f"   Max risk ({risk_percent*100}%): ${max_risk_amount:.2f}")
        logger.info(f"   Allocated: ${usdc_allocation:.2f}")
        
        return usdc_allocation


# Async wrapper for testing
async def main():
    """Test Trade API connection"""
    print("=" * 60)
    print("🧪 Testing Trade API Swap Module")
    print("=" * 60)
    
    swap_module = BaseSwapModule()
    print("✅ Swap module initialized")
    print("\n📍 Trade API ready for Phase 2 implementation")
    print("=" * 60)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
