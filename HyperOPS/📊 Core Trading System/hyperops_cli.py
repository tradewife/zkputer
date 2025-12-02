"""
HyperOPS Trading CLI
Command-line interface for the HyperOPS trading system
"""

import argparse
import sys
import json
from datetime import datetime

from daily_trading_session import DailyTradingSession
from trading_module import create_sample_config


def run_session(args):
    """Run daily trading session"""
    try:
        config_path = args.config if args.config else "config/trading_config.json"
        session = DailyTradingSession(config_path)
        result = session.run_full_session()

        if result["status"] == "success":
            print(f"\n✅ Session completed successfully!")
            print(f"📄 Daily brief: {result['brief_path']}")
            return 0
        else:
            print(f"\n❌ Session failed: {result['error']}")
            return 1

    except Exception as e:
        print(f"❌ Error running session: {e}")
        return 1


def check_status(args):
    """Check current trading status"""
    try:
        config_path = args.config if args.config else "config/trading_config.json"
        session = DailyTradingSession(config_path)

        # Get account state
        account_state = session.trader.get_account_state()
        positions = session.trader.get_positions()
        open_orders = session.trader.get_open_orders()

        equity = float(account_state.get("marginSummary", {}).get("accountValue", 0))
        total_pnl = sum(pos.unrealized_pnl for pos in positions)

        print(f"\n📊 HyperOPS Trading Status")
        print(f"========================")
        print(f"Account Equity: ${equity:.2f}")
        print(f"Total PnL: ${total_pnl:.2f}")
        print(f"Open Positions: {len(positions)}")
        print(f"Open Orders: {len(open_orders)}")

        if positions:
            print(f"\n📈 Positions:")
            for pos in positions:
                print(
                    f"  {pos.symbol}: {pos.side} {pos.size:.4f} @ {pos.entry_price:.4f} | PnL: ${pos.unrealized_pnl:.2f}"
                )

        if open_orders:
            print(f"\n📋 Open Orders:")
            for order in open_orders[:5]:  # Show first 5
                print(
                    f"  {order['coin']}: {order['side']} {order['sz']} @ {order.get('limitPx', 'MARKET')}"
                )

        return 0

    except Exception as e:
        print(f"❌ Error checking status: {e}")
        return 1


def emergency_close(args):
    """Emergency close all positions"""
    try:
        config_path = args.config if args.config else "config/trading_config.json"
        session = DailyTradingSession(config_path)

        confirm = input("⚠️  This will close ALL positions. Type 'CLOSE' to confirm: ")
        if confirm != "CLOSE":
            print("❌ Emergency close cancelled")
            return 1

        results = session.trader.close_all_positions()

        print(f"\n🚨 Emergency Close Results:")
        for i, result in enumerate(results, 1):
            if result.get("status") == "ok":
                print(f"✅ Position {i}: Closed successfully")
            else:
                print(
                    f"❌ Position {i}: Failed - {result.get('error', 'Unknown error')}"
                )

        return 0

    except Exception as e:
        print(f"❌ Error in emergency close: {e}")
        return 1


def execute_trades(args):
    """Execute prepared trades from daily session"""
    try:
        from trade_executor import TradeExecutor, execute_user_command

        config_path = args.config if args.config else "config/trading_config.json"
        session = DailyTradingSession(config_path)

        # Run market scan to get setups
        scan_results, ranked_setups = session.run_market_scan()

        if not ranked_setups:
            print("ℹ️  No trading setups found")
            return 0

        # Prepare top 2-3 setups
        executor = TradeExecutor(session.trader)
        top_setups = ranked_setups[:3]
        prepared_trades = executor.prepare_trades(top_setups)

        print(executor.get_pending_trades_summary())

        # Interactive command loop
        while True:
            command = input("\nEnter command (or 'help'): ").strip()

            if command.lower() in ["quit", "exit", "q"]:
                break
            elif command.lower() == "help":
                print("Available commands:")
                print("- 'Execute all' - Execute all pending trades")
                print("- 'Execute trade [1-3]' - Execute specific trade")
                print("- 'Cancel' - Clear pending trades")
                print("- 'Status' - Show pending trades")
                print("- 'Quit' - Exit")
            else:
                result = execute_user_command(command, executor)
                print(result)

        return 0

    except Exception as e:
        print(f"❌ Error in trade execution: {e}")
        return 1

        results = session.trader.close_all_positions()

        print(f"\n🚨 Emergency Close Results:")
        for i, result in enumerate(results, 1):
            if result.get("status") == "ok":
                print(f"✅ Position {i}: Closed successfully")
            else:
                print(
                    f"❌ Position {i}: Failed - {result.get('error', 'Unknown error')}"
                )

        return 0

    except Exception as e:
        print(f"❌ Error in emergency close: {e}")
        return 1


def setup_config(args):
    """Setup trading configuration"""
    try:
        create_sample_config()
        print(f"\n⚙️  Configuration setup complete!")
        print(f"📝 Edit config/trading_config.json.example with your credentials")
        print(f"🔄 Rename to trading_config.json when ready")
        return 0

    except Exception as e:
        print(f"❌ Error setting up config: {e}")
        return 1


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="HyperOPS Trading CLI")
    parser.add_argument("--config", help="Path to trading config file")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Session command
    session_parser = subparsers.add_parser("session", help="Run daily trading session")
    session_parser.set_defaults(func=run_session)

    # Status command
    status_parser = subparsers.add_parser("status", help="Check trading status")
    status_parser.set_defaults(func=check_status)

    # Emergency close command
    close_parser = subparsers.add_parser(
        "emergency-close", help="Emergency close all positions"
    )
    close_parser.set_defaults(func=emergency_close)

    # Execute trades command
    exec_parser = subparsers.add_parser(
        "execute", help="Execute prepared trades from daily session"
    )
    exec_parser.set_defaults(func=execute_trades)

    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Setup trading configuration")
    setup_parser.set_defaults(func=setup_config)

    # Parse arguments
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Execute command
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
