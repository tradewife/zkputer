"""
HyperOPS Trade Execution Module
Handles user-authorized trade execution via Hyperliquid API
"""

from typing import Dict, List, Optional
import logging

from trading_module import HyperliquidTrader, TradingConfig, OrderSpec
from strategy_module import TradingSetup

logger = logging.getLogger(__name__)


class TradeExecutor:
    """Handles user-authorized trade execution"""

    def __init__(self, trader: HyperliquidTrader):
        self.trader = trader
        self.pending_setups = []

    def prepare_trades(self, setups: List[TradingSetup]) -> List[Dict]:
        """Prepare trades for user review"""
        prepared_trades = []

        for setup in setups:
            # Calculate position size
            entry_price = sum(setup.entry_zone) / 2
            position_size = self.trader.calculate_position_size(
                setup.symbol, entry_price, setup.stop_loss
            )

            if position_size <= 0:
                logger.warning(f"Invalid position size for {setup.symbol}")
                continue

            trade_info = {
                "setup": setup,
                "entry_price": entry_price,
                "position_size": position_size,
                "notional": position_size * entry_price,
                "risk_amount": abs(entry_price - setup.stop_loss) * position_size,
                "order": OrderSpec(
                    symbol=setup.symbol,
                    side=setup.side,
                    order_type="limit",
                    size=position_size,
                    price=setup.entry_zone[0]
                    if setup.side == "buy"
                    else setup.entry_zone[1],
                ),
            }

            prepared_trades.append(trade_info)

        self.pending_setups = prepared_trades
        return prepared_trades

    def execute_trade(self, trade_index: int) -> Dict:
        """Execute a specific trade by index"""
        if trade_index >= len(self.pending_setups):
            return {"status": "error", "error": "Invalid trade index"}

        trade_info = self.pending_setups[trade_index]
        setup = trade_info["setup"]
        order = trade_info["order"]

        logger.info(f"Executing trade: {setup.symbol} {setup.side}")

        try:
            result = self.trader.place_order(order)

            if result.get("status") == "ok":
                logger.info(f"✅ Trade executed: {setup.symbol} {setup.side}")
                return {
                    "status": "success",
                    "setup": setup,
                    "order": result,
                    "trade_info": trade_info,
                }
            else:
                logger.error(f"❌ Trade failed: {result.get('error')}")
                return {"status": "error", "error": result.get("error")}

        except Exception as e:
            logger.error(f"❌ Execution error: {e}")
            return {"status": "error", "error": str(e)}

    def execute_all_trades(self) -> List[Dict]:
        """Execute all prepared trades"""
        results = []

        for i in range(len(self.pending_setups)):
            result = self.execute_trade(i)
            results.append(result)

            # Stop if any trade fails to avoid cascade
            if result.get("status") != "success":
                logger.warning(f"Stopping execution due to failure in trade {i + 1}")
                break

        return results

    def get_pending_trades_summary(self) -> str:
        """Get summary of pending trades for user review"""
        if not self.pending_setups:
            return "No pending trades."

        summary = "🎯 **PENDING TRADES**\n"
        summary += "=" * 40 + "\n\n"

        for i, trade_info in enumerate(self.pending_setups, 1):
            setup = trade_info["setup"]

            summary += f"**Trade {i}: {setup.symbol} {setup.side.upper()}**\n"
            summary += f"Thesis: {setup.thesis}\n"
            summary += f"Entry: ${trade_info['entry_price']:.4f}\n"
            summary += f"Size: {trade_info['position_size']:.6f}\n"
            summary += f"Notional: ${trade_info['notional']:.2f}\n"
            summary += f"Risk: ${trade_info['risk_amount']:.2f}\n"
            summary += f"Stop: ${setup.stop_loss:.4f}\n"
            summary += f"TP1: ${setup.take_profit_1:.4f}\n"
            summary += f"TP2: ${setup.take_profit_2:.4f}\n\n"

        summary += "**Available Commands:**\n"
        summary += "- `Execute trade [1-{}]` - Execute specific trade\n".format(
            len(self.pending_setups)
        )
        summary += "- `Execute all trades` - Execute all pending trades\n"
        summary += "- `Cancel pending trades` - Clear pending trades\n"

        return summary


# CLI functions for user interaction
def execute_user_command(command: str, executor: TradeExecutor) -> str:
    """Execute user command for trade management"""

    command = command.lower().strip()

    if "execute all" in command:
        results = executor.execute_all_trades()
        success_count = sum(1 for r in results if r.get("status") == "success")
        return f"✅ Executed {success_count}/{len(results)} trades successfully"

    elif "execute trade" in command:
        try:
            # Extract trade number
            parts = command.split()
            trade_num = int(parts[-1]) - 1  # Convert to 0-indexed

            result = executor.execute_trade(trade_num)
            if result.get("status") == "success":
                setup = result["setup"]
                return f"✅ Executed {setup.symbol} {setup.side} trade successfully"
            else:
                return f"❌ Trade execution failed: {result.get('error')}"

        except (ValueError, IndexError):
            return "❌ Invalid trade number. Use format: 'Execute trade 1'"

    elif "cancel" in command:
        executor.pending_setups = []
        return "🚫 All pending trades cancelled"

    elif "status" in command or "pending" in command:
        return executor.get_pending_trades_summary()

    else:
        return "❓ Unknown command. Available: 'Execute all', 'Execute trade [1-3]', 'Cancel', 'Status'"
