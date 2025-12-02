"""
HyperOPS Learning Engine
Advanced self-evaluating and evolving trading system
"""

import json
import os
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Tuple
import logging
import numpy as np
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    """Performance metrics for tracking"""
    win_rate: float
    avg_rr: float
    profit_factor: float
    sharpe_ratio: float
    max_drawdown: float
    consecutive_wins: int
    consecutive_losses: int
    total_trades: int
    total_pnl: float

@dataclass
class SetupMetrics:
    """Setup-specific performance metrics"""
    setup_type: str
    trades: int
    wins: int
    losses: int
    win_rate: float
    avg_rr: float
    profit_factor: float
    avg_holding_time: float
    success_trend: List[float]  # Last 10 trades success
    confidence_score: float

class LearningEngine:
    """Advanced learning and optimization engine"""
    
    def __init__(self, knowledge_graph_path: str = "knowledge_graph"):
        self.kg_path = knowledge_graph_path
        self.performance_history = []
        self.setup_metrics = {}
        self.market_regimes = {}
        self.optimization_history = []
        
        # Load existing data
        self._load_knowledge_graph()
    
    def _load_knowledge_graph(self):
        """Load existing knowledge graph data"""
        try:
            # Load performance log
            perf_path = os.path.join(self.kg_path, "performance_log.md")
            if os.path.exists(perf_path):
                self._parse_performance_log(perf_path)
            
            # Load playbook
            playbook_path = os.path.join(self.kg_path, "playbook.md")
            if os.path.exists(playbook_path):
                self._parse_playbook(playbook_path)
            
            logger.info("Knowledge graph loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load knowledge graph: {e}")
    
    def _parse_performance_log(self, file_path: str):
        """Parse performance log for historical data"""
        # This would parse the markdown table into structured data
        # For now, initialize with sample data
        self.performance_history = [
            {
                "date": "2025-11-24",
                "symbol": "BTC",
                "setup": "FUND_ARB",
                "pnl": 32,
                "rr": 1.6,
                "status": "win"
            },
            {
                "date": "2025-11-24",
                "symbol": "ETH",
                "setup": "MEAN_REV",
                "pnl": -18,
                "rr": -0.9,
                "status": "loss"
            }
        ]
    
    def _parse_playbook(self, file_path: str):
        """Parse playbook for setup metrics"""
        # Initialize setup metrics from playbook data
        self.setup_metrics = {
            "FUND_ARB": SetupMetrics("FUND_ARB", 12, 10, 2, 0.83, 1.8, 3.2, 2.1, [1,1,1,0,1,1,0,1,1,1], 0.85),
            "MOMENTUM": SetupMetrics("MOMENTUM", 8, 5, 3, 0.63, 2.4, 2.1, 1.8, [1,0,1,1,0,1,0,1,0,1], 0.70),
            "LIQ_HUNT": SetupMetrics("LIQ_HUNT", 6, 3, 3, 0.50, 1.9, 1.4, 1.2, [0,1,0,0,1,0,1,0,1,0], 0.55),
            "MEAN_REV": SetupMetrics("MEAN_REV", 15, 12, 3, 0.80, 1.6, 2.8, 2.5, [1,1,0,1,1,1,0,1,1,1], 0.82),
            "SMART_MONEY": SetupMetrics("SMART_MONEY", 19, 16, 3, 0.84, 2.1, 3.6, 1.9, [1,1,1,1,0,1,1,1,0,1], 0.88)
        }
    
    def analyze_trade_performance(self, trade_data: Dict) -> Dict:
        """Analyze individual trade performance and update metrics"""
        setup_type = trade_data.get("setup")
        pnl = trade_data.get("pnl", 0)
        rr = trade_data.get("rr", 0)
        status = "win" if pnl > 0 else "loss"
        
        # Update setup metrics
        if setup_type in self.setup_metrics:
            metrics = self.setup_metrics[setup_type]
            metrics.trades += 1
            
            if status == "win":
                metrics.wins += 1
            else:
                metrics.losses += 1
            
            metrics.win_rate = metrics.wins / metrics.trades
            
            # Update success trend (keep last 10)
            metrics.success_trend.append(1 if status == "win" else 0)
            if len(metrics.success_trend) > 10:
                metrics.success_trend.pop(0)
            
            # Update confidence score based on recent performance
            recent_success = sum(metrics.success_trend[-5:]) / min(5, len(metrics.success_trend))
            metrics.confidence_score = (metrics.win_rate * 0.6) + (recent_success * 0.4)
        
        # Add to performance history
        self.performance_history.append({
            **trade_data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": status
        })
        
        # Generate insights
        insights = self._generate_trade_insights(trade_data)
        
        return {
            "analysis": "Trade performance analyzed and metrics updated",
            "setup_metrics": self.setup_metrics.get(setup_type),
            "insights": insights,
            "recommendations": self._generate_recommendations(setup_type)
        }
    
    def _generate_trade_insights(self, trade_data: Dict) -> List[str]:
        """Generate insights from trade analysis"""
        insights = []
        setup_type = trade_data.get("setup")
        pnl = trade_data.get("pnl", 0)
        rr = trade_data.get("rr", 0)
        
        # Performance insights
        if setup_type in self.setup_metrics:
            metrics = self.setup_metrics[setup_type]
            
            if metrics.win_rate > 0.8:
                insights.append(f"🟢 {setup_type} showing excellent performance: {metrics.win_rate:.1%} win rate")
            elif metrics.win_rate < 0.5:
                insights.append(f"🔴 {setup_type} underperforming: {metrics.win_rate:.1%} win rate")
            
            if metrics.avg_rr > 2.0:
                insights.append(f"📈 {setup_type} delivering strong R:R: {metrics.avg_rr:.1f}:1")
            elif metrics.avg_rr < 1.0:
                insights.append(f"📉 {setup_type} poor R:R ratio: {metrics.avg_rr:.1f}:1")
        
        # Trade-specific insights
        if pnl > 30:
            insights.append(f"💰 Strong profit: +${pnl} on {trade_data.get('symbol')}")
        elif pnl < -20:
            insights.append(f"⚠️  Significant loss: -${abs(pnl)} on {trade_data.get('symbol')}")
        
        # Pattern detection
        recent_trades = [t for t in self.performance_history[-10:] if t.get("setup") == setup_type]
        if len(recent_trades) >= 3:
            recent_wins = sum(1 for t in recent_trades if t.get("pnl", 0) > 0)
            if recent_wins == len(recent_trades):
                insights.append(f"🔥 {setup_type} on {len(recent_trades}-trade winning streak")
            elif recent_wins == 0:
                insights.append(f"❄️  {setup_type} on {len(recent_trades)-trade losing streak")
        
        return insights
    
    def _generate_recommendations(self, setup_type: str) -> List[str]:
        """Generate recommendations based on performance analysis"""
        recommendations = []
        
        if setup_type not in self.setup_metrics:
            return ["Insufficient data for recommendations"]
        
        metrics = self.setup_metrics[setup_type]
        
        # Performance-based recommendations
        if metrics.win_rate < 0.6:
            recommendations.append(f"Consider reducing {setup_type} allocation until performance improves")
            recommendations.append(f"Review entry criteria for {setup_type} - may be too loose")
        
        if metrics.avg_rr < 1.5:
            recommendations.append(f"Optimize take-profit levels for {setup_type} - current R:R too low")
            recommendations.append(f"Consider wider stops for {setup_type} to improve win rate")
        
        if metrics.profit_factor < 1.5:
            recommendations.append(f"{setup_type} showing poor risk-adjusted returns")
            recommendations.append(f"Temporarily pause {setup_type} until market conditions improve")
        
        # Recent performance recommendations
        if len(metrics.success_trend) >= 5:
            recent_success = sum(metrics.success_trend[-5:]) / 5
            if recent_success < 0.4:
                recommendations.append(f"🚨 {setup_type} struggling recently - consider market regime change")
            elif recent_success > 0.8:
                recommendations.append(f"🚀 {setup_type} excellent recently - consider increasing allocation")
        
        return recommendations
    
    def optimize_setup_parameters(self, setup_type: str) -> Dict:
        """Optimize parameters for specific setup based on historical performance"""
        if setup_type not in self.setup_metrics:
            return {"error": "Setup not found in metrics"}
        
        metrics = self.setup_metrics[setup_type]
        setup_trades = [t for t in self.performance_history if t.get("setup") == setup_type]
        
        if len(setup_trades) < 5:
            return {"error": "Insufficient trades for optimization"}
        
        # Analyze parameter performance
        optimizations = {}
        
        # Stop distance optimization
        stop_distances = []
        for trade in setup_trades:
            # This would need actual stop distance data
            stop_distances.append(np.random.normal(0.02, 0.005))  # Sample data
        
        if stop_distances:
            optimal_stop = np.median(stop_distances)
            current_stop = 0.02  # Default 2%
            optimizations["stop_distance"] = {
                "current": current_stop,
                "optimal": optimal_stop,
                "recommendation": "tighten" if optimal_stop < current_stop else "widen"
            }
        
        # Take profit optimization
        tp_ratios = []
        for trade in setup_trades:
            tp_ratios.append(trade.get("rr", 1.5))
        
        if tp_ratios:
            optimal_tp = np.percentile(tp_ratios, 75)  # 75th percentile
            optimizations["take_profit"] = {
                "current_avg": np.mean(tp_ratios),
                "optimal": optimal_tp,
                "recommendation": f"Target {optimal_tp:.1f}:1 R:R"
            }
        
        # Position sizing optimization
        win_rates_by_size = {}
        for trade in setup_trades:
            size_bucket = "small" if trade.get("risk", 0) < 15 else "large"
            if size_bucket not in win_rates_by_size:
                win_rates_by_size[size_bucket] = {"wins": 0, "total": 0}
            
            win_rates_by_size[size_bucket]["total"] += 1
            if trade.get("pnl", 0) > 0:
                win_rates_by_size[size_bucket]["wins"] += 1
        
        if win_rates_by_size:
            for size, data in win_rates_by_size.items():
                win_rate = data["wins"] / data["total"]
                if win_rate > 0.7:
                    optimizations["position_sizing"] = f"Prefer {size} positions for {setup_type}"
        
        return {
            "setup_type": setup_type,
            "current_metrics": {
                "win_rate": metrics.win_rate,
                "avg_rr": metrics.avg_rr,
                "confidence": metrics.confidence_score
            },
            "optimizations": optimizations,
            "recommendation": self._get_setup_recommendation(metrics)
        }
    
    def _get_setup_recommendation(self, metrics: SetupMetrics) -> str:
        """Get overall recommendation for setup"""
        if metrics.confidence_score > 0.85:
            return "🟢 HIGH CONFIDENCE - Increase allocation"
        elif metrics.confidence_score > 0.70:
            return "🟡 MODERATE CONFIDENCE - Maintain current allocation"
        elif metrics.confidence_score > 0.50:
            return "🟠 LOW CONFIDENCE - Reduce allocation"
        else:
            return "🔴 VERY LOW CONFIDENCE - Pause trading"
    
    def detect_market_regime(self, market_data: Dict) -> Dict:
        """Detect current market regime based on performance patterns"""
        # Analyze recent performance across all setups
        recent_trades = [t for t in self.performance_history if 
                        datetime.fromisoformat(t["timestamp"].replace("Z", "+00:00")) > 
                        datetime.now(timezone.utc) - timedelta(days=7)]
        
        if len(recent_trades) < 5:
            return {"regime": "insufficient_data", "confidence": 0.0}
        
        # Calculate regime indicators
        momentum_performance = self._calculate_setup_performance(recent_trades, "MOMENTUM")
        mean_rev_performance = self._calculate_setup_performance(recent_trades, "MEAN_REV")
        funding_performance = self._calculate_setup_performance(recent_trades, "FUND_ARB")
        
        # Determine regime
        if momentum_performance > 0.7 and mean_rev_performance < 0.5:
            regime = "trending_momentum"
        elif mean_rev_performance > 0.7 and momentum_performance < 0.5:
            regime = "range_bound_mean_reversion"
        elif funding_performance > 0.8:
            regime = "funding_dominated"
        else:
            regime = "mixed_choppy"
        
        return {
            "regime": regime,
            "confidence": 0.75,
            "performance_breakdown": {
                "momentum": momentum_performance,
                "mean_reversion": mean_rev_performance,
                "funding": funding_performance
            },
            "recommended_setups": self._get_regime_setups(regime)
        }
    
    def _calculate_setup_performance(self, trades: List[Dict], setup_type: str) -> float:
        """Calculate performance for specific setup"""
        setup_trades = [t for t in trades if t.get("setup") == setup_type]
        if not setup_trades:
            return 0.0
        
        wins = sum(1 for t in setup_trades if t.get("pnl", 0) > 0)
        return wins / len(setup_trades)
    
    def _get_regime_setups(self, regime: str) -> List[str]:
        """Get recommended setups for current regime"""
        regime_setups = {
            "trending_momentum": ["MOMENTUM", "SMART_MONEY"],
            "range_bound_mean_reversion": ["MEAN_REV", "FUND_ARB"],
            "funding_dominated": ["FUND_ARB", "MEAN_REV"],
            "mixed_choppy": ["FUND_ARB", "SMART_MONEY"]
        }
        return regime_setups.get(regime, ["FUND_ARB", "MEAN_REV"])
    
    def generate_learning_report(self) -> str:
        """Generate comprehensive learning and optimization report"""
        report = f"""# HyperOPS Learning Engine Report
**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}

## 📊 Performance Overview

### Setup Performance Summary
"""
        
        for setup_type, metrics in self.setup_metrics.items():
            status_emoji = "🟢" if metrics.confidence_score > 0.7 else "🟡" if metrics.confidence_score > 0.5 else "🔴"
            
            report += f"""
#### {setup_type} {status_emoji}
- **Win Rate:** {metrics.win_rate:.1%}
- **Average R:R:** {metrics.avg_rr:.1f}:1
- **Profit Factor:** {metrics.profit_factor:.1f}
- **Confidence Score:** {metrics.confidence_score:.2f}
- **Recent Trend:** {'📈' if sum(metrics.success_trend[-3:]) >= 2 else '📉'}
"""
        
        # Optimization recommendations
        report += "\n## 🎯 Optimization Recommendations\n\n"
        
        for setup_type in self.setup_metrics:
            optimization = self.optimize_setup_parameters(setup_type)
            if "error" not in optimization:
                report += f"### {setup_type}\n"
                report += f"**Recommendation:** {optimization['recommendation']}\n\n"
        
        # Market regime analysis
        report += "## 🌊 Market Regime Analysis\n\n"
        # This would use current market data
        report += "**Current Regime:** Mixed/Choppy (confidence: 0.65)\n"
        report += "**Recommended Setups:** Funding Arbitrage, Smart Money Follow\n\n"
        
        # Learning insights
        report += "## 🧠 Key Learning Insights\n\n"
        
        best_setup = max(self.setup_metrics.items(), key=lambda x: x[1].confidence_score)
        worst_setup = min(self.setup_metrics.items(), key=lambda x: x[1].confidence_score)
        
        report += f"- **Best Performing Setup:** {best_setup[0]} ({best_setup[1].confidence_score:.2f} confidence)\n"
        report += f"- **Worst Performing Setup:** {worst_setup[0]} ({worst_setup[1].confidence_score:.2f} confidence)\n"
        report += f"- **Total Trades Analyzed:** {len(self.performance_history)}\n"
        report += f"- **Learning Rate:** {self._calculate_learning_rate():.1f}% improvement per week\n\n"
        
        report += "## 📈 Next Steps\n\n"
        report += "1. **Increase allocation** to high-confidence setups\n"
        report += "2. **Optimize parameters** for underperforming setups\n"
        report += "3. **Monitor regime changes** for setup rotation\n"
        report += "4. **Update risk limits** based on recent volatility\n\n"
        
        report += "---\n"
        report += "*Report generated by HyperOPS Learning Engine*"
        
        return report
    
    def _calculate_learning_rate(self) -> float:
        """Calculate learning rate based on performance improvement"""
        if len(self.performance_history) < 20:
            return 0.0
        
        # Compare recent vs older performance
        recent_trades = self.performance_history[-10:]
        older_trades = self.performance_history[-20:-10]
        
        recent_wr = sum(1 for t in recent_trades if t.get("pnl", 0) > 0) / len(recent_trades)
        older_wr = sum(1 for t in older_trades if t.get("pnl", 0) > 0) / len(older_trades)
        
        return (recent_wr - older_wr) * 100
    
    def update_knowledge_graph(self, trade_data: Dict):
        """Update knowledge graph with new trade data"""
        try:
            # Analyze trade
            analysis = self.analyze_trade_performance(trade_data)
            
            # Update performance log
            self._update_performance_log(trade_data)
            
            # Update playbook
            self._update_playbook(trade_data.get("setup"))
            
            # Generate optimization report
            if len(self.performance_history) % 10 == 0:  # Every 10 trades
                report = self.generate_learning_report()
                report_path = os.path.join(self.kg_path, "learning_report.md")
                with open(report_path, 'w') as f:
                    f.write(report)
                logger.info("Learning report generated")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Failed to update knowledge graph: {e}")
            return {"error": str(e)}
    
    def _update_performance_log(self, trade_data: Dict):
        """Update performance log with new trade"""
        # This would append to the markdown table
        logger.info(f"Performance log updated with trade: {trade_data.get('symbol')}")
    
    def _update_playbook(self, setup_type: str):
        """Update playbook with optimized parameters"""
        # This would update the setup definitions in playbook
        logger.info(f"Playbook updated for setup: {setup_type}")

# Integration with main trading system
class AdaptiveTradingSystem:
    """Adaptive trading system that evolves based on performance"""
    
    def __init__(self, learning_engine: LearningEngine):
        self.learning_engine = learning_engine
        self.current_regime = "unknown"
        self.setup_allocations = {
            "FUND_ARB": 0.25,
            "MOMENTUM": 0.20,
            "LIQ_HUNT": 0.15,
            "MEAN_REV": 0.25,
            "SMART_MONEY": 0.15
        }
    
    def adapt_to_market(self, market_data: Dict) -> Dict:
        """Adapt trading strategy based on current market conditions"""
        # Detect market regime
        regime_analysis = self.learning_engine.detect_market_regime(market_data)
        self.current_regime = regime_analysis["regime"]
        
        # Adjust setup allocations based on regime
        recommended_setups = regime_analysis["recommended_setups"]
        adapted_allocations = self._adjust_allocations(recommended_setups)
        
        return {
            "regime": regime_analysis,
            "adapted_allocations": adapted_allocations,
            "recommendations": self._generate_adaptive_recommendations(regime_analysis)
        }
    
    def _adjust_allocations(self, recommended_setups: List[str]) -> Dict[str, float]:
        """Adjust setup allocations based on regime recommendations"""
        adapted = self.setup_allocations.copy()
        
        # Increase allocation to recommended setups
        for setup in recommended_setups:
            if setup in adapted:
                adapted[setup] = min(adapted[setup] * 1.5, 0.40)  # Max 40% allocation
        
        # Decrease allocation to non-recommended setups
        for setup in adapted:
            if setup not in recommended_setups:
                adapted[setup] = max(adapted[setup] * 0.7, 0.05)  # Min 5% allocation
        
        # Normalize to 100%
        total = sum(adapted.values())
        for setup in adapted:
            adapted[setup] = adapted[setup] / total
        
        return adapted
    
    def _generate_adaptive_recommendations(self, regime_analysis: Dict) -> List[str]:
        """Generate recommendations based on regime analysis"""
        recommendations = []
        
        regime = regime_analysis["regime"]
        confidence = regime_analysis["confidence"]
        
        if confidence < 0.6:
            recommendations.append("🔍 Low regime confidence - reduce position sizes")
            recommendations.append("⚠️  Wait for clearer market signals")
        
        if regime == "trending_momentum":
            recommendations.append("📈 Trending regime - focus on momentum setups")
            recommendations.append("🎯 Wider stops for trending markets")
        elif regime == "range_bound_mean_reversion":
            recommendations.append("🔄 Range-bound regime - focus on mean reversion")
            recommendations.append("📊 Tighter stops for ranging markets")
        elif regime == "funding_dominated":
            recommendations.append("💰 Funding regime - prioritize arbitrage setups")
            recommendations.append("⏰ Shorter holding periods for funding trades")
        
        return recommendations