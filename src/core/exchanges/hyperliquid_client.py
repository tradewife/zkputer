"""
Hyperliquid Client - Production Trading
Uses hyperliquid-python-sdk
"""

import json
from typing import Dict, List, Optional
from dataclasses import dataclass
import logging

from . import load_hyperliquid_config

logger = logging.getLogger(__name__)

try:
    from hyperliquid.exchange import Exchange
    from hyperliquid.info import Info
    from eth_account import Account
except ImportError:
    raise ImportError("Install: pip install hyperliquid-python-sdk eth-account")


@dataclass
class HyperliquidOrder:
    symbol: str          # e.g., "BTC", "ETH", "SOL"
    side: str            # "buy" or "sell"
    size: float          # Position size
    price: float         # Limit price
    slippage: float = 0.05
    reduce_only: bool = False


class HyperliquidClient:
    """Production Hyperliquid client - MAINNET ONLY"""
    
    def __init__(self):
        self.config = load_hyperliquid_config()
        self.exchange = None
        self.info = None
        self.address = self.config["account_address"]
        self._initialized = False
    
    def connect(self) -> bool:
        """Initialize connection to Hyperliquid"""
        try:
            account = Account.from_key(self.config["secret_key"])
            self.exchange = Exchange(
                wallet=account,
                account_address=self.address,
            )
            self.info = Info(skip_ws=True)
            self._initialized = True
            logger.info(f"Hyperliquid connected: {self.address[:10]}...")
            return True
        except Exception as e:
            logger.error(f"Hyperliquid connection failed: {e}")
            return False
    
    def get_balance(self) -> Dict:
        """Get account balance and margin info"""
        if not self._initialized:
            raise RuntimeError("Client not connected. Call connect() first.")
        
        user_state = self.info.user_state(self.address)
        return {
            "equity": float(user_state.get("marginSummary", {}).get("accountValue", 0)),
            "available": float(user_state.get("withdrawable", 0)),
            "margin_used": float(user_state.get("marginSummary", {}).get("totalMarginUsed", 0)),
        }
    
    def get_positions(self) -> List[Dict]:
        """Get all open positions"""
        if not self._initialized:
            raise RuntimeError("Client not connected. Call connect() first.")
        
        user_state = self.info.user_state(self.address)
        positions = []
        for pos in user_state.get("assetPositions", []):
            position = pos.get("position", {})
            if float(position.get("szi", 0)) != 0:
                size = float(position.get("szi", 0))
                positions.append({
                    "symbol": position.get("coin", ""),
                    "size": abs(size),
                    "side": "long" if size > 0 else "short",
                    "entry_price": float(position.get("entryPx", 0)),
                    "mark_price": float(position.get("positionValue", 0)) / abs(size) if size != 0 else 0,
                    "pnl": float(position.get("unrealizedPnl", 0)),
                    "leverage": int(float(position.get("leverage", {}).get("value", 1))),
                })
        return positions
    
    def get_open_orders(self, symbol: Optional[str] = None) -> List[Dict]:
        """Get open orders"""
        if not self._initialized:
            raise RuntimeError("Client not connected. Call connect() first.")
        
        open_orders = self.info.open_orders(self.address)
        orders = []
        for order in open_orders:
            if symbol is None or order.get("coin") == symbol:
                orders.append({
                    "id": order.get("oid"),
                    "symbol": order.get("coin"),
                    "side": order.get("side", "").lower(),
                    "price": float(order.get("limitPx", 0)),
                    "size": float(order.get("sz", 0)),
                    "filled": float(order.get("sz", 0)) - float(order.get("remainingSz", 0)),
                })
        return orders
    
    def place_order(self, order: HyperliquidOrder) -> Dict:
        """
        Place order on Hyperliquid using market_open for reliable execution
        
        Args:
            order: HyperliquidOrder specification
            
        Returns:
            Dict with status, order_id, fill info, or error
        """
        if not self._initialized:
            raise RuntimeError("Client not connected. Call connect() first.")
        
        try:
            is_buy = order.side.lower() == "buy"
            
            result = self.exchange.market_open(
                name=order.symbol,
                is_buy=is_buy,
                sz=float(order.size),
                px=float(order.price),
                slippage=order.slippage,
            )
            
            if result and result.get("status") == "ok":
                statuses = result.get("response", {}).get("data", {}).get("statuses", [])
                if statuses:
                    status = statuses[0]
                    if "filled" in status:
                        fill_info = status["filled"]
                        logger.info(f"Hyperliquid filled: {order.symbol} {order.side} {fill_info.get('totalSz')} @ {fill_info.get('avgPx')}")
                        return {
                            "status": "ok",
                            "order_id": fill_info.get("oid", ""),
                            "fill_price": float(fill_info.get("avgPx", 0)),
                            "fill_size": float(fill_info.get("totalSz", 0)),
                            "symbol": order.symbol,
                            "side": order.side,
                        }
                    elif "error" in status:
                        return {"status": "error", "error": status["error"], "symbol": order.symbol}
            
            logger.error(f"Hyperliquid order failed: {result}")
            return {"status": "error", "error": str(result), "symbol": order.symbol}
            
        except Exception as e:
            logger.error(f"Hyperliquid order exception: {e}")
            return {"status": "error", "error": str(e), "symbol": order.symbol}
    
    def place_limit_order(self, order: HyperliquidOrder) -> Dict:
        """Place a limit order (may not fill immediately)"""
        if not self._initialized:
            raise RuntimeError("Client not connected. Call connect() first.")
        
        try:
            is_buy = order.side.lower() == "buy"
            
            result = self.exchange.order(
                name=order.symbol,
                is_buy=is_buy,
                sz=float(order.size),
                limit_px=float(order.price),
                order_type={"limit": {"tif": "Gtc"}},
                reduce_only=order.reduce_only,
            )
            
            if result and result.get("status") == "ok":
                statuses = result.get("response", {}).get("data", {}).get("statuses", [])
                if statuses and "resting" in statuses[0]:
                    return {
                        "status": "ok",
                        "order_id": statuses[0]["resting"]["oid"],
                        "symbol": order.symbol,
                        "side": order.side,
                        "size": order.size,
                        "price": order.price,
                    }
            
            return {"status": "error", "error": str(result), "symbol": order.symbol}
            
        except Exception as e:
            return {"status": "error", "error": str(e), "symbol": order.symbol}
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict:
        """Cancel an order"""
        if not self._initialized:
            raise RuntimeError("Client not connected. Call connect() first.")
        
        try:
            result = self.exchange.cancel(symbol, order_id)
            if result.get("status") == "ok":
                return {"status": "ok", "order_id": order_id}
            return {"status": "error", "error": str(result)}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def close_position(self, symbol: str) -> Dict:
        """Close position for a symbol using market order"""
        positions = self.get_positions()
        for pos in positions:
            if pos["symbol"] == symbol:
                order = HyperliquidOrder(
                    symbol=symbol,
                    side="sell" if pos["side"] == "long" else "buy",
                    size=abs(pos["size"]),
                    price=pos["mark_price"],
                    reduce_only=True
                )
                return self.place_order(order)
        return {"status": "error", "error": f"No position found for {symbol}"}


def test_connection():
    """Test Hyperliquid connection"""
    client = HyperliquidClient()
    if client.connect():
        print("Connected to Hyperliquid")
        balance = client.get_balance()
        print(f"Equity: ${balance['equity']:.2f}")
        print(f"Available: ${balance['available']:.2f}")
        positions = client.get_positions()
        print(f"Open positions: {len(positions)}")
        for pos in positions:
            print(f"  {pos['symbol']}: {pos['side']} {pos['size']} @ {pos['entry_price']:.2f}")
    else:
        print("Connection failed")


if __name__ == "__main__":
    test_connection()
