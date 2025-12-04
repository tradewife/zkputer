"""
Example usage and testing for HyperOPS trading system
"""

import os
import json
from datetime import datetime, timezone

from trading_module import HyperliquidTrader, TradingConfig, OrderSpec
from strategy_module import (
    HyperOPSStrategies,
    create_sample_catalysts,
    create_sample_smart_money,
)
from daily_trading_session import DailyTradingSession


def test_configuration():
    """Test configuration loading and validation"""
    print("🧪 Testing Configuration...")

    try:
        # Create sample config if it doesn't exist
        if not os.path.exists("config/trading_config.json"):
            print("⚠️  No config found. Creating sample...")
            from trading_module import create_sample_config

            create_sample_config()
            print("📝 Please edit config/trading_config.json with your credentials")
            return False

        # Load and validate config
        config = TradingConfig.from_file("config/trading_config.json")
        print(f"✅ Config loaded for address: {config.account_address}")
        print(f"🔧 Testnet: {config.testnet}")
        print(f"💰 Max Risk: {config.max_risk_percent * 100}%")
        print(f"⚡ Leverage: {config.leverage_min}-{config.leverage_max}x")

        return True

    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False


def test_api_connection():
    """Test API connection and basic data retrieval"""
    print("\n🧪 Testing API Connection...")

    try:
        config = TradingConfig.from_file("config/trading_config.json")
        trader = HyperliquidTrader(config)

        # Test account state
        account_state = trader.get_account_state()
        if account_state:
            equity = float(
                account_state.get("marginSummary", {}).get("accountValue", 0)
            )
            print(f"✅ API connection successful")
            print(f"💳 Account Equity: ${equity:.2f}")
        else:
            print("⚠️  Could not fetch account state")

        # Test market data
        market_data = trader.get_market_data(["BTC", "ETH"])
        print(f"📊 Market data retrieved for {len(market_data)} symbols")

        for symbol, data in market_data.items():
            price = data.get("mark_price", 0)
            funding = data.get("funding", {}).get("fundingRate", 0)
            print(f"  {symbol}: ${price:.2f} | Funding: {funding:.4f}")

        return True

    except Exception as e:
        print(f"❌ API connection test failed: {e}")
        return False


def test_strategy_scanning():
    """Test strategy scanning with sample data"""
    print("\n🧪 Testing Strategy Scanning...")

    try:
        config = TradingConfig.from_file("config/trading_config.json")
        trader = HyperliquidTrader(config)
        strategies = HyperOPSStrategies(trader)

        # Get market data
        market_data = trader.get_market_data(["BTC", "ETH", "SOL"])

        # Test funding arbitrage scan
        funding_setups = strategies.scan_funding_arbitrage(market_data)
        print(f"💰 Funding arbitrage setups: {len(funding_setups)}")

        # Test momentum catalyst scan
        catalysts = create_sample_catalysts()
        momentum_setups = strategies.scan_momentum_catalysts(market_data, catalysts)
        print(f"🚀 Momentum catalyst setups: {len(momentum_setups)}")

        # Test mean reversion scan
        mean_reversion_setups = strategies.scan_mean_reversion(market_data)
        print(f"🔄 Mean reversion setups: {len(mean_reversion_setups)}")

        # Test smart money follow scan
        smart_money = create_sample_smart_money()
        smart_money_setups = strategies.scan_smart_money_follow(
            market_data, smart_money
        )
        print(f"🐋 Smart money setups: {len(smart_money_setups)}")

        # Show top setup if any found
        all_setups = (
            funding_setups
            + momentum_setups
            + mean_reversion_setups
            + smart_money_setups
        )
        if all_setups:
            ranked = strategies.rank_setups(all_setups)
            top = ranked[0]
            print(f"\n🎯 Top Setup:")
            print(f"  Symbol: {top.symbol}")
            print(f"  Type: {top.setup_type}")
            print(f"  Side: {top.side}")
            print(f"  Thesis: {top.thesis}")
            print(f"  Confidence: {top.confidence:.2f}")
            print(f"  Entry: {top.entry_zone[0]:.4f} - {top.entry_zone[1]:.4f}")
            print(f"  Stop: {top.stop_loss:.4f}")
            print(f"  TP1: {top.take_profit_1:.4f}")
            print(f"  TP2: {top.take_profit_2:.4f}")
        else:
            print("ℹ️  No setups found in current market conditions")

        return True

    except Exception as e:
        print(f"❌ Strategy scanning test failed: {e}")
        return False


def test_paper_trading():
    """Test paper trading (without real orders)"""
    print("\n🧪 Testing Paper Trading...")

    try:
        config = TradingConfig.from_file("config/trading_config.json")

        # Force testnet mode for safety
        config.testnet = True

        trader = HyperliquidTrader(config)
        strategies = HyperOPSStrategies(trader)

        # Get market data and find setups
        market_data = trader.get_market_data(["BTC", "ETH"])
        catalysts = create_sample_catalysts()
        smart_money = create_sample_smart_money()

        all_setups = []
        all_setups.extend(strategies.scan_funding_arbitrage(market_data))
        all_setups.extend(strategies.scan_momentum_catalysts(market_data, catalysts))
        all_setups.extend(strategies.scan_mean_reversion(market_data))
        all_setups.extend(strategies.scan_smart_money_follow(market_data, smart_money))

        if not all_setups:
            print("ℹ️  No setups found for paper trading test")
            return True

        # Test position sizing
        ranked_setups = strategies.rank_setups(all_setups)
        top_setup = ranked_setups[0]

        entry_price = sum(top_setup.entry_zone) / 2
        position_size = trader.calculate_position_size(
            top_setup.symbol, entry_price, top_setup.stop_loss
        )

        print(f"📏 Position sizing test:")
        print(f"  Symbol: {top_setup.symbol}")
        print(f"  Entry Price: ${entry_price:.2f}")
        print(f"  Stop Loss: ${top_setup.stop_loss:.2f}")
        print(f"  Position Size: {position_size:.6f}")
        print(f"  Notional: ${position_size * entry_price:.2f}")
        print(
            f"  Risk Amount: ${abs(entry_price - top_setup.stop_loss) * position_size:.2f}"
        )

        # Test order creation (without placing)
        order = OrderSpec(
            symbol=top_setup.symbol,
            side=top_setup.side,
            order_type="limit",
            size=position_size,
            price=entry_price,
        )

        print(f"📋 Order created (not placed):")
        print(f"  Symbol: {order.symbol}")
        print(f"  Side: {order.side}")
        print(f"  Type: {order.order_type}")
        print(f"  Size: {order.size}")
        print(f"  Price: ${order.price:.2f}")

        print("✅ Paper trading test completed successfully")
        return True

    except Exception as e:
        print(f"❌ Paper trading test failed: {e}")
        return False


def test_daily_session():
    """Test daily trading session workflow"""
    print("\n🧪 Testing Daily Session Workflow...")

    try:
        # Create session
        session = DailyTradingSession()

        # Test market preparation
        market_prep = session.run_market_preparation()
        print(f"✅ Market preparation completed")
        print(f"  Equity: ${market_prep['account_equity']:.2f}")
        print(f"  Positions: {market_prep['open_positions']}")

        # Test market scan
        scan_results, ranked_setups = session.run_market_scan()
        print(f"✅ Market scan completed")
        print(f"  Setups found: {len(ranked_setups)}")

        # Test deep dive
        deep_dive = session.run_deep_dive(ranked_setups)
        print(f"✅ Deep dive completed")
        print(f"  Analyzed: {len(deep_dive['analysis'])} setups")

        print("✅ Daily session workflow test completed")
        return True

    except Exception as e:
        print(f"❌ Daily session test failed: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("🚀 Starting HyperOPS Trading System Tests")
    print("=" * 50)

    tests = [
        ("Configuration", test_configuration),
        ("API Connection", test_api_connection),
        ("Strategy Scanning", test_strategy_scanning),
        ("Paper Trading", test_paper_trading),
        ("Daily Session", test_daily_session),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)

    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1

    print(f"\n🎯 Results: {passed}/{len(results)} tests passed")

    if passed == len(results):
        print("🎉 All tests passed! System is ready for trading.")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")

    return passed == len(results)


if __name__ == "__main__":
    # Check if config exists
    if not os.path.exists("config/trading_config.json"):
        print("⚠️  No trading configuration found.")
        print("📝 Please run 'python hyperops_cli.py setup' first")
        exit(1)

    # Run tests
    success = run_all_tests()
    exit(0 if success else 1)
