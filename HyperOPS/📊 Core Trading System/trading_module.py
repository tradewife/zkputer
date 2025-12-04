"""
HyperOPS Trading Module
Integration with Hyperliquid Python SDK for automated trading
"""

import json
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timezone
import logging

try:
    from hyperliquid.info import Info
    from hyperliquid.api import API
    from hyperliquid.utils import constants
    from hyperliquid.utils.signing import sign_l1_action, sign_usd_transfer
    import eth_account
except ImportError:
    print(
        "Required packages not found. Install with: pip install hyperliquid-python-sdk eth-account"
    )
    exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class TradingConfig:
    """Configuration for HyperOPS trading"""

    account_address: str
    secret_key: str
    base_url: str = constants.MAINNET_API_URL
    testnet: bool = False
    max_risk_percent: float = 0.20  # 20% max risk per trade
    leverage_min: int = 9
    leverage_max: int = 12
    max_positions: int = 2

    @classmethod
    def from_file(cls, config_path: str = "config/trading_config.json"):
        """Load config from file"""
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path, "r") as f:
            config_data = json.load(f)

        return cls(**config_data)


@dataclass
class OrderSpec:
    """Order specification"""

    symbol: str
    side: str  # "buy" or "sell"
    order_type: str  # "limit", "market"
    size: float
    price: Optional[float] = None
    reduce_only: bool = False
    time_in_force: str = "gtc"  # good till cancelled


@dataclass
class Position:
    """Position information"""

    symbol: str
    size: float
    side: str
    entry_price: float
    mark_price: float
    unrealized_pnl: float
    leverage: int
    margin_used: float


class HyperliquidTrader:
    """Main trading class for HyperOPS"""

    def __init__(self, config: TradingConfig):
        self.config = config
        self.base_url = (
            constants.TESTNET_API_URL if config.testnet else constants.MAINNET_API_URL
        )

        # Initialize API clients
        self.info = Info(self.base_url, skip_ws=True)
        self.api = API(self.base_url)

        # Setup account
        self.account = eth_account.Account.from_key(config.secret_key)
        self.address = self.account.address

        # Verify address matches config
        if self.address.lower() != config.account_address.lower():
            raise ValueError(
                f"Address mismatch: derived {self.address} != config {config.account_address}"
            )

        logger.info(f"Initialized trader for address: {self.address}")

    def get_account_state(self) -> Dict:
        """Get current account state"""
        try:
            return self.info.user_state(self.address)
        except Exception as e:
            logger.error(f"Failed to get account state: {e}")
            return {}

    def get_positions(self) -> List[Position]:
        """Get current positions"""
        try:
            account_state = self.get_account_state()
            positions = []

            if "assetPositions" in account_state:
                for pos_data in account_state["assetPositions"]:
                    if float(pos_data["position"]["szi"]) != 0:  # Non-zero position
                        position = pos_data["position"]
                        coin = position["coin"]

                        positions.append(
                            Position(
                                symbol=coin,
                                size=float(position["szi"]),
                                side="long" if float(position["szi"]) > 0 else "short",
                                entry_price=float(position["entryPx"]),
                                mark_price=float(position["positionValue"])
                                / abs(float(position["szi"])),
                                unrealized_pnl=float(position["unrealizedPnl"]),
                                leverage=int(position["leverage"]["value"]),
                                margin_used=float(position["marginUsed"]),
                            )
                        )

            return positions
        except Exception as e:
            logger.error(f"Failed to get positions: {e}")
            return []

    def get_market_data(self, symbols: List[str] = None) -> Dict:
        """Get market data for specified symbols"""
        try:
            all_meta = self.info.meta()
            if not symbols:
                symbols = [asset["name"] for asset in all_meta["universe"]]

            market_data = {}
            for symbol in symbols:
                # Find asset metadata
                asset_meta = next(
                    (
                        asset
                        for asset in all_meta["universe"]
                        if asset["name"] == symbol
                    ),
                    None,
                )
                if asset_meta:
                    # Get current funding and OI
                    funding = self.info.funding_history(symbol)
                    oi = self.info.open_interest(symbol)

                    market_data[symbol] = {
                        "meta": asset_meta,
                        "funding": funding[-1] if funding else None,
                        "open_interest": oi,
                        "mark_price": asset_meta.get("markPrice", 0),
                        "index_price": asset_meta.get("indexPrice", 0),
                    }

            return market_data
        except Exception as e:
            logger.error(f"Failed to get market data: {e}")
            return {}

    def calculate_position_size(
        self, symbol: str, entry_price: float, stop_price: float
    ) -> float:
        """Calculate position size based on risk management rules"""
        try:
            account_state = self.get_account_state()
            if not account_state or "marginSummary" not in account_state:
                logger.error("Cannot get account equity for position sizing")
                return 0.0

            equity = float(account_state["marginSummary"]["accountValue"])
            risk_usd = equity * self.config.max_risk_percent

            # Calculate stop distance
            stop_distance = abs(entry_price - stop_price)
            if stop_distance == 0:
                logger.error("Stop distance cannot be zero")
                return 0.0

            # Calculate raw size
            raw_size = risk_usd / stop_distance

            # Get asset metadata for rounding
            meta = self.info.meta()
            asset_meta = next(
                (asset for asset in meta["universe"] if asset["name"] == symbol), None
            )
            if not asset_meta:
                logger.error(f"Cannot find metadata for {symbol}")
                return 0.0

            # Round down to lot size
            sz_decimals = asset_meta.get("szDecimals", 6)
            lot_size = 10 ** (-sz_decimals)
            rounded_size = int(raw_size / lot_size) * lot_size

            # Verify leverage constraints
            notional = rounded_size * entry_price
            max_notional = equity * self.config.leverage_max

            if notional > max_notional:
                # Adjust size to meet leverage constraint
                rounded_size = max_notional / entry_price
                rounded_size = int(rounded_size / lot_size) * lot_size

            logger.info(
                f"Position sizing: equity={equity:.2f}, risk={risk_usd:.2f}, size={rounded_size}"
            )
            return rounded_size

        except Exception as e:
            logger.error(f"Failed to calculate position size: {e}")
            return 0.0

    def place_order(self, order: OrderSpec) -> Dict:
        """Place an order"""
        try:
            # Create order dictionary
            order_dict = {
                "coin": order.symbol,
                "side": order.side,
                "orderType": order.order_type,
                "sz": str(order.size),
                "reduceOnly": order.reduce_only,
                "timeInForce": order.time_in_force,
            }

            if order.price:
                order_dict["limitPx"] = str(order.price)

            # Sign the order
            signature = sign_l1_action(self.account, "order", order_dict, self.base_url)

            # Place the order
            result = self.api.post_order(order_dict, signature)

            logger.info(
                f"Order placed: {order.symbol} {order.side} {order.size} @ {order.price}"
            )
            return result

        except Exception as e:
            logger.error(f"Failed to place order: {e}")
            return {"status": "error", "error": str(e)}

    def cancel_order(self, order_id: str, symbol: str) -> Dict:
        """Cancel an order"""
        try:
            cancel_dict = {"coin": symbol, "oid": order_id}

            signature = sign_l1_action(
                self.account, "cancel", cancel_dict, self.base_url
            )

            result = self.api.cancel_order(cancel_dict, signature)
            logger.info(f"Order cancelled: {order_id} for {symbol}")
            return result

        except Exception as e:
            logger.error(f"Failed to cancel order: {e}")
            return {"status": "error", "error": str(e)}

    def get_open_orders(self, symbol: str = None) -> List[Dict]:
        """Get open orders"""
        try:
            orders = self.info.open_orders(self.address)
            if symbol:
                orders = [order for order in orders if order["coin"] == symbol]
            return orders
        except Exception as e:
            logger.error(f"Failed to get open orders: {e}")
            return []

    def close_all_positions(self) -> List[Dict]:
        """Close all positions (emergency function)"""
        try:
            positions = self.get_positions()
            results = []

            for position in positions:
                # Create market order to close
                close_order = OrderSpec(
                    symbol=position.symbol,
                    side="sell" if position.side == "long" else "buy",
                    order_type="market",
                    size=abs(position.size),
                    reduce_only=True,
                )

                result = self.place_order(close_order)
                results.append(result)

            return results
        except Exception as e:
            logger.error(f"Failed to close positions: {e}")
            return [{"status": "error", "error": str(e)}]


# Utility functions
def create_sample_config():
    """Create a sample configuration file"""
    sample_config = {
        "account_address": "0xYOUR_WALLET_ADDRESS",
        "secret_key": "your_private_key_here",
        "testnet": True,
        "max_risk_percent": 0.20,
        "leverage_min": 9,
        "leverage_max": 12,
        "max_positions": 2,
        "hard_exit_time": "22:00",
    }

    os.makedirs("config", exist_ok=True)
    with open("config/trading_config.json.example", "w") as f:
        json.dump(sample_config, f, indent=2)

    print("Sample config created at config/trading_config.json.example")
    print("Edit this file with your credentials and rename to trading_config.json")


if __name__ == "__main__":
    # Example usage
    create_sample_config()
