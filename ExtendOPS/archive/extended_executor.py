#!/usr/bin/env python3
"""
Extended Exchange Executor - Production Ready
Consolidated trading executor for Extended Exchange
"""

import json
import sys
import os
import asyncio
from decimal import Decimal
from typing import Optional, Dict, List

from x10.perpetual.accounts import StarkPerpetualAccount
from x10.perpetual.trading_client import PerpetualTradingClient
from x10.perpetual.configuration import MAINNET_CONFIG, TESTNET_CONFIG
from x10.perpetual.orders import OrderSide


class ExtendedExecutor:
    """Production executor for Extended Exchange trading"""
    
    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            config_path = (
                "/home/kt/ZKputer/ExtendOPS/⚙️ Configuration/config/trading_config.json"
            )
        
        self.config_path = config_path
        self.trading_client = None
        self.stark_account = None
        self.config = None

    async def initialize(self) -> bool:
        """Initialize Extended trading client"""
        try:
            if not os.path.exists(self.config_path):
                print(f"❌ Config not found: {self.config_path}")
                return False

            with open(self.config_path, "r") as f:
                self.config = json.load(f)

            self.stark_account = StarkPerpetualAccount(
                vault=self.config["vault_number"],
                private_key=self.config["stark_private_key"],
                public_key=self.config["stark_public_key"],
                api_key=self.config["api_key"],
            )

            exchange_config = TESTNET_CONFIG if self.config.get("testnet", False) else MAINNET_CONFIG
            self.trading_client = PerpetualTradingClient(
                exchange_config,
                self.stark_account
            )

            print(f"✅ Extended client initialized")
            print(f"✅ Vault: {self.config['vault_number']}")
            print(f"✅ Mode: {'TESTNET' if self.config.get('testnet') else 'MAINNET'}")
            return True

        except Exception as e:
            print(f"❌ Initialization failed: {e}")
            return False

    async def set_leverage(self, market: str, leverage: int) -> bool:
        """Set leverage for a market"""
        try:
            await self.trading_client.account.update_leverage(
                market_name=market,
                leverage=Decimal(str(leverage))
            )
            print(f"✅ {market}: Set leverage to {leverage}x")
            return True
        except Exception as e:
            print(f"❌ {market}: Failed to set leverage - {e}")
            return False

    async def place_order(
        self,
        market: str,
        side: str,  # "buy" or "sell"
        size: float,
        price: float,
        leverage: Optional[int] = None
    ) -> Optional[Dict]:
        """
        Place an order on Extended
        
        Args:
            market: e.g. "BTC-USD", "ETH-USD"
            side: "buy" or "sell"
            size: Order size
            price: Limit price
            leverage: Optional leverage (will set if provided)
        
        Returns:
            Dict with order info or None on failure
        """
        try:
            # Set leverage if provided
            if leverage:
                await self.set_leverage(market, leverage)
                await asyncio.sleep(0.2)

            # Determine order side
            order_side = OrderSide.BUY if side.lower() == "buy" else OrderSide.SELL

            # Place order
            print(f"📝 {market}: Placing {side.upper()} order - {size} @ ${price}")
            
            placed_order = await self.trading_client.place_order(
                market_name=market,
                amount_of_synthetic=Decimal(str(size)),
                price=Decimal(str(price)),
                side=order_side,
                reduce_only=False,
                post_only=False
            )

            print(f"✅ {market}: Order placed! ID: {placed_order.data.id}")
            
            return {
                "status": "success",
                "order_id": placed_order.data.id,
                "market": market,
                "side": side,
                "size": size,
                "price": price
            }

        except Exception as e:
            print(f"❌ {market}: Order failed - {e}")
            return None

    async def place_stop_tp_orders(
        self,
        market: str,
        position_side: str,  # "long" or "short"
        size: float,
        stop_price: float,
        tp1_price: float,
        tp2_price: Optional[float] = None
    ) -> Dict[str, Optional[str]]:
        """
        Place stop loss and take profit orders
        
        Returns:
            Dict with order IDs: {"stop": id, "tp1": id, "tp2": id or None}
        """
        result = {"stop": None, "tp1": None, "tp2": None}
        
        # Determine close side
        close_side = OrderSide.SELL if position_side.lower() == "long" else OrderSide.BUY
        
        # Calculate TP sizes
        tp1_size = size / 2
        tp2_size = size - tp1_size if tp2_price else 0
        
        # Place Stop Loss
        try:
            print(f"📝 {market}: Placing Stop Loss @ ${stop_price}")
            stop_order = await self.trading_client.place_order(
                market_name=market,
                amount_of_synthetic=Decimal(str(size)),
                price=Decimal(str(stop_price)),
                side=close_side,
                reduce_only=False,
                post_only=False
            )
            result["stop"] = stop_order.data.id
            print(f"✅ {market}: Stop Loss placed - ID: {stop_order.data.id}")
        except Exception as e:
            print(f"❌ {market}: Stop Loss failed - {e}")
        
        await asyncio.sleep(0.3)
        
        # Place TP1
        try:
            print(f"📝 {market}: Placing TP1 @ ${tp1_price} (Size: {tp1_size})")
            tp1_order = await self.trading_client.place_order(
                market_name=market,
                amount_of_synthetic=Decimal(str(tp1_size)),
                price=Decimal(str(tp1_price)),
                side=close_side,
                reduce_only=False,
                post_only=False
            )
            result["tp1"] = tp1_order.data.id
            print(f"✅ {market}: TP1 placed - ID: {tp1_order.data.id}")
        except Exception as e:
            print(f"❌ {market}: TP1 failed - {e}")
        
        await asyncio.sleep(0.3)
        
        # Place TP2 if provided
        if tp2_price and tp2_size > 0:
            try:
                print(f"📝 {market}: Placing TP2 @ ${tp2_price} (Size: {tp2_size})")
                tp2_order = await self.trading_client.place_order(
                    market_name=market,
                    amount_of_synthetic=Decimal(str(tp2_size)),
                    price=Decimal(str(tp2_price)),
                    side=close_side,
                    reduce_only=False,
                    post_only=False
                )
                result["tp2"] = tp2_order.data.id
                print(f"✅ {market}: TP2 placed - ID: {tp2_order.data.id}")
            except Exception as e:
                print(f"❌ {market}: TP2 failed - {e}")
        
        return result

    async def cancel_all_orders(self, market: Optional[str] = None) -> int:
        """Cancel all open orders (optionally filtered by market)"""
        try:
            orders = await self.trading_client.account.get_open_orders()
            
            cancelled_count = 0
            for order in orders.data:
                if market is None or order.market == market:
                    await self.trading_client.orders.cancel_order(order_id=order.id)
                    print(f"✅ Cancelled: {order.market} Order ID {order.id}")
                    cancelled_count += 1
                    await asyncio.sleep(0.1)
            
            return cancelled_count
        except Exception as e:
            print(f"❌ Failed to cancel orders: {e}")
            return 0

    async def close_position(self, market: str) -> bool:
        """Close a position at market price"""
        try:
            # Get position
            positions = await self.trading_client.account.get_positions()
            position = None
            
            for pos in positions.data:
                if pos.market == market:
                    position = pos
                    break
            
            if not position:
                print(f"⚠️ No position found for {market}")
                return False
            
            # Determine close side
            close_side = OrderSide.SELL if str(position.side) == "LONG" else OrderSide.BUY
            
            # Get current price for market order
            markets = await self.trading_client.markets_info.get_markets([market])
            market_price = float(markets.data[0].market_stats.last_price)
            
            # Adjust price for slippage
            if close_side == OrderSide.SELL:
                close_price = market_price * 0.999  # Sell below market
            else:
                close_price = market_price * 1.001  # Buy above market
            
            #Place close order
            close_order = await self.trading_client.place_order(
                market_name=market,
                amount_of_synthetic=Decimal(str(float(position.size))),
                price=Decimal(str(close_price)),
                side=close_side,
                reduce_only=False,
                post_only=False
            )
            
            print(f"✅ {market}: Position closed - Order ID: {close_order.data.id}")
            return True
            
        except Exception as e:
            print(f"❌ {market}: Failed to close position - {e}")
            return False


async def main():
    """Example usage"""
    executor = ExtendedExecutor()
    if not await executor.initialize():
        return
    
    # Example: Get account status
    try:
        balance = await executor.trading_client.account.get_balance()
        print(f"\n💰 Equity: ${float(balance.data.equity):.2f}")
        
        positions = await executor.trading_client.account.get_positions()
        print(f"📊 Open Positions: {len(positions.data)}")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
