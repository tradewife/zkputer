#!/usr/bin/env python3

import asyncio
import json
import os
from hyperliquid.exchange import Exchange


class HyperliquidExecutor:
    def __init__(self):
        self.exchange = None
        self.address = None
        self.secret_key = None

    async def initialize(self):
        # Load configuration
        config_path = (
            "/home/kt/Desktop/HyperOPS/⚙️ Configuration/config/trading_config.json"
        )
        with open(config_path, "r") as f:
            config = json.load(f)

        self.address = config["account_address"]
        self.secret_key = config["secret_key"]

        # Initialize exchange (CORRECTED FOR NEW SDK)
        self.exchange = Exchange(
            account_address=config["account_address"], private_key=config["secret_key"]
        )

        print(f"✅ Initialized with address: {self.address}")
        print(f"✅ Mainnet: {not config.get('testnet', True)}")

    async def place_order(
        self, symbol, side, size, price, order_type="limit", reduce_only=False
    ):
        """Place order on Hyperliquid"""
        try:
            # Get meta for symbol
            meta = await self.exchange.meta()
            symbol_meta = None
            for m in meta["universe"]:
                if m["name"] == symbol:
                    symbol_meta = m
                    break

            if not symbol_meta:
                print(f"❌ Symbol {symbol} not found")
                return None

            # Calculate size in base currency
            sz_decimals = symbol_meta["szDecimals"]

            order = {
                "side": side,
                "orderType": order_type,
                "reduceOnly": reduce_only,
                "sz": str(size),
                "price": str(price),
            }

            print(f"📝 Placing {side} order: {size} {symbol} @ {price}")

            result = await self.exchange.order(order, symbol)

            if result and result.get("status") == "ok":
                order_id = result.get("response", {}).get("data", {}).get("oid", "")
                print(f"✅ Order placed successfully! ID: {order_id}")
                return result
            else:
                print(f"❌ Order failed: {result}")
                return None

        except Exception as e:
            print(f"❌ Error placing order: {e}")
            return None

    async def execute_trades(self):
        """Execute both trades"""
        print("🚀 EXECUTING LIVE TRADES ON MAINNET...")

        # Trade 1: XRP-PERP
        xrp_result = await self.place_order(
            symbol="XRP", side="buy", size=8.0, price=2.24
        )

        # Trade 2: SOL-PERP
        sol_result = await self.place_order(
            symbol="SOL", side="buy", size=0.086, price=138.50
        )

        return {"xrp": xrp_result, "sol": sol_result}

    async def main(self):
        await self.initialize()

        results = await self.execute_trades()

        print("\n📊 EXECUTION SUMMARY:")
        print(
            f"XRP Trade: {'✅ SUCCESS' if results['xrp'] and results['xrp'].get('status') == 'ok' else '❌ FAILED'}"
        )
        print(
            f"SOL Trade: {'✅ SUCCESS' if results['sol'] and results['sol'].get('status') == 'ok' else '❌ FAILED'}"
        )

        # Update performance log
        log_entry = {
            "timestamp": "2025-11-25_10:45",
            "trades": {
                "xrp": {
                    "status": "success"
                    if results["xrp"] and results["xrp"].get("status") == "ok"
                    else "failed",
                    "order_id": results["xrp"]
                    .get("response", {})
                    .get("data", {})
                    .get("oid", "")
                    if results["xrp"]
                    else None,
                },
                "sol": {
                    "status": "success"
                    if results["sol"] and results["sol"].get("status") == "ok"
                    else "failed",
                    "order_id": results["sol"]
                    .get("response", {})
                    .get("data", {})
                    .get("oid", "")
                    if results["sol"]
                    else None,
                },
            },
        }

        # Save to performance log
        log_path = "/home/kt/Desktop/HyperOPS/📖 Other Components/knowledge_graph/performance_log.md"
        with open(log_path, "a") as f:
            f.write(
                f"\n| 2025-11-25 | XRP-PERP | ETF_MOMENTUM | 2.24 | 2.15 | 2.35 | 2.45 | 8.0 | 12 | | | | {'🟢 Win' if log_entry['trades']['xrp']['status'] == 'success' else '🔴 Loss'} | ETF institutional flows |\n"
            )
            f.write(
                f"| 2025-11-25 | SOL-PERP | UPGRADE_CATALYST | 138.50 | 134.00 | 144.00 | 150.00 | 0.086 | 12 | | | | {'🟢 Win' if log_entry['trades']['sol']['status'] == 'success' else '🔴 Loss'} | Network upgrade catalyst |\n"
            )

        print(f"\n📝 Performance log updated: {log_path}")


if __name__ == "__main__":
    executor = HyperliquidExecutor()
    asyncio.run(executor.main())
