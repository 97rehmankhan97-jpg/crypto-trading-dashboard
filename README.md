# Professional Cryptocurrency Trading Dashboard

**Real-time BTC/USDT Trading Analysis with Binance API**

A professional-grade cryptocurrency trading dashboard that provides real-time market data, order book analysis, whale transaction detection, and volume profiling.

## Features

✅ **Real-time Order Book** - Top 10 bids and asks with live updates
✅ **Whale Detection** - Automatically detect and alert on large transactions (>0.5 BTC)
✅ **Inflow/Outflow Analysis** - Track buying vs selling pressure
✅ **Volume Profile** - Analyze volume distribution by price levels
✅ **Trade History** - Recent trades with timestamps and prices
✅ **Market Statistics** - 24-hour high/low, volume, price spreads
✅ **WebSocket Support** - Ultra-fast real-time updates (tick-by-tick)
✅ **Termux Compatible** - Run on Android phones with Termux

## Installation

### Requirements
- Python 3.8+
- Binance API Key & Secret (get from https://www.binance.com/en/account/api-management)
- Internet connection

### Setup

```bash
# Clone the repository
git clone https://github.com/97rehmankhan97-jpg/crypto-trading-dashboard.git
cd crypto-trading-dashboard

# Install dependencies
pip install -r requirements.txt
```

## Configuration

### Get Binance API Keys

1. Visit https://www.binance.com/en/account/api-management
2. Click "Create Api"
3. Choose "API Key"
4. Copy your API Key and Secret Key
5. Edit `main.py` and replace:
   ```python
   API_KEY = "your_binance_api_key_here"
   API_SECRET = "your_binance_api_secret_here"
   ```

**Security Note**: Never share your API keys! Use IP whitelist in Binance for added security.

## Usage

### Run REST API Version (Recommended for Beginners)
```bash
python main.py
```

This will:
- Fetch order book data
- Detect whale transactions
- Calculate volume profiles
- Analyze inflow/outflow
- Update every 5 seconds

### Run WebSocket Version (Real-time Tick Updates)
```bash
python websocket_version.py
```

This provides:
- Ultra-fast updates (every tick)
- Instant whale alerts
- Live order book changes
- Real-time trade stream

## Run on Termux (Android Phone)

```bash
# Install Termux from F-Droid or Google Play
# Open Termux and run:

pkg install python3 git
git clone https://github.com/97rehmankhan97-jpg/crypto-trading-dashboard.git
cd crypto-trading-dashboard
pip install -r requirements.txt
python main.py
```

## Dashboard Output

### Order Book Display
```
================================================================================
ORDER BOOK - BTC/USDT (Top 10)
================================================================================

ASKS (Sell Orders):
Price (USDT)         Quantity (BTC)       Total (USDT)        
44850.00             0.5234               23,421.00           
44851.00             1.2450               55,380.00           

Current Price: $44,820.50
Bid-Ask Spread: $2.50

BIDS (Buy Orders):
Price (USDT)         Quantity (BTC)       Total (USDT)        
44818.50             2.1234               94,892.00           
44817.00             0.8765               39,012.00           
```

### Whale Transactions
```
================================================================================
WHALE TRANSACTIONS (>0.5 BTC)
================================================================================
Time                      Price           Quantity        Value (USDT)       Type      
─────────────────────────────────────────────────────────────────────────────────
2024-01-15 10:30:45       44850.25        2.5400           113,493.00         BUY
2024-01-15 10:29:12       44825.00        1.2300           55,014.75          SELL
```

### Inflow/Outflow Analysis
```
================================================================================
INFLOW / OUTFLOW ANALYSIS
================================================================================
Inflow (Buying):   $2,450,230.50
Outflow (Selling): $1,890,120.25
Net Flow:          $560,110.25
Status: BULLISH (More buying than selling)
Inflow Percentage: 56.48%
```

## API Endpoints Used

- `GET /api/v3/depth` - Order book data
- `GET /api/v3/trades` - Recent trades
- `GET /api/v3/ticker/24hr` - 24-hour statistics
- `WebSocket` - Real-time streams

## Data Storage

The dashboard stores:
- Last 1000 trades in memory
- Last 500 whale transactions
- Last 100 price points
- Volume profile by price level

## Performance

- **REST Version**: Updates every 5 seconds
- **WebSocket Version**: Real-time tick updates (<100ms)
- **Memory Usage**: ~50-100 MB
- **CPU Usage**: Minimal (< 5%)
- **Network**: ~50-100 KB/sec

## Customization

### Change Refresh Interval
```python
dashboard.run_dashboard(refresh_interval=2)  # Update every 2 seconds
```

### Change Whale Detection Threshold
```python
dashboard.whale_threshold = 1.0  # Alert on >1 BTC instead of 0.5
```

### Add Different Trading Pair
```python
dashboard.symbol = 'ETHUSDT'  # For Ethereum
# Or 'BNBUSDT', 'ADAUSDT', etc.
```

## Troubleshooting

### "Connection Error" or "API Error"
- Check your internet connection
- Verify API keys are correct
- Check Binance API status

### "Module not found" errors
```bash
pip install --upgrade -r requirements.txt
```

### High CPU Usage
- Increase refresh interval
- Close other applications
- Use REST version instead of WebSocket

### Binance Rate Limiting
- Reduce update frequency
- Use WebSocket streams (don't count toward rate limit)

## Disclaimer

⚠️ **This tool is for educational and analysis purposes only.**
- Use at your own risk
- Not financial advice
- Do your own research (DYOR)
- Paper trade first
- Manage risk carefully

## Resources

- [Binance API Documentation](https://binance-docs.github.io/apidocs/)
- [WebSocket Streams](https://binance-docs.github.io/apidocs/#websocket-market-streams)
- [Trading Strategy Guides](https://www.binance.com/)

## Support

For issues, questions, or suggestions:
1. Open an GitHub issue
2. Check existing issues first
3. Provide error messages and details

## Contributing

Contributions welcome! Areas for improvement:
- More technical indicators
- ML-based predictions
- Alert notifications
- Database persistence
- Web UI dashboard

## License

MIT License - See LICENSE file for details

## Author

Created with ❤️ for crypto traders

---

**Made Professional. Made Fast. Made for You. 🚀**