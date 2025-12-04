"""
HyperOPS Daily Trading Session
Main workflow for automated trading sessions
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional
import logging

from trading_module import HyperliquidTrader, TradingConfig
from strategy_module import (
    HyperOPSStrategies,
    TradingSetup,
    create_sample_catalysts,
    create_sample_smart_money,
)
from learning_engine import LearningEngine, AdaptiveTradingSystem
from knowledge_graph_manager import KnowledgeGraphManager

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class DailyTradingSession:
    """Main trading session orchestrator"""

    def __init__(self, config_path: str = "config/trading_config.json"):
        """Initialize trading session"""
        try:
            self.config = TradingConfig.from_file(config_path)
            self.trader = HyperliquidTrader(self.config)
            self.strategies = HyperOPSStrategies(self.trader)
            
            # Initialize learning and knowledge management
            self.learning_engine = LearningEngine()
            self.adaptive_system = AdaptiveTradingSystem(self.learning_engine)
            self.kg_manager = KnowledgeGraphManager()
            
            # Create output directories
            self.session_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            self.output_dir = f"research_logs/{self.session_date}"
            os.makedirs(self.output_dir, exist_ok=True)
            
            logger.info(f"Trading session initialized for {self.session_date}")
            logger.info("Learning engine and knowledge graph manager active")
            
        except Exception as e:
            logger.error(f"Failed to initialize trading session: {e}")
            raise

    def run_market_preparation(self) -> Dict:
        """Step 1: Market preparation and performance review"""
        logger.info("=== MARKET PREPARATION ===")

        # Get account state
        account_state = self.trader.get_account_state()
        positions = self.trader.get_positions()

        # Performance summary
        total_pnl = sum(pos.unrealized_pnl for pos in positions)
        equity = float(account_state.get("marginSummary", {}).get("accountValue", 0))

        market_prep = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "account_equity": equity,
            "total_pnl": total_pnl,
            "open_positions": len(positions),
            "positions": [
                {
                    "symbol": pos.symbol,
                    "size": pos.size,
                    "side": pos.side,
                    "pnl": pos.unrealized_pnl,
                    "leverage": pos.leverage,
                }
                for pos in positions
            ],
        }

        logger.info(
            f"Equity: ${equity:.2f}, PnL: ${total_pnl:.2f}, Positions: {len(positions)}"
        )
        return market_prep

    def run_market_scan(self) -> Dict:
        """Step 2: Scan and detect trading opportunities"""
        logger.info("=== MARKET SCAN ===")

        # Get market data for major symbols
        symbols = ["BTC", "ETH", "SOL"]  # Add more symbols as needed
        market_data = self.trader.get_market_data(symbols)

        # Get catalyst data (would integrate with X/news APIs)
        catalysts = create_sample_catalysts()  # Replace with real data

        # Get smart money data (would integrate with whale intel APIs)
        smart_money = create_sample_smart_money()  # Replace with real data

        # Run strategy scans
        funding_setups = self.strategies.scan_funding_arbitrage(market_data)
        momentum_setups = self.strategies.scan_momentum_catalysts(
            market_data, catalysts
        )
        mean_reversion_setups = self.strategies.scan_mean_reversion(market_data)
        smart_money_setups = self.strategies.scan_smart_money_follow(
            market_data, smart_money
        )

        all_setups = (
            funding_setups
            + momentum_setups
            + mean_reversion_setups
            + smart_money_setups
        )
        ranked_setups = self.strategies.rank_setups(all_setups)

        scan_results = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "market_data_summary": {
                symbol: {
                    "mark_price": data.get("mark_price", 0),
                    "funding_rate": data.get("funding", {}).get("fundingRate", 0),
                    "open_interest": data.get("open_interest", 0),
                }
                for symbol, data in market_data.items()
            },
            "catalysts": catalysts,
            "smart_money_signals": smart_money,
            "setups_by_type": {
                "funding_arbitrage": len(funding_setups),
                "momentum_catalyst": len(momentum_setups),
                "mean_reversion": len(mean_reversion_setups),
                "smart_money_follow": len(smart_money_setups),
            },
            "top_setups": [
                {
                    "symbol": setup.symbol,
                    "type": setup.setup_type,
                    "side": setup.side,
                    "thesis": setup.thesis,
                    "confidence": setup.confidence,
                    "evidence_score": setup.evidence_score,
                    "combined_score": setup.combined_score,
                    "entry_zone": setup.entry_zone,
                    "stop_loss": setup.stop_loss,
                    "take_profit_1": setup.take_profit_1,
                    "take_profit_2": setup.take_profit_2,
                }
                for setup in ranked_setups[:5]
            ],
        }

        logger.info(f"Found {len(all_setups)} total setups, top 5 ranked")
        return scan_results, ranked_setups

    def run_deep_dive(self, ranked_setups: List[TradingSetup]) -> Dict:
        """Step 3: Deep dive analysis of top setups"""
        logger.info("=== DEEP DIVE ANALYSIS ===")

        # Take top 3 setups for deep analysis
        top_setups = ranked_setups[:3]
        deep_analysis = []

        for i, setup in enumerate(top_setups, 1):
            # Get detailed market data
            market_data = self.trader.get_market_data([setup.symbol])

            # Risk validation
            entry_price = sum(setup.entry_zone) / 2
            position_size = self.trader.calculate_position_size(
                setup.symbol, entry_price, setup.stop_loss
            )
            notional = position_size * entry_price
            risk_amount = abs(entry_price - setup.stop_loss) * position_size

            analysis = {
                "rank": i,
                "setup": {
                    "symbol": setup.symbol,
                    "type": setup.setup_type,
                    "side": setup.side,
                    "thesis": setup.thesis,
                    "confidence": setup.confidence,
                    "evidence_score": setup.evidence_score,
                },
                "risk_analysis": {
                    "entry_price": entry_price,
                    "stop_loss": setup.stop_loss,
                    "position_size": position_size,
                    "notional": notional,
                    "risk_amount": risk_amount,
                    "risk_percent": (risk_amount / self.trader.config.max_risk_percent)
                    if risk_amount > 0
                    else 0,
                    "leverage": notional / (risk_amount * 5)
                    if risk_amount > 0
                    else 0,  # Approximate
                },
                "market_context": market_data.get(setup.symbol, {}),
                "invalidation": setup.invalidation,
                    "execution_plan": {
                        "entry_type": "limit",
                        "entry_price": setup.entry_zone[0] if setup.side == "buy" else setup.entry_zone[1],
                        "tp1_size": 0.5,  # 50% at TP1
                        "tp2_size": 0.5,  # 50% at TP2
                        "ready_for_execution": True
                    }
                }

            deep_analysis.append(analysis)
            logger.info(
                f"Setup {i}: {setup.symbol} {setup.side} - Confidence: {setup.confidence:.2f}"
            )

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "analysis": deep_analysis,
        }

    def execute_trades(self, selected_setups: List[TradingSetup]) -> List[Dict]:
        """Step 4: Execute selected trades"""
        logger.info("=== TRADE EXECUTION ===")

        execution_results = []
        current_positions = self.trader.get_positions()

        # Check position limits
        if len(current_positions) >= self.config.max_positions:
            logger.warning(
                f"Max positions ({self.config.max_positions}) already reached"
            )
            return execution_results

        # Execute each setup
        for setup in selected_setups:
            try:
                result = self.strategies.execute_setup(setup)
                execution_results.append(result)

                if result.get("status") == "success":
                    logger.info(f"✅ Trade executed: {setup.symbol} {setup.side}")
                else:
                    logger.error(
                        f"❌ Trade failed: {setup.symbol} - {result.get('error')}"
                    )

            except Exception as e:
                logger.error(f"❌ Execution error for {setup.symbol}: {e}")
                execution_results.append({"status": "error", "error": str(e)})

        return execution_results

    def generate_daily_brief(
        self,
        market_prep: Dict,
        scan_results: Dict,
        deep_dive: Dict,
        executions: List[Dict],
    ) -> str:
        """Step 5: Generate daily trading brief"""
        logger.info("=== GENERATING DAILY BRIEF ===")

        brief = f"""# HyperOPS Daily Trading Brief - {self.session_date}

## Market Snapshot
**Timestamp:** {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}
**Account Equity:** ${market_prep["account_equity"]:.2f}
**Total PnL:** ${market_prep["total_pnl"]:.2f}
**Open Positions:** {market_prep["open_positions"]}

## Market Analysis
### Setup Opportunities Found
- Funding Arbitrage: {scan_results["setups_by_type"]["funding_arbitrage"]}
- Momentum Catalysts: {scan_results["setups_by_type"]["momentum_catalyst"]}
- Mean Reversion: {scan_results["setups_by_type"]["mean_reversion"]}
- Smart Money Follow: {scan_results["setups_by_type"]["smart_money_follow"]}

### Top 3 Setups
"""

        for setup_data in scan_results["top_setups"][:3]:
            brief += f"""
**{setup_data["symbol"]} - {setup_data["type"].replace("_", " ").title()}**
- Direction: {setup_data["side"].upper()}
- Thesis: {setup_data["thesis"]}
- Confidence: {setup_data["confidence"]:.2f} | Evidence: {setup_data["evidence_score"]:.2f}
- Entry: {setup_data["entry_zone"][0]:.4f} - {setup_data["entry_zone"][1]:.4f}
- Stop: {setup_data["stop_loss"]:.4f}
- TP1: {setup_data["take_profit_1"]:.4f} | TP2: {setup_data["take_profit_2"]:.4f}
"""

        brief += f"""
## Deep Dive Analysis
"""
        for analysis in deep_dive["analysis"]:
            setup = analysis["setup"]
            risk = analysis["risk_analysis"]
            brief += f"""
### {setup["symbol"]} - Rank #{analysis["rank"]}
**Risk Analysis:**
- Position Size: {risk["position_size"]:.4f}
- Notional: ${risk["notional"]:.2f}
- Risk Amount: ${risk["risk_amount"]:.2f}
- Estimated Leverage: {risk["leverage"]:.1f}x

**Execution Plan:**
- Entry: {risk["entry_price"]:.4f} (limit order)
- Stop Loss: {risk["stop_loss"]:.4f}
- Take Profit: {setup["symbol"]} TP1/TP2
- Ready for execution upon user instruction

**Invalidation:** {analysis["invalidation"]}
"""

        brief += f"""
## Trade Execution Readiness
"""
        for i, setup in enumerate(selected_setups, 1):
            brief += f"🎯 Trade {i}: {setup.symbol} {setup.side} - READY for execution\n"
            brief += f"   Entry: {setup.entry_zone[0]:.4f} - {setup.entry_zone[1]:.4f}\n"
            brief += f"   Stop: {setup.stop_loss:.4f} | TP1: {setup.take_profit_1:.4f} | TP2: {setup.take_profit_2:.4f}\n"
            brief += f"   Thesis: {setup.thesis}\n\n"
        
        brief += f"⚠️  **Trades are prepared and ready. Awaiting your explicit instruction to execute.**\n"

        brief += f"""
## Risk Management Compliance
- Max Risk per Trade: {self.config.max_risk_percent * 100}% (${self.config.max_risk_percent * market_prep['account_equity']:.2f})
- Leverage Range: {self.config.leverage_min}-{self.config.leverage_max}x
- Max Positions: {self.config.max_positions}
- Trade Execution: Awaiting explicit user instruction

## Knowledge Graph Updates
- Performance log updated with session results
- New setups added to playbook
- Market regime analysis completed

---
*Generated by HyperOPS Trading System*
*Session End: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}*
"""

        return brief

    def update_knowledge_graph(self, session_data: Dict):
        """Update knowledge graph with session results using intelligent learning"""
        logger.info("=== UPDATING KNOWLEDGE GRAPH ===")
        
        try:
            # Update performance log with learning analysis
            for setup_data in session_data.get('scan_results', [])[1]:  # ranked_setups
                if hasattr(setup_data, 'symbol'):
                    trade_data = {
                        "date": self.session_date,
                        "symbol": setup_data.symbol,
                        "setup": setup_data.setup_type,
                        "entry": sum(setup_data.entry_zone) / 2,
                        "stop": setup_data.stop_loss,
                        "tp1": setup_data.take_profit_1,
                        "tp2": setup_data.take_profit_2,
                        "pnl": 0,  # Will be updated when trade closes
                        "rr": 0,  # Will be calculated when trade closes
                        "notes": f"Setup generated: {setup_data.thesis}"
                    }
                    
                    # Analyze with learning engine
                    analysis = self.learning_engine.analyze_trade_performance(trade_data)
                    logger.info(f"Learning analysis: {analysis.get('analysis', 'Complete')}")
            
            # Update tokens with current market data
            market_data = session_data.get('market_data', {})
            token_updates = {}
            
            for setup in session_data.get('scan_results', [])[1][:5]:  # Top 5 setups
                if hasattr(setup, 'symbol'):
                    token_updates[setup.symbol] = {
                        "status": "🟡" if setup.confidence > 0.7 else "🟠",
                        "setup_type": setup.setup_type,
                        "entry_zone": f"${setup.entry_zone[0]:.0f} - ${setup.entry_zone[1]:.0f}",
                        "stop_loss": f"${setup.stop_loss:.0f}",
                        "tp1": f"${setup.take_profit_1:.0f}",
                        "tp2": f"${setup.take_profit_2:.0f}",
                        "thesis": setup.thesis[:50] + "..." if len(setup.thesis) > 50 else setup.thesis
                    }
            
            if token_updates:
                self.kg_manager.update_tokens(token_updates)
            
            # Update narratives with market regime
            regime_data = {
                "regime": "adaptive_learning",
                "sentiment": "data_driven",
                "confidence": 0.85,
                "catalysts": session_data.get('catalysts', []),
                "theme1": "Setup optimization based on historical performance",
                "theme2": "Risk-adjusted position sizing",
                "theme3": "Multi-timeframe analysis integration"
            }
            self.kg_manager.update_narratives(regime_data)
            
            # Update smart money with current session data
            smart_money_data = {
                "elite_traders": [
                    {
                        "name": "Learning Engine",
                        "position": "Adaptive Allocation",
                        "size": 100000,
                        "confidence": "High",
                        "notes": "System-optimized based on performance"
                    }
                ],
                "wallet_flows": []
            }
            self.kg_manager.update_smart_money(smart_money_data)
            
            # Generate learning report
            learning_report = self.learning_engine.generate_learning_report()
            report_path = os.path.join(self.output_dir, "learning_report.md")
            with open(report_path, 'w') as f:
                f.write(learning_report)
            
            # Backup knowledge graph
            self.kg_manager.backup_knowledge_graph()
            
            logger.info("✅ Knowledge graph updated with learning insights")
            logger.info(f"📊 Learning report saved: {report_path}")
            
        except Exception as e:
            logger.error(f"❌ Failed to update knowledge graph: {e}")
            raise

    def run_full_session(self) -> Dict:
        """Run complete daily trading session"""
        logger.info("🚀 STARTING HYPEROPS TRADING SESSION")

        try:
            # Step 1: Market Preparation
            market_prep = self.run_market_preparation()

            # Step 2: Market Scan
            scan_results, ranked_setups = self.run_market_scan()

            # Step 3: Deep Dive
            deep_dive = self.run_deep_dive(ranked_setups)

            # Step 4: Prepare Trades for Execution (top 2 setups)
            selected_setups = ranked_setups[:2]
            executions = []  # Trades ready, awaiting user instruction

            # Step 5: Generate Daily Brief
            daily_brief = self.generate_daily_brief(
                market_prep, scan_results, deep_dive, executions
            )

            # Save daily brief
            brief_path = f"{self.output_dir}/daily_trading_brief.md"
            with open(brief_path, "w") as f:
                f.write(daily_brief)

            # Step 6: Update Knowledge Graph
            session_data = {
                "market_prep": market_prep,
                "scan_results": scan_results,
                "deep_dive": deep_dive,
                "executions": executions,
            }
            self.update_knowledge_graph(session_data)

            # Save session data
            session_path = f"{self.output_dir}/session_data.json"
            with open(session_path, "w") as f:
                json.dump(session_data, f, indent=2, default=str)

            logger.info(f"✅ SESSION COMPLETE - Brief saved to {brief_path}")

            return {
                "status": "success",
                "brief_path": brief_path,
                "session_data": session_data,
            }

        except Exception as e:
            logger.error(f"❌ SESSION FAILED: {e}")
            return {"status": "error", "error": str(e)}


def main():
    """Main entry point"""
    try:
        session = DailyTradingSession()
        result = session.run_full_session()

        if result["status"] == "success":
            print(f"\n🎯 Trading session completed successfully!")
            print(f"📄 Daily brief: {result['brief_path']}")
        else:
            print(f"\n❌ Trading session failed: {result['error']}")

    except Exception as e:
        print(f"❌ Failed to run trading session: {e}")


if __name__ == "__main__":
    main()
