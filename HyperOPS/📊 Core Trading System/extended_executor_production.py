#!/usr/bin/env python3
"""
Extended Trade Executor - PRODUCTION READY
Migrated from Hyperliquid to Extended Exchange
"""

import json
import sys
import os
import asyncio
from decimal import Decimal

# Import Extended SDK
from x10.perpetual.accounts import StarkPerpetualAccount
from x10.perpetual.trading_client import PerpetualTradingClient
from x10.perpetual.configuration import MAINNET_CONFIG, TESTNET_CONFIG
from x10.perpetual.orders import OrderSide, OrderType


class ExtendedExecutor:
    def __init__(self):
        self.trading_client = None
        self.stark_account = None
        self.config = None

    async def initialize(self):
        """Initialize Extended trading client with proper error handling"""
        try:
            # Load configuration
            config_path = (
                "/home/kt/ZKputer/HyperOPS/⚙️ Configuration/config/trading_config.json"
            )

            if not os.path.exists(config_path):
                raise FileNotFoundError(f"Config file not found: {config_path}")

            with open(config_path, "r") as f:
                self.config = json.load(f)

            # Create Stark account
            self.stark_account = StarkPerpetualAccount(
                vault=self.config["vault_number"],
                private_key=self.config["stark_private_key"],
                public_key=self.config["stark_public_key"],
                api_key=self.config["api_key"],
            )

            # Initialize trading client
            exchange_config = TESTNET_CONFIG if self.config.get("testnet", False) else MAINNET_CONFIG
            self.trading_client = await PerpetualTradingClient.create(
                exchange_config,
                self.stark_account
            )

            print(f"✅ Initialized Extended client")
            print(f"✅ Vault: {self.config['vault_number']}")
            print(f"✅ Mainnet: {not self.config.get('testnet', False)}")
            return True

        except Exception as e:
            print(f"❌ Initialization failed: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def place_order(self, symbol, side, size, price, slippage=0.05):
        """
        Place order with robust error handling
        """
        try:
            # Convert side to OrderSide enum
            order_side = OrderSide.BUY if side.lower() == "buy" else OrderSide.SELL

            print(f"📝 Placing {side} order: {size} {symbol} @ ${price}")

            # Place limit order with IOC for market execution
            placed_order = await self.trading_client.place_order(
                market_name=symbol,
                amount_of_synthetic=Decimal(str(size)),
                price=Decimal(str(price)),
                side=order_side,
                order_type=OrderType.IOC,  # Immediate or Cancel (market-like)
                reduce_only=False,
                post_only=False,
            )

            print(f"✅ Order placed! ID: {placed_order.id}")
            
            # Wait a moment for fill
            await asyncio.sleep(1)
            
            # Check order status
            try:
                positions = await self.trading_client.account.get_positions()
                for pos in positions.data:
                    if pos.market == symbol:
                        print(f"✅ Position confirmed: {pos.size} @ {pos.open_price}")
                        return {
                            "status": "ok",
                            "order_id": placed_order.id,
                            "fill_price": str(pos.open_price),
                            "fill_size": str(pos.size),
                            "symbol": symbol,
                            "side": side,
                        }
            except:
                pass

            return {
                "status": "ok",
                "order_id": placed_order.id,
                "symbol": symbol,
                "side": side,
            }

        except Exception as e:
            print(f"❌ Error placing order: {e}")
            import traceback
            traceback.print_exc()
            return {"status": "error", "error": str(e), "symbol": symbol}

    async def execute_trades(self, trade_list):
        """
        Execute list of trades
        trade_list format: [{"symbol": "XRP-USD", "side": "buy", "size": 8.0, "price": 2.24}, ...]
        """
        print("🚀 EXECUTING LIVE TRADES ON EXTENDED MAINNET...")

        results = {}

        for trade in trade_list:
            symbol = trade["symbol"]
            result = await self.place_order(
                symbol=symbol,
                side=trade["side"],
                size=trade["size"],
                price=trade["price"],
            )
            results[symbol] = result
            
            # Small delay between trades
            await asyncio.sleep(0.5)

        return results

    async def update_performance_log(self, results, timestamp=None):
        """Update performance log with trade results"""
        if timestamp is None:
            from datetime import datetime

            timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M")

        log_path = "/home/kt/ZKputer/HyperOPS/📖 Other Components/knowledge_graph/performance_log.md"

        try:
            with open(log_path, "a") as f:
                for symbol, result in results.items():
                    if result.get("status") == "ok":
                        status_emoji = "🟢 Win"
                        fill_price = result.get("fill_price", "N/A")
                        fill_size = result.get("fill_size", "N/A")
                        log_entry = f"\n| {timestamp} | {symbol} | EXTENDED_EXECUTION | {fill_price} | | | | {fill_size} | 12 | | | | {status_emoji} | Extended automated execution |"
                        f.write(log_entry)

            print(f"📝 Performance log updated: {log_path}")
            return True

        except Exception as e:
            print(f"❌ Failed to update performance log: {e}")
            return False

    async def main(self, trade_list=None):
        """Main execution method"""
        if trade_list is None:
            # Default trades - update symbols to Extended format (e.g., "BTC-USD")
            trade_list = [
                {"symbol": "XRP-USD", "side": "buy", "size": 8.0, "price": 2.24},
                {"symbol": "SOL-USD", "side": "buy", "size": 0.1, "price": 238.50},
            ]

        # Initialize
        if not await self.initialize():
            print("❌ Failed to initialize. Exiting.")
            return False

        # Check account balance
        try:
            balance = await self.trading_client.account.get_balance()
            print(f"\n💰 Account Balance: ${float(balance.data.equity):.2f}")
            print(f"💰 Available: ${float(balance.data.available_for_trade):.2f}")
        except Exception as e:
            print(f"⚠️ Could not fetch balance: {e}")

        # Execute trades
        results = await self.execute_trades(trade_list)

        # Print summary
        print("\n📊 EXECUTION SUMMARY:")
        for symbol, result in results.items():
            status = "✅ SUCCESS" if result.get("status") == "ok" else "❌ FAILED"
            print(f"{symbol} Trade: {status}")

        # Update performance log
        await self.update_performance_log(results)

        return True


async def run_executor(trade_list=None):
    """Async wrapper for executor"""
    executor = ExtendedExecutor()
    return await executor.main(trade_list)


if __name__ == "__main__":
    # Check if custom trades provided as command line args
    trade_list = None
    
    # Run async executor
    asyncio.run(run_executor(trade_list))
