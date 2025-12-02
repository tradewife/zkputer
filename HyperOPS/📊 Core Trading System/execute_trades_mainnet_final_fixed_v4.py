#!/usr/bin/env python3

import json
from hyperliquid.exchange import Exchange
from eth_account import Account


class HyperliquidExecutor:
    def __init__(self):
        self.exchange = None
        self.address = None
        self.secret_key = None

    def initialize(self):
        # Load configuration
        config_path = (
            "/home/kt/Desktop/HyperOPS/⚙️ Configuration/config/trading_config.json"
        )
        with open(config_path, "r") as f:
            config = json.load(f)

        self.address = config["account_address"]
        self.secret_key = config["secret_key"]

        # Initialize exchange (CORRECTED FOR NEW SDK SYNTAX)
        account = Account.from_key(config["secret_key"])
        self.exchange = Exchange(
            wallet=account,
            account_address=config["account_address"],
        )

        print(f"✅ Initialized with address: {self.address}")
        print(f"✅ Mainnet: {not config.get('testnet', True)}")

    def place_order(
        self, symbol, side, size, price, order_type="limit", reduce_only=False
    ):
        """Place order on Hyperliquid"""
        try:
            from hyperliquid.utils.signing import OrderType

            # Convert side string to boolean
            is_buy = side.lower() == "buy"

            print(f"📝 Placing {side} order: {size} {symbol} @ ${price}")

            # Try using market_open for simpler execution
            result = self.exchange.market_open(
                name=symbol,
                is_buy=is_buy,
                sz=float(size),
                px=float(price),
                slippage=0.05,
            )

            print(f"🔍 Raw result: {result}")

            if result and result.get("status") == "ok":
                # Check if order was filled or has error
                statuses = (
                    result.get("response", {}).get("data", {}).get("statuses", [])
                )
                if statuses:
                    status = statuses[0]
                    if "filled" in status:
                        order_id = status.get("filled", {}).get("oid", "")
                        fill_price = status.get("filled", {}).get("avgPx", "")
                        fill_size = status.get("filled", {}).get("totalSz", "")
                        print(
                            f"✅ Order filled! ID: {order_id}, Size: {fill_size}, Price: ${fill_price}"
                        )
                        return {
                            "status": "ok",
                            "order_id": order_id,
                            "fill_price": fill_price,
                            "fill_size": fill_size,
                        }
                    elif "error" in status:
                        error_msg = status.get("error", "")
                        print(f"❌ Order error: {error_msg}")
                        return {"status": "error", "error": error_msg}

                print(f"❌ Unknown order response: {result}")
                return {"status": "failed", "result": str(result)}
            else:
                print(f"❌ Order failed: {result}")
                return {"status": "failed", "result": str(result)}

        except Exception as e:
            print(f"❌ Error placing order: {e}")
            return {"status": "error", "error": str(e)}

    def execute_trades(self):
        """Execute both trades"""
        print("🚀 EXECUTING LIVE TRADES ON MAINNET...")

        # Trade 1: XRP-PERP
        xrp_result = self.place_order(symbol="XRP", side="buy", size=8.0, price=2.24)

        # Trade 2: SOL-PERP (try different size)
        sol_result = self.place_order(symbol="SOL", side="buy", size=0.1, price=138.50)

        return {"xrp": xrp_result, "sol": sol_result}

    def main(self):
        self.initialize()

        results = self.execute_trades()

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
                    "order_id": results["xrp"].get("order_id", "")
                    if results["xrp"]
                    else None,
                },
                "sol": {
                    "status": "success"
                    if results["sol"] and results["sol"].get("status") == "ok"
                    else "failed",
                    "order_id": results["sol"].get("order_id", "")
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

        print(f"\n📝 Performance log updated: {log_path}")


if __name__ == "__main__":
    executor = HyperliquidExecutor()
    executor.main()
