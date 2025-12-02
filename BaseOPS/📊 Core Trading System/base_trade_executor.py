"""
BaseOPS Trade Execution Module
Handles user-authorized token trading execution via CDP Trade API
Mirrors HyperOPS pattern for consistency
"""

import asyncio
from typing import Dict, List, Optional
from dataclasses import dataclass
import logging

from cdp_swap_module import BaseSwapModule
from position_tracker import PositionTracker

logger = logging.getLogger(__name__)


@dataclass
class TokenPick:
    """Token research pick from BaseOPS analysis"""
    symbol: str
    token_address: str
    action: str  # "buy" or "sell"
    usdc_allocation: float  # Amount of USDC to spend/expect
    conviction: str  # "HIGH", "MEDIUM", "LOW"
    thesis: str  # Trading thesis from research
    risk_score: float  # 0-100 from BaseOPS scoring


class BaseTradeExecutor:
    """Handles user-authorized spot token trading on Base"""
    
    def __init__(self):
        """Initialize trade executor with CDP modules"""
        self.swap_module = BaseSwapModule()
        self.position_tracker = PositionTracker()
        self.pending_trades = []
        logger.info("✅ Trade executor initialized")
    
    async def prepare_trades(self, token_picks: List[TokenPick]) -> List[Dict]:
        """
        Prepare trades from BaseOPS research for user review
        
        Args:
            token_picks: List of tokens from BaseOPS analysis
            
        Returns:
            List of prepared trades with quotes
        """
        prepared_trades = []
        
        # Get account balance
        account = await self.swap_module.cdp.evm.getOrCreateAccount({"name": "BaseOPSTrading"})
        usdc_balance = await account.balance("usdc")
        usdc_balance_float = float(usdc_balance) / 1_000_000  # Convert from wei
        
        logger.info(f"💰 USDC Balance: ${usdc_balance_float:.2f}")
        
        for pick in token_picks:
            try:
                # Apply risk management
                allocation = self.swap_module.calculate_position_size(
                    account_balance=usdc_balance_float,
                    risk_percent=0.20,  # Max 20% per trade
                    token_price_usdc=pick.usdc_allocation  # Approximate
                )
                
                # Skip if allocation too small
                if allocation < 5.0:
                    logger.warning(f"⚠️ Skipping {pick.symbol}: Allocation too small (${allocation:.2f})")
                    continue
                
                # Get quote
                if pick.action == "buy":
                    # Quote buying token with USDC
                    amount_wei = int(allocation * 1_000_000)
                    
                    trade_info = {
                        "pick": pick,
                        "action": "buy",
                        "usdc_amount": allocation,
                        "amount_wei": amount_wei,
                        "expected_slippage_bps": 100,  # 1%
                        "status": "prepared"
                    }
                else:
                    # Selling - would need to check current holdings
                    logger.warning(f"⚠️ Sell not yet implemented for {pick.symbol}")
                    continue
                
                prepared_trades.append(trade_info)
                logger.info(f"📋 Prepared: {pick.action.upper()} {pick.symbol} with ${allocation:.2f}")
                
            except Exception as e:
                logger.error(f"❌ Failed to prepare {pick.symbol}: {e}")
        
        self.pending_trades = prepared_trades
        return prepared_trades
    
    async def execute_trade(self, trade_index: int) -> Dict:
        """
        Execute a specific prepared trade by index
        
        Args:
            trade_index: Index of trade in pending_trades (0-indexed)
            
        Returns:
            dict: Execution result with transaction hash
        """
        if trade_index >= len(self.pending_trades):
            return {"status": "error", "error": "Invalid trade index"}
        
        trade_info = self.pending_trades[trade_index]
        pick = trade_info["pick"]
        
        logger.info(f"🚀 Executing: {pick.action.upper()} {pick.symbol}")
        
        try:
            if trade_info["action"] == "buy":
                # Execute buy via Trade API
                result = await self.swap_module.buy_token(
                    token_address=pick.token_address,
                    amount_usdc=trade_info["usdc_amount"],
                    slippage_bps=trade_info["expected_slippage_bps"]
                )
                
                # Log to performance tracker
                self.position_tracker.update_performance_log({
                    "token_address": pick.token_address,
                    "symbol": pick.symbol,
                    "entry_price": trade_info["usdc_amount"],  # Approximate
                    "amount": result.get("toAmount", 0),
                    "tx_hash": result.get("transactionHash"),
                    "usdc_spent": trade_info["usdc_amount"]
                })
                
                return {
                    "status": "success",
                    "pick": pick,
                    "result": result,
                    "tx_hash": result.get("transactionHash")
                }
            else:
                return {"status": "error", "error": "Sell not yet implemented"}
                
        except Exception as e:
            logger.error(f"❌ Execution failed: {e}")
            return {"status": "error", "error": str(e)}
    
    async def execute_all_trades(self) -> List[Dict]:
        """
        Execute all prepared trades sequentially
        
        Returns:
            List of execution results
        """
        results = []
        
        for i in range(len(self.pending_trades)):
            result = await self.execute_trade(i)
            results.append(result)
            
            # Stop on failure to avoid cascade
            if result.get("status") != "success":
                logger.warning(f"⚠️ Stopping after trade {i+1} failure")
                break
            
            # Small delay between trades
            await asyncio.sleep(2)
        
        return results
    
    def get_pending_trades_summary(self) -> str:
        """
        Get formatted summary of pending trades for user review
        
        Returns:
            str: Markdown-formatted summary
        """
        if not self.pending_trades:
            return "No pending trades."
        
        summary = "🎯 **PENDING BASE TRADES**\n"
        summary += "=" * 50 + "\n\n"
        
        for i, trade_info in enumerate(self.pending_trades, 1):
            pick = trade_info["pick"]
            
            summary += f"**Trade {i}: {pick.action.upper()} {pick.symbol}**\n"
            summary += f"Thesis: {pick.thesis}\n"
            summary += f"Conviction: {pick.conviction}\n"
            summary += f"USDC Allocation: ${trade_info['usdc_amount']:.2f}\n"
            summary += f"Slippage Tolerance: {trade_info['expected_slippage_bps']/100}%\n"
            summary += f"Risk Score: {pick.risk_score:.1f}/100\n\n"
        
        summary += "**Available Commands:**\n"
        summary += f"- `Execute trade [1-{len(self.pending_trades)}]` - Execute specific trade\n"
        summary += "- `Execute all trades` - Execute all pending trades\n"
        summary += "- `Cancel pending trades` - Clear pending trades\n"
        summary += "- `Show positions` - View current holdings\n"
        
        return summary
    
    def cancel_pending_trades(self) -> None:
        """Clear all pending trades"""
        self.pending_trades = []
        logger.info("🚫 Pending trades cancelled")


# User command parser
def execute_user_command(command: str, executor: BaseTradeExecutor) -> str:
    """
    Execute user command for trade management
    
    Args:
        command: User command string
        executor: BaseTradeExecutor instance
        
    Returns:
        str: Result message
    """
    command = command.lower().strip()
    
    if "execute all" in command:
        results = asyncio.run(executor.execute_all_trades())
        success_count = sum(1 for r in results if r.get("status") == "success")
        return f"✅ Executed {success_count}/{len(results)} trades successfully"
    
    elif "execute trade" in command:
        try:
            # Extract trade number
            parts = command.split()
            trade_num = int(parts[-1]) - 1  # Convert to 0-indexed
            
            result = asyncio.run(executor.execute_trade(trade_num))
            if result.get("status") == "success":
                pick = result["pick"]
                tx_hash = result.get("tx_hash", "N/A")
                return f"✅ {pick.action.upper()} {pick.symbol} executed\nTX: {tx_hash}"
            else:
                return f"❌ Trade failed: {result.get('error')}"
        
        except (ValueError, IndexError):
            return "❌ Invalid trade number. Use: 'Execute trade 1'"
    
    elif "cancel" in command:
        executor.cancel_pending_trades()
        return "🚫 All pending trades cancelled"
    
    elif "show positions" in command or "positions" in command:
        positions = asyncio.run(executor.position_tracker.get_current_positions())
        if not positions:
            return "📭 No open positions"
        
        summary = "📊 **CURRENT POSITIONS**\n\n"
        for pos in positions:
            summary += f"{pos.symbol}: {pos.amount:.4f} tokens\n"
            summary += f"  P&L: ${pos.unrealized_pnl:.2f} ({pos.pnl_percent:.2f}%)\n\n"
        return summary
    
    elif "status" in command or "pending" in command:
        return executor.get_pending_trades_summary()
    
    else:
        return "❓ Unknown command. Available: 'Execute all', 'Execute trade [1-3]', 'Cancel', 'Show positions', 'Status'"


# Test
async def main():
    """Test trade executor"""
    print("=" * 60)
    print("Trade Executor - Testing")
    print("=" * 60)
    
    executor = BaseTradeExecutor()
    print("✅ Executor initialized")
    print("\n📍 Phase 3 Ready!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
