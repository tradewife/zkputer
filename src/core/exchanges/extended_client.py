"""
Extended Exchange Client - Production Trading
Uses x10-python-trading-starknet SDK
"""

import asyncio
import json
from decimal import Decimal
from typing import Dict, List, Optional
from dataclasses import dataclass
import logging

from . import load_extended_config

logger = logging.getLogger(__name__)

try:
    from x10.perpetual.accounts import StarkPerpetualAccount
    from x10.perpetual.trading_client import PerpetualTradingClient
    from x10.perpetual.configuration import MAINNET_CONFIG
    from x10.perpetual.orders import OrderSide, OrderType, TimeInForce, OrderTpslType, OrderTriggerPriceType, OrderPriceType
    from x10.perpetual.order_object import OrderTpslTriggerParam
except ImportError:
    raise ImportError("Install: pip install x10-python-trading-starknet")


@dataclass
class ExtendedOrder:
    symbol: str          # e.g., "BTC-USD"
    side: str            # "buy" or "sell"
    size: float          # Position size
    price: Optional[float] = None
    order_type: str = "limit"  # "limit", "market"
    reduce_only: bool = False
    take_profit: Optional[float] = None
    stop_loss: Optional[float] = None


class ExtendedClient:
    """Production Extended Exchange client - MAINNET ONLY"""
    
    def __init__(self):
        self.config = load_extended_config()
        self.trading_client = None
        self.stark_account = None
        self._initialized = False
    
    async def connect(self) -> bool:
        """Initialize connection to Extended Exchange"""
        try:
            self.stark_account = StarkPerpetualAccount(
                vault=self.config["vault_number"],
                private_key=self.config["stark_private_key"],
                public_key=self.config["stark_public_key"],
                api_key=self.config["api_key"],
            )
            
            self.trading_client = PerpetualTradingClient(
                MAINNET_CONFIG, self.stark_account
            )
            
            self._initialized = True
            logger.info(f"Extended connected: vault {self.config['vault_number']}")
            return True
        except Exception as e:
            logger.error(f"Extended connection failed: {e}")
            return False
    
    async def disconnect(self):
        """Close connection"""
        if self.trading_client:
            await self.trading_client.close()
            self._initialized = False
    
    async def get_balance(self) -> Dict:
        """Get account balance and equity"""
        if not self._initialized:
            raise RuntimeError("Client not connected. Call connect() first.")
        
        balance = await self.trading_client.account.get_balance()
        return {
            "equity": float(balance.data.equity),
            "available": float(balance.data.available_for_trade),
            "margin_ratio": float(balance.data.margin_ratio) if balance.data.margin_ratio else 0.0,
        }
    
    async def get_positions(self) -> List[Dict]:
        """Get all open positions"""
        if not self._initialized:
            raise RuntimeError("Client not connected. Call connect() first.")
        
        response = await self.trading_client.account.get_positions()
        positions = []
        for pos in response.data:
            positions.append({
                "symbol": pos.market,
                "size": float(pos.size),
                "side": "long" if str(pos.side).upper() == "LONG" else "short",
                "entry_price": float(pos.open_price),
                "mark_price": float(pos.mark_price),
                "pnl": float(pos.unrealised_pnl),
                "leverage": int(float(pos.leverage)),
            })
        return positions
    
    async def get_open_orders(self, symbol: Optional[str] = None) -> List[Dict]:
        """Get open orders"""
        if not self._initialized:
            raise RuntimeError("Client not connected. Call connect() first.")
        
        response = await self.trading_client.account.get_open_orders(
            market_names=[symbol] if symbol else None
        )
        orders = []
        for order in response.data:
            orders.append({
                "id": order.id,
                "symbol": order.market,
                "side": str(order.side).lower(),
                "type": str(order.type).lower(),
                "price": float(order.price),
                "size": float(order.qty),
                "filled": float(order.filled_qty) if order.filled_qty else 0,
            })
        return orders
    
    async def place_order(self, order: ExtendedOrder) -> Dict:
        """
        Place order on Extended Exchange
        
        Args:
            order: ExtendedOrder specification
            
        Returns:
            Dict with status, order_id, or error
        """
        if not self._initialized:
            raise RuntimeError("Client not connected. Call connect() first.")
        
        try:
            side = OrderSide.BUY if order.side.lower() == "buy" else OrderSide.SELL
            
            if order.order_type.lower() == "market":
                time_in_force = TimeInForce.IOC
                order_type_enum = OrderType.MARKET
            else:
                time_in_force = TimeInForce.GTT
                order_type_enum = OrderType.LIMIT
            
            # Configure TP/SL if provided
            tp_param = None
            sl_param = None
            tp_sl_type = None
            
            if order.take_profit or order.stop_loss:
                tp_sl_type = OrderTpslType.ORDER
                is_buy = side == OrderSide.BUY
                
                if order.take_profit:
                    tp_limit = Decimal(str(order.take_profit)) * (Decimal("0.99") if is_buy else Decimal("1.01"))
                    tp_param = OrderTpslTriggerParam(
                        trigger_price=Decimal(str(order.take_profit)),
                        trigger_price_type=OrderTriggerPriceType.MARK,
                        price=tp_limit,
                        price_type=OrderPriceType.LIMIT
                    )
                
                if order.stop_loss:
                    sl_limit = Decimal(str(order.stop_loss)) * (Decimal("0.95") if is_buy else Decimal("1.05"))
                    sl_param = OrderTpslTriggerParam(
                        trigger_price=Decimal(str(order.stop_loss)),
                        trigger_price_type=OrderTriggerPriceType.MARK,
                        price=sl_limit,
                        price_type=OrderPriceType.LIMIT
                    )
            
            result = await self.trading_client.place_order(
                market_name=order.symbol,
                amount_of_synthetic=Decimal(str(order.size)),
                price=Decimal(str(order.price)) if order.price else Decimal("0"),
                side=side,
                time_in_force=time_in_force,
                reduce_only=order.reduce_only,
                tp_sl_type=tp_sl_type,
                take_profit=tp_param,
                stop_loss=sl_param
            )
            
            logger.info(f"Extended order placed: {order.symbol} {order.side} {order.size}")
            return {
                "status": "ok",
                "order_id": result.data.id,
                "symbol": order.symbol,
                "side": order.side,
                "size": order.size,
            }
            
        except Exception as e:
            logger.error(f"Extended order failed: {e}")
            return {"status": "error", "error": str(e), "symbol": order.symbol}
    
    async def cancel_order(self, order_id: int) -> Dict:
        """Cancel an order by ID"""
        if not self._initialized:
            raise RuntimeError("Client not connected. Call connect() first.")
        
        try:
            await self.trading_client.orders.cancel_order(order_id=order_id)
            return {"status": "ok", "order_id": order_id}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    async def close_position(self, symbol: str) -> Dict:
        """Close position for a symbol using market order"""
        positions = await self.get_positions()
        for pos in positions:
            if pos["symbol"] == symbol:
                order = ExtendedOrder(
                    symbol=symbol,
                    side="sell" if pos["side"] == "long" else "buy",
                    size=abs(pos["size"]),
                    price=pos["mark_price"],
                    order_type="market",
                    reduce_only=True
                )
                return await self.place_order(order)
        return {"status": "error", "error": f"No position found for {symbol}"}


async def test_connection():
    """Test Extended Exchange connection"""
    client = ExtendedClient()
    if await client.connect():
        print("Connected to Extended Exchange")
        balance = await client.get_balance()
        print(f"Equity: ${balance['equity']:.2f}")
        print(f"Available: ${balance['available']:.2f}")
        positions = await client.get_positions()
        print(f"Open positions: {len(positions)}")
        await client.disconnect()
    else:
        print("Connection failed")


if __name__ == "__main__":
    asyncio.run(test_connection())
