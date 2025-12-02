# HyperOPS Python Trading Integration

## Installation

Install the required Python packages:

```bash
pip install hyperliquid-python-sdk eth-account
```

## Quick Setup

1. **Create Configuration:**
```bash
python hyperops_cli.py setup
```

2. **Edit Configuration:**
Edit `config/trading_config.json.example` with your credentials:
```json
{
  "account_address": "0xYOUR_WALLET_ADDRESS",
  "secret_key": "your_private_key_here",
  "testnet": true,
  "max_risk_percent": 0.20,
  "leverage_min": 9,
  "leverage_max": 12,
  "max_positions": 2,
  "hard_exit_time": "22:00"
}
```

3. **Rename Config:**
```bash
mv config/trading_config.json.example config/trading_config.json
```

## Usage

### Run Daily Trading Session
```bash
python hyperops_cli.py session
```

### Check Trading Status
```bash
python hyperops_cli.py status
```

### Emergency Close All Positions
```bash
python hyperops_cli.py emergency-close
```

## Core Components

### 1. Trading Module (`trading_module.py`)
- **HyperliquidTrader**: Main trading interface
- **TradingConfig**: Configuration management
- **OrderSpec**: Order specification
- **Position**: Position tracking

### 2. Strategy Module (`strategy_module.py`)
- **HyperOPSStrategies**: Strategy implementation
- **TradingSetup**: Trading setup definition
- **MarketEvidence**: Market evidence analysis

### 3. Daily Session (`daily_trading_session.py`)
- **DailyTradingSession**: Main workflow orchestrator
- Implements the 5-step HyperOPS protocol:
  1. Market Preparation
  2. Market Scan & Detection
  3. Deep Dive Analysis
  4. Trade Execution
  5. Daily Brief Generation

### 4. CLI Interface (`hyperops_cli.py`)
- Command-line interface for all operations
- Session management, status checking, emergency controls

## Trading Strategies

### 1. Funding Arbitrage
- **Signal**: Extreme funding rates (>0.5%)
- **Entry**: Limit orders at VWAP/LVN
- **Exit**: Funding normalization + 1.5x risk

### 2. Momentum Catalysts
- **Signal**: News, upgrades, unlocks
- **Entry**: Breakout entries
- **Exit**: Catalyst completion or 2.5x risk

### 3. Mean Reversion
- **Signal**: Extreme basis deviations
- **Entry**: Fade extreme moves
- **Exit**: Return to VWAP + 1.5x risk

### 4. Smart Money Follow
- **Signal**: Verified smart money flows
- **Entry**: Passive at their levels
- **Exit**: Their exit signals + 2x risk

## Risk Management

- **Max Risk**: 20% per trade
- **Leverage**: 9-12x
- **Position Limit**: 2 simultaneous positions
- **Hard Exit**: 22:00 AEST daily
- **Entry Type**: Limit orders only (passive)

### ⚠️ CRITICAL: Stop Loss Order Types

**NEVER use LIMIT orders for stop losses** - they will execute immediately!

**Problem:**
- Short position @ $2980, want stop @ $3050
- Using `order_type="limit"`, `side="buy"`, `price=3050`
- Limit buy @ $3050 when market is $2980 = "buy at $3050 or BETTER (lower)"
- **Result:** Order executes IMMEDIATELY at market price instead of waiting for $3050

**Solution:**
- Use STOP or STOP_LIMIT order types that only trigger when price reaches the specified level
- For Extended SDK: Check documentation for proper stop order implementation
- Stop losses for SHORTS: Use stop-buy that triggers when price goes UP
- Stop losses for LONGS: Use stop-sell that triggers when price goes DOWN

**Implementation Note:**
Current `trading_module.py` does not implement stop orders correctly. Before placing protective stops, verify the SDK supports stop order types and update the implementation accordingly.

## Output Files

### Daily Trading Briefs
- Location: `research_logs/YYYY-MM-DD/daily_trading_brief.md`
- Contains: Market analysis, top setups, execution results

### Session Data
- Location: `research_logs/YYYY-MM-DD/session_data.json`
- Contains: Complete session data for analysis

### Knowledge Graph Updates
- Updates: `knowledge_graph/performance_log.md`
- Tracks: Performance, setups, market regimes

## API Integration Points

### Real Data Sources (To Be Implemented)
- **Hyperliquid API**: Primary market data
- **Dune Analytics**: On-chain flows
- **Dextrabot**: Whale trades
- **ApexLiquid**: Top traders
- **X/Twitter**: Catalyst detection

### Current Implementation
- Sample data for catalysts and smart money
- Real Hyperliquid API integration
- Full order execution and position management

## Security Notes

- Keep private keys secure
- Use testnet for initial testing
- Implement proper API key rotation
- Monitor for unusual activity

## Next Steps

1. **Real Data Integration**: Connect to live catalyst and whale intel sources
2. **Enhanced Risk**: Add more sophisticated risk controls
3. **Backtesting**: Historical strategy performance analysis
4. **Dashboard**: Real-time trading dashboard
5. **Alerts**: Telegram/Discord notifications

## Troubleshooting

### Common Issues
- **Address Mismatch**: Ensure config address matches derived address
- **Insufficient Margin**: Check account has sufficient USDC
- **API Limits**: Monitor rate limits on API calls
- **Network Issues**: Ensure stable internet connection

### Debug Mode
Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Support

For issues or questions:
1. Check logs for error details
2. Verify configuration settings
3. Test with small amounts first
4. Use testnet for initial deployment