"""
HyperOPS Trading Strategy Module
Implements the thesis-driven trading strategies from HyperOPS protocol
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timezone
import math

from trading_module import HyperliquidTrader, TradingConfig, OrderSpec, Position


@dataclass
class TradingSetup:
    """Trading setup with thesis and risk parameters"""

    symbol: str
    setup_type: str  # "funding_arb", "momentum_catalyst", "liquidity_hunt", "mean_reversion", "smart_money_follow"
    side: str  # "long" or "short"
    thesis: str
    entry_zone: Tuple[float, float]  # (min_price, max_price)
    stop_loss: float
    take_profit_1: float
    take_profit_2: float
    confidence: float  # 0.0 to 1.0
    evidence_score: float  # 0.0 to 1.0
    invalidation: str
    catalyst_details: Optional[Dict] = None


@dataclass
class MarketEvidence:
    """Market evidence for trading decisions"""

    funding_rate: float
    funding_percentile: float  # 0.0 to 1.0
    oi_change_24h: float
    oi_change_percentile: float
    basis_rate: float
    liquidity_gap: float
    volume_profile: Dict
    whale_activity: List[Dict]
    smart_money_signals: List[Dict]


class HyperOPSStrategies:
    """Implements HyperOPS trading strategies"""

    def __init__(self, trader: HyperliquidTrader):
        self.trader = trader
        self.min_funding_threshold = 0.001  # 0.1%
        self.extreme_funding_threshold = 0.005  # 0.5%
        self.min_oi_threshold = 1000000  # $1M
        self.min_volume_threshold = 500000  # $500K

    def scan_funding_arbitrage(self, market_data: Dict) -> List[TradingSetup]:
        """Scan for funding arbitrage opportunities"""
        setups = []

        for symbol, data in market_data.items():
            if not data.get("funding"):
                continue

            funding = data["funding"]
            funding_rate = float(funding.get("fundingRate", 0))

            # Check for extreme funding rates
            if abs(funding_rate) > self.min_funding_threshold:
                # Determine direction based on funding
                if funding_rate > self.extreme_funding_threshold:
                    # High positive funding = short opportunity
                    side = "sell"
                    thesis = f"Extreme funding rate: {funding_rate:.4f} (> {self.extreme_funding_threshold})"
                elif funding_rate < -self.extreme_funding_threshold:
                    # High negative funding = long opportunity
                    side = "buy"
                    thesis = f"Extreme negative funding: {funding_rate:.4f} (< -{self.extreme_funding_threshold})"
                else:
                    continue

                # Calculate entry and exit levels
                current_price = data.get("mark_price", 0)
                if current_price == 0:
                    continue

                # Use 2x ATR approximation for stop (simplified)
                atr_approx = current_price * 0.02  # 2% price approximation

                if side == "buy":
                    stop_loss = current_price - atr_approx
                    take_profit_1 = current_price + (atr_approx * 1.5)
                    take_profit_2 = current_price + (atr_approx * 3)
                    entry_zone = (
                        current_price * 0.998,
                        current_price * 1.002,
                    )  # Tight zone
                else:
                    stop_loss = current_price + atr_approx
                    take_profit_1 = current_price - (atr_approx * 1.5)
                    take_profit_2 = current_price - (atr_approx * 3)
                    entry_zone = (current_price * 0.998, current_price * 1.002)

                setup = TradingSetup(
                    symbol=symbol,
                    setup_type="funding_arb",
                    side=side,
                    thesis=thesis,
                    entry_zone=entry_zone,
                    stop_loss=stop_loss,
                    take_profit_1=take_profit_1,
                    take_profit_2=take_profit_2,
                    confidence=min(
                        abs(funding_rate) / self.extreme_funding_threshold, 1.0
                    ),
                    evidence_score=0.7,  # Base score for funding setups
                    invalidation=f"Funding rate normalizes below {self.min_funding_threshold}",
                    catalyst_details={"funding_rate": funding_rate},
                )

                setups.append(setup)

        return setups

    def scan_momentum_catalysts(
        self, market_data: Dict, catalysts: List[Dict]
    ) -> List[TradingSetup]:
        """Scan for momentum catalyst setups"""
        setups = []

        for catalyst in catalysts:
            symbol = catalyst.get("symbol")
            if not symbol or symbol not in market_data:
                continue

            data = market_data[symbol]
            current_price = data.get("mark_price", 0)
            if current_price == 0:
                continue

            # Check volume and OI requirements
            meta = data.get("meta", {})
            if not self._check_liquidity_requirements(meta):
                continue

            catalyst_type = catalyst.get("type", "unknown")
            impact_score = catalyst.get("impact_score", 0.5)

            # Determine direction based on catalyst
            if catalyst_type in ["upgrade", "partnership", "listing", "bullish_news"]:
                side = "buy"
                thesis = (
                    f"Bullish catalyst: {catalyst.get('description', 'Positive news')}"
                )
            elif catalyst_type in [
                "hack",
                "delisting",
                "bearish_news",
                "regulatory_fud",
            ]:
                side = "sell"
                thesis = (
                    f"Bearish catalyst: {catalyst.get('description', 'Negative news')}"
                )
            else:
                continue

            # Calculate levels based on volatility
            volatility = catalyst.get("expected_volatility", 0.05)  # 5% default
            atr_approx = current_price * volatility

            if side == "buy":
                # Breakout entry above current level
                entry_zone = (current_price * 1.005, current_price * 1.015)
                stop_loss = current_price - (atr_approx * 0.8)
                take_profit_1 = current_price + (atr_approx * 2)
                take_profit_2 = current_price + (atr_approx * 4)
            else:
                # Breakdown entry below current level
                entry_zone = (current_price * 0.985, current_price * 0.995)
                stop_loss = current_price + (atr_approx * 0.8)
                take_profit_1 = current_price - (atr_approx * 2)
                take_profit_2 = current_price - (atr_approx * 4)

            setup = TradingSetup(
                symbol=symbol,
                setup_type="momentum_catalyst",
                side=side,
                thesis=thesis,
                entry_zone=entry_zone,
                stop_loss=stop_loss,
                take_profit_1=take_profit_1,
                take_profit_2=take_profit_2,
                confidence=impact_score,
                evidence_score=0.6 + (impact_score * 0.3),
                invalidation=f"Catalyst fails or price breaks {stop_loss:.4f}",
                catalyst_details=catalyst,
            )

            setups.append(setup)

        return setups

    def scan_mean_reversion(self, market_data: Dict) -> List[TradingSetup]:
        """Scan for mean reversion opportunities"""
        setups = []

        for symbol, data in market_data.items():
            current_price = data.get("mark_price", 0)
            index_price = data.get("index_price", 0)

            if current_price == 0 or index_price == 0:
                continue

            # Calculate basis (perp premium/discount)
            basis = (current_price - index_price) / index_price

            # Look for extreme basis deviations
            extreme_basis_threshold = 0.02  # 2%
            if abs(basis) < extreme_basis_threshold:
                continue

            # Check funding confirmation
            funding = data.get("funding", {})
            funding_rate = float(funding.get("fundingRate", 0))

            # Confirm basis and funding alignment
            if (basis > extreme_basis_threshold and funding_rate > 0) or (
                basis < -extreme_basis_threshold and funding_rate < 0
            ):
                # Fade the extreme
                side = "sell" if basis > 0 else "buy"
                thesis = f"Extreme basis: {basis:.4f} with funding confirmation: {funding_rate:.4f}"

                # Calculate reversion levels
                reversion_target = index_price
                atr_approx = current_price * 0.03  # 3% volatility

                if side == "sell":
                    entry_zone = (current_price * 0.998, current_price * 1.002)
                    stop_loss = current_price + (atr_approx * 0.5)
                    take_profit_1 = current_price - (atr_approx * 1.5)
                    take_profit_2 = reversion_target
                else:
                    entry_zone = (current_price * 0.998, current_price * 1.002)
                    stop_loss = current_price - (atr_approx * 0.5)
                    take_profit_1 = current_price + (atr_approx * 1.5)
                    take_profit_2 = reversion_target

                setup = TradingSetup(
                    symbol=symbol,
                    setup_type="mean_reversion",
                    side=side,
                    thesis=thesis,
                    entry_zone=entry_zone,
                    stop_loss=stop_loss,
                    take_profit_1=take_profit_1,
                    take_profit_2=take_profit_2,
                    confidence=min(abs(basis) / extreme_basis_threshold, 1.0),
                    evidence_score=0.65,
                    invalidation=f"Basis normalizes below {extreme_basis_threshold}",
                    catalyst_details={"basis": basis, "funding_rate": funding_rate},
                )

                setups.append(setup)

        return setups

    def scan_smart_money_follow(
        self, market_data: Dict, smart_money_trades: List[Dict]
    ) -> List[TradingSetup]:
        """Scan for smart money following opportunities"""
        setups = []

        # Aggregate smart money signals by symbol
        symbol_signals = {}
        for trade in smart_money_trades:
            symbol = trade.get("symbol")
            if not symbol or symbol not in market_data:
                continue

            if symbol not in symbol_signals:
                symbol_signals[symbol] = []
            symbol_signals[symbol].append(trade)

        for symbol, signals in symbol_signals.items():
            if len(signals) < 2:  # Need multiple signals
                continue

            data = market_data[symbol]
            current_price = data.get("mark_price", 0)
            if current_price == 0:
                continue

            # Calculate net smart money bias
            total_notional = sum(s.get("notional", 0) for s in signals)
            net_exposure = sum(
                s.get("notional", 0) * (1 if s.get("side") == "buy" else -1)
                for s in signals
            )

            if total_notional == 0:
                continue

            bias_ratio = net_exposure / total_notional

            # Need strong conviction (70%+ one-sided)
            if abs(bias_ratio) < 0.7:
                continue

            side = "buy" if bias_ratio > 0 else "sell"

            # Calculate average entry price of smart money
            weighted_price = (
                sum(
                    s.get("price", current_price) * s.get("notional", 0)
                    for s in signals
                )
                / total_notional
            )

            thesis = f"Smart money bias: {bias_ratio:.2f} with ${total_notional:,.0f} notional"

            # Use smart money levels for entry
            atr_approx = current_price * 0.025

            if side == "buy":
                entry_zone = (weighted_price * 0.995, weighted_price * 1.005)
                stop_loss = weighted_price - (atr_approx * 0.8)
                take_profit_1 = weighted_price + (atr_approx * 2)
                take_profit_2 = weighted_price + (atr_approx * 3.5)
            else:
                entry_zone = (weighted_price * 0.995, weighted_price * 1.005)
                stop_loss = weighted_price + (atr_approx * 0.8)
                take_profit_1 = weighted_price - (atr_approx * 2)
                take_profit_2 = weighted_price - (atr_approx * 3.5)

            setup = TradingSetup(
                symbol=symbol,
                setup_type="smart_money_follow",
                side=side,
                thesis=thesis,
                entry_zone=entry_zone,
                stop_loss=stop_loss,
                take_profit_1=take_profit_1,
                take_profit_2=take_profit_2,
                confidence=min(abs(bias_ratio), 1.0),
                evidence_score=0.7 + (abs(bias_ratio) * 0.2),
                invalidation=f"Smart money reverses position or price breaks {stop_loss:.4f}",
                catalyst_details={
                    "bias_ratio": bias_ratio,
                    "total_notional": total_notional,
                    "signal_count": len(signals),
                    "avg_price": weighted_price,
                },
            )

            setups.append(setup)

        return setups

    def _check_liquidity_requirements(self, meta: Dict) -> bool:
        """Check if symbol meets liquidity requirements"""
        # This would need real volume/OI data from the API
        # For now, assume major symbols pass
        symbol = meta.get("name", "")
        major_symbols = ["BTC", "ETH", "SOL"]
        return any(major in symbol for major in major_symbols)

    def rank_setups(self, setups: List[TradingSetup]) -> List[TradingSetup]:
        """Rank setups by combined score"""
        for setup in setups:
            # Combine confidence and evidence score
            setup.combined_score = (setup.confidence * 0.6) + (
                setup.evidence_score * 0.4
            )

        return sorted(setups, key=lambda x: x.combined_score, reverse=True)

    def execute_setup(self, setup: TradingSetup) -> Dict:
        """Execute a trading setup"""
        try:
            # Calculate position size
            entry_price = sum(setup.entry_zone) / 2  # Use midpoint
            position_size = self.trader.calculate_position_size(
                setup.symbol, entry_price, setup.stop_loss
            )

            if position_size <= 0:
                return {"status": "error", "error": "Invalid position size"}

            # Create limit order at bottom of entry zone for longs, top for shorts
            if setup.side == "buy":
                entry_price = setup.entry_zone[0]  # Bottom of zone
            else:
                entry_price = setup.entry_zone[1]  # Top of zone

            order = OrderSpec(
                symbol=setup.symbol,
                side=setup.side,
                order_type="limit",
                size=position_size,
                price=entry_price,
                time_in_force="gtc",
            )

            result = self.trader.place_order(order)

            if result.get("status") == "ok":
                # Setup take-profit orders if main order filled
                # This would be handled by order management system
                return {
                    "status": "success",
                    "setup": setup,
                    "order": result,
                    "position_size": position_size,
                    "entry_price": entry_price,
                }
            else:
                return {
                    "status": "error",
                    "error": result.get("error", "Unknown error"),
                }

        except Exception as e:
            return {"status": "error", "error": str(e)}


# Example catalyst data structure
def create_sample_catalysts() -> List[Dict]:
    """Create sample catalyst data for testing"""
    return [
        {
            "symbol": "ETH",
            "type": "upgrade",
            "description": "Ethereum Dencun upgrade successful",
            "impact_score": 0.8,
            "expected_volatility": 0.06,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
        {
            "symbol": "SOL",
            "type": "partnership",
            "description": "Major DeFi protocol announces Solana integration",
            "impact_score": 0.7,
            "expected_volatility": 0.08,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    ]


# Example smart money data structure
def create_sample_smart_money() -> List[Dict]:
    """Create sample smart money data for testing"""
    return [
        {
            "symbol": "BTC",
            "side": "buy",
            "notional": 500000,
            "price": 43500,
            "trader": "whale_001",
            "confidence": "high",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
        {
            "symbol": "BTC",
            "side": "buy",
            "notional": 300000,
            "price": 43450,
            "trader": "fund_abc",
            "confidence": "high",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    ]
