"""
ExtendedOPS Trading Module
Integration with Extended Python SDK for automated trading
"""

import json
import os
import asyncio
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
import logging

try:
    from x10.perpetual.accounts import StarkPerpetualAccount
    from x10.perpetual.trading_client import PerpetualTradingClient
    from x10.perpetual.configuration import MAINNET_CONFIG, TESTNET_CONFIG
    from x10.perpetual.orders import OrderSide, OrderType, TimeInForce, OrderTpslType, OrderTriggerPriceType, OrderPriceType
    from x10.perpetual.order_object import OrderTpslTriggerParam
except ImportError:
    print(
        "Required packages not found. Install with: pip install x10-python-trading-starknet"
    )
    exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class TradingConfig:
    """Configuration for ExtendedOPS trading"""

    account_address: str
    api_key: str
    stark_public_key: str
    stark_private_key: str
    vault_number: int
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

        # Filter to only valid TradingConfig fields
        valid_fields = {
            "account_address", "api_key", "stark_public_key", "stark_private_key",
            "vault_number", "testnet", "max_risk_percent", "leverage_min",
            "leverage_max", "max_positions"
        }
        filtered_config = {k: v for k, v in config_data.items() if k in valid_fields}
        
        return cls(**filtered_config)



@dataclass
class OrderSpec:
    """Order specification"""

    symbol: str  # Format: "BTC-USD"
    side: str  # "buy" or "sell"
    order_type: str  # "limit", "market", "stop_loss", "take_profit"
    size: float
    price: Optional[float] = None
    reduce_only: bool = False
    post_only: bool = False
    take_profit_price: Optional[float] = None
    stop_loss_price: Optional[float] = None


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


class ExtendedTrader:
    """Main trading class for ExtendedOPS"""

    def __init__(self, config: TradingConfig):
        self.config = config
        self.trading_client = None
        self.stark_account = None
        
        # Initialize in async context
        logger.info(f"Initialized trader for vault: {config.vault_number}")

    async def initialize(self):
        """Initialize Extended trading client (async)"""
        try:
            # Create Stark account
            self.stark_account = StarkPerpetualAccount(
                vault=self.config.vault_number,
                private_key=self.config.stark_private_key,
                public_key=self.config.stark_public_key,
                api_key=self.config.api_key,
            )

            # Create trading client (direct constructor, not .create())
            config = TESTNET_CONFIG if self.config.testnet else MAINNET_CONFIG
            self.trading_client = PerpetualTradingClient(
                config, self.stark_account
            )

            logger.info(f"Extended client initialized for vault {self.config.vault_number}")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize Extended client: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def cleanup(self):
        """Cleanup Extended client connections"""
        try:
            if self.trading_client:
                await self.trading_client.close()
                logger.info("Extended client closed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

    async def get_account_state(self) -> Dict:
        """Get current account state"""
        try:
            balance = await self.trading_client.account.get_balance()
            return {
                "equity": float(balance.data.equity),
                "available_balance": float(balance.data.available_for_trade),
                "margin_usage": float(balance.data.margin_ratio) if balance.data.margin_ratio else 0.0,
            }
        except Exception as e:
            logger.error(f"Failed to get account state: {e}")
            import traceback
            traceback.print_exc()
            return {}

    async def get_positions(self) -> List[Position]:
        """Get current positions"""
        try:
            positions_response = await self.trading_client.account.get_positions()
            positions = []

            # Extended returns WrappedApiResponse with .data attribute
            for pos in positions_response.data:
                positions.append(
                    Position(
                        symbol=pos.market,
                        size=float(pos.size),
                        side="long" if (pos.side.value if hasattr(pos.side, 'value') else pos.side) == "LONG" else "short",
                        entry_price=float(pos.open_price),
                        mark_price=float(pos.mark_price),
                        unrealized_pnl=float(pos.unrealised_pnl),
                        leverage=int(float(pos.leverage)),
                        margin_used=float(pos.value) / float(pos.leverage) if float(pos.leverage) > 0 else 0,
                    )
                )

            return positions
        except Exception as e:
            logger.error(f"Failed to get positions: {e}")
            import traceback
            traceback.print_exc()
            return []

    async def get_market_data(self, symbols: List[str] = None) -> Dict:
        """Get market data for specified symbols"""
        try:
            markets = await self.trading_client.markets_info.get_markets()
            
            market_data = {}
            for market in markets.data:
                market_name = market.name
                if symbols is None or market_name in symbols:
                    # Extended has market data in market_stats
                    stats = market.market_stats if hasattr(market, 'market_stats') else None
                    
                    market_data[market_name] = {
                        "symbol": market_name,
                        "mark_price": float(stats.mark_price) if stats else None,
                        "index_price": float(stats.index_price) if stats else None,
                        "funding_rate": float(stats.funding_rate) if stats else None,
                        "daily_volume": float(stats.daily_volume) if stats else None,
                        "open_interest": float(stats.open_interest) if stats else None,
                        "last_price": float(stats.last_price) if stats else None,
                        "active": market.active if hasattr(market, 'active') else True,
                    }

            return market_data
        except Exception as e:
            logger.error(f"Failed to get market data: {e}")
            import traceback
            traceback.print_exc()
            return {}

    async def calculate_position_size(
        self, symbol: str, entry_price: float, stop_price: float
    ) -> float:
        """Calculate position size based on risk management rules"""
        try:
            account_state = await self.get_account_state()
            if not account_state:
                logger.error("Cannot get account equity for position sizing")
                return 0.0

            equity = account_state["equity"]
            risk_usd = equity * self.config.max_risk_percent

            # Calculate stop distance
            stop_distance = abs(entry_price - stop_price)
            if stop_distance == 0:
                logger.error("Stop distance cannot be zero")
                return 0.0

            # Calculate raw size
            raw_size = risk_usd / stop_distance

            # Round down to reasonable precision (Extended handles lot size internally)
            rounded_size = round(raw_size, 4)

            # Verify leverage constraints
            notional = rounded_size * entry_price
            max_notional = equity * self.config.leverage_max

            if notional > max_notional:
                # Adjust size to meet leverage constraint
                rounded_size = max_notional / entry_price
                rounded_size = round(rounded_size, 4)

            logger.info(
                f"Position sizing: equity={equity:.2f}, risk={risk_usd:.2f}, size={rounded_size}"
            )
            return rounded_size

        except Exception as e:
            logger.error(f"Failed to calculate position size: {e}")
            return 0.0

    async def place_order(self, order: OrderSpec) -> Dict:
        """Place an order"""
        try:
            # Convert side to OrderSide enum
            side = OrderSide.BUY if order.side.lower() == "buy" else OrderSide.SELL

            # Convert order type
            # Convert order type
            if order.order_type.lower() == "market":
                time_in_force = TimeInForce.IOC
                order_type_enum = OrderType.MARKET
            elif order.order_type.lower() in ["stop_loss", "take_profit"]:
                time_in_force = TimeInForce.GTT
                order_type_enum = OrderType.TPSL
            else:
                time_in_force = TimeInForce.GTT
                order_type_enum = OrderType.LIMIT

            # Configure TP/SL if provided
            tp_param = None
            sl_param = None
            tp_sl_type = None

            if order.take_profit_price or order.stop_loss_price or order.order_type.lower() in ["stop_loss", "take_profit"]:
                tp_sl_type = OrderTpslType.ORDER
                
                # Determine slippage direction based on main order side
                # If BUY, TP/SL are SELL. If SELL, TP/SL are BUY.
                is_buy = side == OrderSide.BUY
                
                # Handle standalone TP/SL orders where price might be in order.price
                trigger_price_tp = order.take_profit_price
                trigger_price_sl = order.stop_loss_price
                
                if order.order_type.lower() == "take_profit" and not trigger_price_tp:
                    trigger_price_tp = order.price
                    
                if order.order_type.lower() == "stop_loss" and not trigger_price_sl:
                    trigger_price_sl = order.price

                if trigger_price_tp:
                    # TP Limit Price:
                    # If Main BUY -> TP SELL. Trigger > Entry. Limit should be <= Trigger (usually just Trigger).
                    # If Main SELL -> TP BUY. Trigger < Entry. Limit should be >= Trigger.
                    # To ensure fill, we can use a slight buffer or just the trigger price.
                    # Let's use 1% slippage for TP to ensure fill upon trigger.
                    tp_limit_price = Decimal(str(trigger_price_tp)) * (Decimal("0.99") if is_buy else Decimal("1.01"))
                    
                    tp_param = OrderTpslTriggerParam(
                        trigger_price=Decimal(str(trigger_price_tp)),
                        trigger_price_type=OrderTriggerPriceType.MARK,
                        price=tp_limit_price,
                        price_type=OrderPriceType.LIMIT
                    )
                
                if trigger_price_sl:
                    # SL Limit Price:
                    # If Main BUY -> SL SELL. Trigger < Entry. Limit should be < Trigger (Market-like).
                    # If Main SELL -> SL BUY. Trigger > Entry. Limit should be > Trigger (Market-like).
                    # Use 5% slippage to ensure stop fill.
                    sl_limit_price = Decimal(str(trigger_price_sl)) * (Decimal("0.95") if is_buy else Decimal("1.05"))
                    
                    sl_param = OrderTpslTriggerParam(
                        trigger_price=Decimal(str(trigger_price_sl)),
                        trigger_price_type=OrderTriggerPriceType.MARK,
                        price=sl_limit_price,
                        price_type=OrderPriceType.LIMIT
                    )

            # Place the order
            placed_order = await self.trading_client.place_order(
                market_name=order.symbol,
                amount_of_synthetic=Decimal(str(order.size)),
                price=Decimal(str(order.price)) if order.price and order_type_enum != OrderType.TPSL else Decimal("0"),
                side=side,
                time_in_force=time_in_force,
                reduce_only=order.reduce_only,
                post_only=order.post_only,
                tp_sl_type=tp_sl_type,
                take_profit=tp_param,
                stop_loss=sl_param
            )

            logger.info(
                f"Order placed: {order.symbol} {order.side} {order.size} @ {order.price} | ID: {placed_order.data.id}"
            )
            return {
                "status": "ok",
                "order_id": placed_order.data.id,
                "symbol": order.symbol,
                "side": order.side,
                "size": order.size,
                "price": order.price,
            }

        except Exception as e:
            logger.error(f"Failed to place order: {e}")
            return {"status": "error", "error": str(e), "symbol": order.symbol}

    async def cancel_order(self, order_id: int) -> Dict:
        """Cancel an order"""
        try:
            await self.trading_client.orders.cancel_order(order_id=order_id)
            logger.info(f"Order cancelled: {order_id}")
            return {"status": "ok", "order_id": order_id}

        except Exception as e:
            logger.error(f"Failed to cancel order: {e}")
            return {"status": "error", "error": str(e)}

    async def get_open_orders(self, symbol: str = None) -> List[Dict]:
        """Get open orders"""
        try:
            orders_response = await self.trading_client.account.get_open_orders(
                market_names=[symbol] if symbol else None
            )
            
            orders = []
            for order in orders_response.data:
                orders.append({
                    "id": order.id,
                    "symbol": order.market,
                    "side": order.side.value.lower() if hasattr(order.side, 'value') else str(order.side).lower(),
                    "type": order.type.value.lower() if hasattr(order.type, 'value') else str(order.type).lower(),
                    "price": float(order.price),
                    "size": float(order.qty),
                    "filled": float(order.filled_qty) if order.filled_qty else 0,
                })
            
            return orders
        except Exception as e:
            logger.error(f"Failed to get open orders: {e}")
            return []

    async def close_all_positions(self) -> List[Dict]:
        """Close all positions (emergency function)"""
        try:
            positions = await self.get_positions()
            results = []

            for position in positions:
                # Create market order to close
                close_order = OrderSpec(
                    symbol=position.symbol,
                    side="sell" if position.side == "long" else "buy",
                    order_type="market",
                    size=abs(position.size),
                    price=position.mark_price,  # Reference price for IOC
                    reduce_only=True,
                )

                result = await self.place_order(close_order)
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
        "api_key": "your_api_key_from_extended_ui",
        "stark_public_key": "your_stark_public_key",
        "stark_private_key": "your_stark_private_key",
        "vault_number": 0,
        "testnet": False,
        "max_risk_percent": 0.20,
        "leverage_min": 9,
        "leverage_max": 12,
        "max_positions": 2,
    }

    os.makedirs("config", exist_ok=True)
    with open("config/trading_config.json.example", "w") as f:
        json.dump(sample_config, f, indent=2)

    print("Sample config created at config/trading_config.json.example")
    print("Get your credentials from: https://app.extended.exchange/api-management")


if __name__ == "__main__":
    # Example usage
    create_sample_config()
