"""
ZKputer Trade Executor
Wraps BaseOPS CDP trading and HyperOPS perpetuals with NEAR AI intelligence
"""
import sys
import os

# Add BaseOPS to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../BaseOPS/📊 Core Trading System'))

try:
    from base_trade_executor import BaseTradeExecutor, TokenPick
    BASEOPS_AVAILABLE = True
except ImportError:
    BASEOPS_AVAILABLE = False
    print("Warning: BaseOPS trade executor not available")

try:
    from hyperliquid.exchange import Exchange
    HYPEROPS_AVAILABLE = True
except ImportError:
    HYPEROPS_AVAILABLE = False
    print("Warning: Hyperliquid SDK not available")


# Import NEAR AI agent
try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
    from near_ai_agent import NEARAIAgent
    NEAR_AI_AVAILABLE = True
except ImportError:
    NEAR_AI_AVAILABLE = False
    print("Warning: NEAR AI agent not available")


class ZKputerTradeExecutor:
    """Unified trade executor for Base and Hyperliquid via Near Intents + NEAR AI"""
    
    def __init__(self, zcash_wallet=None, near_intents_client=None, enable_near_ai=True):
        self.base_executor = BaseTradeExecutor() if BASEOPS_AVAILABLE else None
        self.hyper_exchange = None
        self.zcash_wallet = zcash_wallet
        self.near_intents = near_intents_client
        
        # Initialize NEAR AI agent
        if enable_near_ai and NEAR_AI_AVAILABLE:
            self.near_ai = NEARAIAgent(zkputer_executor=self)
            print("✅ NEAR AI-powered trading enabled")
        else:
            self.near_ai = None
    
    def execute_zec_to_base_trade(self, token_symbol, token_address, zec_amount):
        """
        Full flow: ZEC → Near Intents → USDC on Base → Buy Token
        
        This is the key innovation:
        1. User has shielded ZEC in Zcash wallet
        2. Near Intents converts ZEC → USDC via Maya Protocol
        3. USDC arrives on Base chain
        4. CDP Trade API executes token purchase
        
        Args:
            token_symbol: Target token (e.g., "DEGEN")
            token_address: Token contract on Base
            zec_amount: Amount of ZEC to spend
        
        Returns:
            dict with full execution details
        """
        if not self.near_intents:
            return {"status": "error", "error": "Near Intents not configured"}
        
        try:
            # Step 1: Get ZEC balance
            zec_balance = self.zcash_wallet.get_balance() if self.zcash_wallet else 0
            if zec_balance < zec_amount:
                return {"status": "error", "error": f"Insufficient ZEC. Have: {zec_balance}, Need: {zec_amount}"}
            
            # Step 2: Near Intents - ZEC → USDC on Base
            print(f"[1/3] Converting {zec_amount} ZEC → USDC via Near Intents...")
            
            # Get user's Base address (would come from config)
            base_address = "0x..."  # TODO: Get from user config
            
            swap_result = self.near_intents.execute_swap(
                from_token="ZEC",
                to_token="USDC",
                amount=zec_amount,
                user_address=base_address,
                from_chain="zcash",
                to_chain="base"
            )
            
            if not swap_result or swap_result.get("status") != "completed":
                return {"status": "error", "error": "Near Intents swap failed", "details": swap_result}
            
            usdc_received = swap_result.get("to_amount", 0)
            print(f"[2/3] Received {usdc_received} USDC on Base")
            
            # Step 3: Execute Base token purchase with USDC
            print(f"[3/3] Buying {token_symbol} with USDC...")
            
            trade_result = self.execute_base_trade(
                token_symbol=token_symbol,
                token_address=token_address,
                usdc_amount=usdc_received
            )
            
            return {
                "status": "success",
                "flow": "ZEC → Near Intents → USDC → Base Token",
                "zec_spent": zec_amount,
                "usdc_received": usdc_received,
                "token_bought": token_symbol,
                "swap_tx": swap_result.get("tx_hash"),
                "trade_tx": trade_result.get("tx_hash")
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def execute_zec_to_hyperliquid_trade(self, symbol, side, zec_amount, leverage=10):
        """
        Full flow: ZEC → Near Intents → USDC on Hyperliquid → Open Position
        
        Args:
            symbol: Perpetual symbol (e.g., "BTC")
            side: "buy" or "sell"
            zec_amount: Amount of ZEC to spend
            leverage: Leverage multiplier
        
        Returns:
            dict with execution details
        """
        if not self.near_intents:
            return {"status": "error", "error": "Near Intents not configured"}
        
        try:
            # Step 1: Near Intents - ZEC → USDC on Hyperliquid
            print(f"[1/2] Converting {zec_amount} ZEC → USDC on Hyperliquid...")
            
            # Hyperliquid address (would come from config)
            hyper_address = "0x..."  # TODO: Get from user config
            
            swap_result = self.near_intents.execute_swap(
                from_token="ZEC",
                to_token="USDC",
                amount=zec_amount,
                user_address=hyper_address,
                from_chain="zcash",
                to_chain="arbitrum"  # Hyperliquid uses Arbitrum for deposits
            )
            
            if not swap_result or swap_result.get("status") != "completed":
                return {"status": "error", "error": "Near Intents swap failed"}
            
            usdc_received = swap_result.get("to_amount", 0)
            print(f"[2/2] Opening {symbol} {side.upper()} position with {usdc_received} USDC @ {leverage}x...")
            
            # Step 2: Execute Hyperliquid trade
            trade_result = self.execute_hyper_trade(
                symbol=symbol,
                side=side,
                size=usdc_received * leverage,
                leverage=leverage
            )
            
            return {
                "status": "success",
                "flow": "ZEC → Near Intents → USDC → Hyperliquid Position",
                "zec_spent": zec_amount,
                "usdc_received": usdc_received,
                "position": f"{symbol} {side.upper()} @ {leverage}x",
                "swap_tx": swap_result.get("tx_hash"),
                "order_id": trade_result.get("order_id")
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
        
    def execute_base_trade(self, token_symbol, token_address, usdc_amount):
        """
        Execute Base chain trade via CDP
        
        Args:
            token_symbol: Token symbol (e.g., "DEGEN")
            token_address: Token contract address
            usdc_amount: Amount of USDC to spend
        
        Returns:
            dict with status and tx_hash
        """
        if not BASEOPS_AVAILABLE:
            return {"status": "error", "error": "BaseOPS not available"}
        
        try:
            # Create token pick
            pick = TokenPick(
                symbol=token_symbol,
                token_address=token_address,
                action="buy",
                usdc_allocation=usdc_amount,
                conviction="MEDIUM",
                thesis="ZKputer automated trade",
                risk_score=50.0
            )
            
            # Prepare and execute
            import asyncio
            prepared = asyncio.run(self.base_executor.prepare_trades([pick]))
            
            if not prepared:
                return {"status": "error", "error": "Failed to prepare trade"}
            
            result = asyncio.run(self.base_executor.execute_trade(0))
            return result
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def execute_hyper_trade(self, symbol, side, size, leverage=10):
        """
        Execute Hyperliquid perpetual trade
        
        Args:
            symbol: Perpetual symbol (e.g., "BTC")
            side: "buy" or "sell"
            size: Position size in USD
            leverage: Leverage multiplier
        
        Returns:
            dict with status and order_id
        """
        if not HYPEROPS_AVAILABLE:
            return {"status": "error", "error": "Hyperliquid SDK not available"}
        
        try:
            # Initialize exchange if needed
            if not self.hyper_exchange:
                # Would need private key from env
                return {"status": "error", "error": "Hyperliquid not configured"}
            
            # Place order
            # This is a placeholder - actual implementation would use Exchange.order()
            return {"status": "simulated", "message": "Hyperliquid trade simulation"}
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
