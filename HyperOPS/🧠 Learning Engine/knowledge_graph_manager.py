"""
HyperOPS Knowledge Graph Manager
Centralized management of all knowledge graph data with intelligent updates
"""

import os
import json
import re
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


class KnowledgeGraphManager:
    """Manages all knowledge graph components with intelligent updates"""

    def __init__(self, kg_path: str = "knowledge_graph"):
        self.kg_path = kg_path
        self.files = {
            "performance_log": "performance_log.md",
            "playbook": "playbook.md",
            "tokens": "tokens.md",
            "narratives": "narratives.md",
            "smart_money": "smart_money.md",
        }

        # Ensure knowledge graph directory exists
        os.makedirs(self.kg_path, exist_ok=True)

        # Load existing data
        self.data = self._load_all_data()

    def _load_all_data(self) -> Dict[str, Any]:
        """Load all knowledge graph data"""
        data = {}

        for key, filename in self.files.items():
            filepath = os.path.join(self.kg_path, filename)
            if os.path.exists(filepath):
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data[key] = f.read()
                except Exception as e:
                    logger.error(f"Failed to load {filename}: {e}")
                    data[key] = ""
            else:
                data[key] = ""

        return data

    def update_performance_log(self, trade_data: Dict) -> bool:
        """Update performance log with new trade"""
        try:
            # Parse existing trades
            existing_trades = self._parse_performance_trades()

            # Add new trade
            new_trade = {
                "date": trade_data.get(
                    "date", datetime.now(timezone.utc).strftime("%Y-%m-%d")
                ),
                "symbol": trade_data.get("symbol", ""),
                "setup": trade_data.get("setup", ""),
                "entry": trade_data.get("entry", 0),
                "stop": trade_data.get("stop", 0),
                "tp1": trade_data.get("tp1", 0),
                "tp2": trade_data.get("tp2", 0),
                "size": trade_data.get("size", 0),
                "risk": trade_data.get("risk", 0),
                "pnl": trade_data.get("pnl", 0),
                "rr": trade_data.get("rr", 0),
                "status": "🟢 Win" if trade_data.get("pnl", 0) > 0 else "🔴 Loss",
                "notes": trade_data.get("notes", ""),
            }

            existing_trades.append(new_trade)

            # Keep only last 100 trades in table
            if len(existing_trades) > 100:
                existing_trades = existing_trades[-100:]

            # Generate updated performance log
            updated_log = self._generate_performance_log(existing_trades)

            # Write back to file
            filepath = os.path.join(self.kg_path, self.files["performance_log"])
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(updated_log)

            # Update in-memory data
            self.data["performance_log"] = updated_log

            logger.info(
                f"Performance log updated with trade: {new_trade['symbol']} {new_trade['setup']}"
            )
            return True

        except Exception as e:
            logger.error(f"Failed to update performance log: {e}")
            return False

    def _parse_performance_trades(self) -> List[Dict]:
        """Parse existing trades from performance log"""
        trades = []

        if not self.data.get("performance_log"):
            return trades

        # Find the table in markdown
        table_pattern = r"\|.*\|[\s\S]*?\n\|.*\|"
        matches = re.findall(table_pattern, self.data["performance_log"])

        if not matches:
            return trades

        # Parse table rows
        lines = matches[0].strip().split("\n")
        for line in lines:
            if line.startswith("|") and not line.startswith("|---"):
                parts = [p.strip() for p in line.split("|")[1:-1]]  # Remove empty ends

                if len(parts) >= 11:
                    try:
                        trade = {
                            "date": parts[0],
                            "symbol": parts[1],
                            "setup": parts[2],
                            "entry": float(parts[3].replace(",", "")),
                            "stop": float(parts[4].replace(",", "")),
                            "tp1": float(parts[5].replace(",", "")),
                            "tp2": float(parts[6].replace(",", "")),
                            "size": float(parts[7]),
                            "risk": float(parts[8]),
                            "pnl": float(parts[9]),
                            "rr": float(parts[10]),
                            "status": parts[11] if len(parts) > 11 else "",
                            "notes": parts[12] if len(parts) > 12 else "",
                        }
                        trades.append(trade)
                    except (ValueError, IndexError) as e:
                        logger.warning(f"Failed to parse trade row: {e}")

        return trades

    def _generate_performance_log(self, trades: List[Dict]) -> str:
        """Generate complete performance log markdown"""
        # Calculate metrics
        total_trades = len(trades)
        wins = sum(1 for t in trades if t.get("pnl", 0) > 0)
        losses = total_trades - wins
        win_rate = wins / total_trades if total_trades > 0 else 0

        total_pnl = sum(t.get("pnl", 0) for t in trades)

        # Setup performance
        setup_stats = {}
        for trade in trades:
            setup = trade.get("setup", "UNKNOWN")
            if setup not in setup_stats:
                setup_stats[setup] = {"wins": 0, "losses": 0, "total_rr": 0, "count": 0}

            setup_stats[setup]["count"] += 1
            setup_stats[setup]["total_rr"] += trade.get("rr", 0)

            if trade.get("pnl", 0) > 0:
                setup_stats[setup]["wins"] += 1
            else:
                setup_stats[setup]["losses"] += 1

        # Generate markdown
        log_content = f"""# Performance Log & Trading Journal

**Objective:** Track every Hyperliquid trade to measure accuracy, optimize setups, and maintain discipline.

## 📊 Trading Performance

| Date | Symbol | Setup | Entry | Stop | TP1 | TP2 | Size | Risk ($) | PnL ($) | R:R | Status | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""

        # Add trades (most recent first)
        for trade in reversed(trades[-20:]):  # Show last 20 in table
            log_content += f"| {trade['date']} | {trade['symbol']} | {trade['setup']} | {trade['entry']:,.0f} | {trade['stop']:,.0f} | {trade['tp1']:,.0f} | {trade['tp2']:,.0f} | {trade['size']} | ${trade['risk']:.0f} | ${trade['pnl']:+.0f} | {trade['rr']:.1f}:1 | {trade['status']} | {trade['notes']} |\n"

        # Add metrics section
        log_content += f"""
## 📈 Performance Metrics

**Daily Stats:**
- **Today's PnL:** ${total_pnl:+.0f} ({total_pnl:.0%})
- **Win Rate:** {win_rate:.1%} ({wins}/{total_trades} trades)
- **Average R:R:** {sum(t.get("rr", 0) for t in trades) / total_trades:.1f}:1
- **Total Trades:** {total_trades}

## 🎯 Setup Performance

| Setup | Trades | Wins | Win Rate | Avg R:R | Profit Factor |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""

        for setup, stats in setup_stats.items():
            setup_wr = stats["wins"] / stats["count"] if stats["count"] > 0 else 0
            avg_rr = stats["total_rr"] / stats["count"] if stats["count"] > 0 else 0
            profit_factor = (
                (stats["wins"] * avg_rr) / abs(stats["losses"])
                if stats["losses"] > 0
                else avg_rr
            )

            log_content += f"| **{setup}** | {stats['count']} | {stats['wins']} | {setup_wr:.1%} | {avg_rr:.1f}:1 | {profit_factor:.1f} |\n"

        log_content += (
            """
## 🧠 Learning Journal

**Key Insights:**
- Trading performance tracked and analyzed continuously
- Setup optimization based on historical results
- Risk management compliance monitored

**Process Improvements:**
- Multi-source verification for all setups
- Strict risk management adherence
- Continuous learning from trade outcomes

---
*Last updated: """
            + datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            + "*"
        )

        return log_content

    def update_playbook(self, setup_updates: Dict) -> bool:
        """Update playbook with optimized setup parameters"""
        try:
            # Parse existing playbook
            existing_content = self.data.get("playbook", "")

            # Update setup metrics
            updated_content = self._update_setup_metrics(
                existing_content, setup_updates
            )

            # Write back to file
            filepath = os.path.join(self.kg_path, self.files["playbook"])
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(updated_content)

            self.data["playbook"] = updated_content
            logger.info("Playbook updated with optimized parameters")
            return True

        except Exception as e:
            logger.error(f"Failed to update playbook: {e}")
            return False

    def _update_setup_metrics(self, content: str, updates: Dict) -> str:
        """Update specific setup metrics in playbook"""
        for setup_type, update_data in updates.items():
            # Find setup section in content
            setup_pattern = rf"### \d+\. {re.escape(setup_type)}.*?\n(?=###|\Z)"
            setup_match = re.search(setup_pattern, content, re.DOTALL)

            if setup_match:
                setup_section = setup_match.group(0)

                # Update success rate
                if "win_rate" in update_data:
                    wr_pattern = r"\*   \*\*Success Rate:\*\* \d+%"
                    new_wr = f"*   **Success Rate:** {update_data['win_rate']:.0%}"
                    setup_section = re.sub(wr_pattern, new_wr, setup_section)

                # Update status
                if "status" in update_data:
                    status_pattern = r"\*   \*\*Status:\*\* [🟢🟡🔴]+"
                    status_emoji = (
                        "🟢"
                        if update_data["status"] == "active"
                        else "🟡"
                        if update_data["status"] == "experimental"
                        else "🔴"
                    )
                    new_status = f"*   **Status:** {status_emoji}"
                    setup_section = re.sub(status_pattern, new_status, setup_section)

                # Replace in content
                content = content.replace(setup_match.group(0), setup_section)

        return content

    def update_tokens(self, token_updates: Dict) -> bool:
        """Update tokens knowledge with current market data"""
        try:
            # Parse existing tokens
            existing_content = self.data.get("tokens", "")

            # Update token table
            updated_content = self._update_token_table(existing_content, token_updates)

            # Write back to file
            filepath = os.path.join(self.kg_path, self.files["tokens"])
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(updated_content)

            self.data["tokens"] = updated_content
            logger.info("Tokens knowledge updated with market data")
            return True

        except Exception as e:
            logger.error(f"Failed to update tokens: {e}")
            return False

    def _update_token_table(self, content: str, updates: Dict) -> str:
        """Update token table with current data"""
        # Find and update the token table
        table_pattern = r"\| Symbol \| Status \|.*?\n(?=##|\Z)"
        table_match = re.search(table_pattern, content, re.DOTALL)

        if not table_match:
            return content

        # Build updated table
        table_header = "| Symbol | Status | Setup Type | Entry Zone | Stop Loss | TP1 | TP2 | Thesis | Last Update |\n"
        table_separator = (
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
        )

        table_rows = []
        for symbol, data in updates.items():
            status_emoji = data.get("status", "🟡")
            setup_type = data.get("setup_type", "-")
            entry_zone = data.get("entry_zone", "-")
            stop_loss = data.get("stop_loss", "-")
            tp1 = data.get("tp1", "-")
            tp2 = data.get("tp2", "-")
            thesis = data.get("thesis", "")
            last_update = datetime.now(timezone.utc).strftime("%Y-%m-%d")

            row = f"| **{symbol}** | {status_emoji} | {setup_type} | {entry_zone} | {stop_loss} | {tp1} | {tp2} | {thesis} | {last_update} |"
            table_rows.append(row)

        new_table = table_header + table_separator + "\n".join(table_rows) + "\n"

        # Replace in content
        updated_content = content.replace(table_match.group(0), new_table)

        return updated_content

    def update_narratives(self, narrative_data: Dict) -> bool:
        """Update market narratives and regime tracking"""
        try:
            # Parse existing narratives
            existing_content = self.data.get("narratives", "")

            # Add new narrative entry
            updated_content = self._add_narrative_entry(
                existing_content, narrative_data
            )

            # Write back to file
            filepath = os.path.join(self.kg_path, self.files["narratives"])
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(updated_content)

            self.data["narratives"] = updated_content
            logger.info("Narratives updated with market regime data")
            return True

        except Exception as e:
            logger.error(f"Failed to update narratives: {e}")
            return False

    def _add_narrative_entry(self, content: str, data: Dict) -> str:
        """Add new narrative entry to existing content"""
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        regime = data.get("regime", "Unknown")
        catalysts = data.get("catalysts", [])
        sentiment = data.get("sentiment", "Neutral")

        new_entry = f"""
## {date}

### Market Regime
**Regime:** {regime}
**Sentiment:** {sentiment}
**Confidence:** {data.get("confidence", 0.5):.1%}

### Key Catalysts
"""

        for catalyst in catalysts:
            new_entry += f"- **{catalyst.get('type', 'Unknown')}:** {catalyst.get('description', '')}\n"

        new_entry += f"""
### Market Themes
- {data.get("theme1", "Monitoring market developments")}
- {data.get("theme2", "Tracking liquidity flows")}
- {data.get("theme3", "Analyzing smart money positioning")}

---
"""

        # Insert before the last ## heading or at end
        if "## " in content:
            last_heading = content.rfind("## ")
            updated_content = (
                content[:last_heading] + new_entry + "\n" + content[last_heading:]
            )
        else:
            updated_content = content + new_entry

        return updated_content

    def update_smart_money(self, smart_money_data: Dict) -> bool:
        """Update smart money intelligence"""
        try:
            # Parse existing smart money data
            existing_content = self.data.get("smart_money", "")

            # Add new smart money entries
            updated_content = self._add_smart_money_entries(
                existing_content, smart_money_data
            )

            # Write back to file
            filepath = os.path.join(self.kg_path, self.files["smart_money"])
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(updated_content)

            self.data["smart_money"] = updated_content
            logger.info("Smart money intelligence updated")
            return True

        except Exception as e:
            logger.error(f"Failed to update smart money: {e}")
            return False

    def _add_smart_money_entries(self, content: str, data: Dict) -> str:
        """Add new smart money entries"""
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        new_entry = f"""
## {date}

### Elite Trader Activity
"""

        for trader in data.get("elite_traders", []):
            new_entry += f"""
#### {trader.get("name", "Unknown")}
- **Position:** {trader.get("position", "Unknown")}
- **Size:** ${trader.get("size", 0):,.0f}
- **Confidence:** {trader.get("confidence", "Unknown")}
- **Notes:** {trader.get("notes", "")}
"""

        new_entry += """
### Whale Wallet Flows
"""

        for wallet in data.get("wallet_flows", []):
            new_entry += f"- **{wallet.get('address', 'Unknown')[:8]}...:** {wallet.get('action', 'Unknown')} ${wallet.get('amount', 0):,.0f} of {wallet.get('token', 'Unknown')}\n"

        new_entry += "\n---\n"

        # Insert before the last ## heading or at end
        if "## " in content:
            last_heading = content.rfind("## ")
            updated_content = (
                content[:last_heading] + new_entry + "\n" + content[last_heading:]
            )
        else:
            updated_content = content + new_entry

        return updated_content

    def get_knowledge_summary(self) -> Dict:
        """Get summary of all knowledge graph data"""
        summary = {
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "files": {},
            "key_insights": [],
        }

        # Analyze each knowledge graph file
        for key, content in self.data.items():
            if content:
                summary["files"][key] = {
                    "size": len(content),
                    "last_modified": os.path.getmtime(
                        os.path.join(self.kg_path, self.files[key])
                    )
                    if os.path.exists(os.path.join(self.kg_path, self.files[key]))
                    else None,
                }

        # Extract key insights
        if self.data.get("performance_log"):
            trades = self._parse_performance_trades()
            if trades:
                wins = sum(1 for t in trades if t.get("pnl", 0) > 0)
                summary["key_insights"].append(
                    f"Total trades: {len(trades)}, Win rate: {wins / len(trades):.1%}"
                )

        return summary

    def backup_knowledge_graph(self, backup_path: str = None) -> bool:
        """Create backup of entire knowledge graph"""
        try:
            if not backup_path:
                timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
                backup_path = f"backups/knowledge_graph_{timestamp}"

            os.makedirs(backup_path, exist_ok=True)

            # Copy all knowledge graph files
            for key, filename in self.files.items():
                src = os.path.join(self.kg_path, filename)
                dst = os.path.join(backup_path, filename)

                if os.path.exists(src):
                    with open(src, "r", encoding="utf-8") as f:
                        content = f.read()

                    with open(dst, "w", encoding="utf-8") as f:
                        f.write(content)

            logger.info(f"Knowledge graph backed up to: {backup_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to backup knowledge graph: {e}")
            return False
