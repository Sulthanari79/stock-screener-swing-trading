# Indonesian Stock Screener for Swing Trading

A powerful Python-based stock screener designed specifically for swing trading strategies on the Indonesian stock exchange (IDX). This tool helps traders identify promising trading opportunities using technical analysis indicators and customizable screening criteria.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [Technical Indicators](#technical-indicators)
- [Screening Criteria](#screening-criteria)
- [Configuration Options](#configuration-options)
- [Troubleshooting](#troubleshooting)
- [Disclaimers](#disclaimers)

## Overview

This stock screener is designed for swing traders who want to identify Indonesian stocks with potential for 2-5 day trading moves. It combines multiple technical analysis indicators to filter stocks based on momentum, volatility, trend strength, and volume conditions.

The screener analyzes data from the Indonesian Stock Exchange (IDX) and helps traders make data-driven decisions by automating the initial stock scanning process.

## Features

- **Real-time Data Integration**: Connects to Indonesian stock market data sources
- **Multiple Technical Indicators**: RSI, MACD, Bollinger Bands, Moving Averages, ATR, Volume analysis
- **Customizable Screening Criteria**: Configure thresholds for each indicator
- **Batch Processing**: Screen multiple stocks in a single run
- **Export Results**: Save screening results in CSV format
- **Backtesting Support**: Test screening criteria against historical data
- **Performance Metrics**: Analyze win rate and profitability of screening criteria
- **Alert System**: Get notified when stocks meet your criteria

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step-by-Step Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Sulthanari79/stock-screener-swing-trading.git
   cd stock-screener-swing-trading
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure API Keys** (if required):
   - Create a `.env` file in the project root directory
   - Add your API keys for data providers:
     ```
     IDX_API_KEY=your_api_key_here
     DATA_PROVIDER=your_provider
     ```

## Quick Start

1. **Run the screener**:
   ```bash
   python screener.py
   ```

2. **View results**:
   - Results are displayed in the console
   - CSV export is saved to `results/` directory

3. **Check alerts**:
   - Monitor the alert log file in `logs/alerts.log`

## Usage Guide

### Basic Screening

Run a basic screen with default criteria:
```bash
python screener.py --config default
```

### Custom Screening

Use a custom configuration file:
```bash
python screener.py --config custom_config.json
```

### Backtesting Your Criteria

Test your screening criteria against historical data:
```bash
python screener.py --backtest --from-date 2023-01-01 --to-date 2024-01-01
```

### Export Results

Export screening results to CSV:
```bash
python screener.py --export results.csv
```

### Advanced Options

```bash
# Screen specific stocks only
python screener.py --stocks BBRI BBCA ASII

# Set minimum price filter
python screener.py --min-price 1000 --max-price 50000

# Screen by sector
python screener.py --sector banking

# Include dividend stocks only
python screener.py --dividends-only

# Set lookback period (days)
python screener.py --lookback 60
```

### Command Line Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `--config` | Configuration file to use | `--config custom.json` |
| `--stocks` | Specific stocks to screen | `--stocks BBRI BBCA ASII` |
| `--sector` | Filter by sector | `--sector banking` |
| `--min-price` | Minimum stock price | `--min-price 1000` |
| `--max-price` | Maximum stock price | `--max-price 50000` |
| `--min-volume` | Minimum daily volume | `--min-volume 100000` |
| `--lookback` | Historical data lookback (days) | `--lookback 60` |
| `--backtest` | Run backtesting mode | `--backtest` |
| `--from-date` | Backtest start date (YYYY-MM-DD) | `--from-date 2023-01-01` |
| `--to-date` | Backtest end date (YYYY-MM-DD) | `--to-date 2024-01-01` |
| `--export` | Export results to CSV | `--export results.csv` |
| `--dividends-only` | Only show dividend-paying stocks | `--dividends-only` |
| `--verbose` | Detailed output logging | `--verbose` |

## Technical Indicators

### 1. Relative Strength Index (RSI)

**What it measures**: Momentum oscillator measuring overbought/oversold conditions (0-100 scale)

**Default thresholds**:
- Oversold: RSI < 30 (potential reversal up)
- Overbought: RSI > 70 (potential reversal down)
- Sweet spot for swing trading: 40-60 (neutral momentum)

**How it's used**: Identify stocks with strong momentum but not yet overextended

**Configuration**:
```json
{
  "rsi": {
    "period": 14,
    "oversold": 30,
    "overbought": 70
  }
}
```

### 2. MACD (Moving Average Convergence Divergence)

**What it measures**: Trend direction and momentum using exponential moving averages

**Default settings**:
- Fast EMA: 12 periods
- Slow EMA: 26 periods
- Signal line: 9 periods

**How it's used**: Identify trend changes and momentum reversals

**Configuration**:
```json
{
  "macd": {
    "fast_period": 12,
    "slow_period": 26,
    "signal_period": 9
  }
}
```

### 3. Bollinger Bands

**What it measures**: Volatility and support/resistance levels (2 standard deviations)

**Default settings**:
- Period: 20
- Standard Deviations: 2
- Entry signal: Price touches lower band
- Exit signal: Price touches upper band

**How it's used**: Identify oversold conditions and volatility breakouts

**Configuration**:
```json
{
  "bollinger_bands": {
    "period": 20,
    "std_dev": 2,
    "touch_lower_band": true
  }
}
```

### 4. Moving Averages

**What it measures**: Trend direction and support/resistance levels

**Default settings**:
- Short-term MA: 20-day (recent trend)
- Medium-term MA: 50-day (intermediate trend)
- Long-term MA: 200-day (long-term trend)

**How it's used**: Confirm trend and identify trend reversals

**Configuration**:
```json
{
  "moving_averages": {
    "short_period": 20,
    "medium_period": 50,
    "long_period": 200
  }
}
```

### 5. Average True Range (ATR)

**What it measures**: Volatility of the stock (typical price movement range)

**Default settings**:
- Period: 14
- High volatility: ATR > 2% of current price
- Low volatility: ATR < 0.5% of current price

**How it's used**: Filter stocks by volatility for swing trading opportunities

**Configuration**:
```json
{
  "atr": {
    "period": 14,
    "min_volatility_percent": 1.5,
    "max_volatility_percent": 5.0
  }
}
```

### 6. Volume Analysis

**What it measures**: Trading activity and conviction behind price moves

**Default settings**:
- Volume above 20-day average: 1.5x or higher
- Minimum daily volume: 100,000 shares

**How it's used**: Confirm trend strength and identify breakouts

**Configuration**:
```json
{
  "volume": {
    "min_volume": 100000,
    "volume_ma_period": 20,
    "volume_multiplier": 1.5
  }
}
```

## Screening Criteria

### Default Screening Criteria

The screener comes with predefined criteria optimized for swing trading:

1. **RSI Condition**: 30-70 (avoid extreme conditions)
2. **MACD**: Bullish crossover or histogram above signal line
3. **Volume**: Above 1.5x 20-day average
4. **Price**: Between 1,000 IDR and 50,000 IDR
5. **Volatility**: 1.5% - 5% ATR
6. **Trend**: Price above 20-day moving average
7. **Momentum**: 5-day momentum > 0

### Custom Criteria Example

Create a file `my_criteria.json`:
```json
{
  "criteria": {
    "rsi": {
      "enabled": true,
      "min": 40,
      "max": 60
    },
    "macd": {
      "enabled": true,
      "bullish_crossover": true
    },
    "volume": {
      "enabled": true,
      "min_volume": 200000,
      "above_average_ma": 2.0
    },
    "price": {
      "enabled": true,
      "min": 2000,
      "max": 30000
    },
    "volatility": {
      "enabled": true,
      "min_percent": 2.0,
      "max_percent": 4.0
    },
    "trend": {
      "enabled": true,
      "above_short_ma": true,
      "short_ma_above_long_ma": true
    },
    "momentum": {
      "enabled": true,
      "min_5day_momentum": 0.5
    }
  }
}
```

## Configuration Options

### Main Configuration File (`config.json`)

```json
{
  "data_source": {
    "provider": "idx",
    "api_endpoint": "https://api.idx.co.id",
    "timeout": 30,
    "retry_attempts": 3
  },
  "screening": {
    "lookback_days": 60,
    "min_stock_price": 1000,
    "max_stock_price": 50000,
    "min_daily_volume": 100000,
    "exclude_suspended": true,
    "exclude_delisted": true
  },
  "indicators": {
    "rsi_period": 14,
    "macd_fast": 12,
    "macd_slow": 26,
    "macd_signal": 9,
    "bb_period": 20,
    "bb_std_dev": 2,
    "atr_period": 14,
    "ma_short": 20,
    "ma_medium": 50,
    "ma_long": 200
  },
  "output": {
    "export_format": "csv",
    "export_directory": "./results",
    "include_charts": false,
    "save_alerts": true,
    "alert_log_file": "./logs/alerts.log"
  },
  "performance": {
    "log_backtest_results": true,
    "calculate_win_rate": true,
    "min_trades_for_analysis": 10
  }
}
```

### Environment Variables

Create a `.env` file:
```
IDX_API_KEY=your_api_key
IDX_API_SECRET=your_api_secret
DATA_PROVIDER=idx
LOG_LEVEL=INFO
CACHE_ENABLED=true
CACHE_TTL=3600
PROXY_ENABLED=false
PROXY_URL=http://proxy.example.com:8080
```

### Logging Configuration

Edit `logging_config.json` to customize logging:
```json
{
  "version": 1,
  "disable_existing_loggers": false,
  "formatters": {
    "standard": {
      "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    }
  },
  "handlers": {
    "console": {
      "class": "logging.StreamHandler",
      "level": "INFO",
      "formatter": "standard"
    },
    "file": {
      "class": "logging.FileHandler",
      "level": "DEBUG",
      "filename": "screener.log",
      "formatter": "standard"
    }
  },
  "root": {
    "level": "INFO",
    "handlers": ["console", "file"]
  }
}
```

## Troubleshooting

### Common Issues and Solutions

#### 1. **"No data available" error**
**Problem**: Screener cannot retrieve stock data
**Solutions**:
- Verify internet connection
- Check API key validity in `.env` file
- Verify data provider is accessible
- Try with `--verbose` flag for more details

```bash
python screener.py --verbose
```

#### 2. **"Invalid configuration" error**
**Problem**: Configuration file has incorrect format
**Solutions**:
- Validate JSON syntax using online JSON validator
- Check file encoding is UTF-8
- Ensure all required fields are present
- Check file permissions (readable)

```bash
# Validate configuration
python -m json.tool config.json
```

#### 3. **High memory usage**
**Problem**: Screener uses excessive memory when screening large number of stocks
**Solutions**:
- Reduce `lookback_days` in configuration
- Process stocks in batches
- Increase virtual memory available
- Check for data provider rate limits

```bash
# Process stocks in batches
python screener.py --stocks BBRI BBCA ASII
python screener.py --stocks INDF UNVR TLKM
```

#### 4. **Slow performance**
**Problem**: Screener takes too long to complete
**Solutions**:
- Enable caching in `.env`: `CACHE_ENABLED=true`
- Reduce lookback period: `--lookback 30`
- Filter by price range: `--min-price 5000 --max-price 20000`
- Run during off-market hours

```bash
python screener.py --lookback 30 --min-price 5000 --max-price 20000
```

#### 5. **"Connection timeout" error**
**Problem**: Cannot connect to data provider
**Solutions**:
- Check if data provider API is online
- Increase timeout in config.json: `"timeout": 60`
- Check firewall/proxy settings
- Try using VPN if connection is unstable

#### 6. **Missing indicators in results**
**Problem**: Some technical indicators are not calculated
**Solutions**:
- Ensure sufficient historical data (at least 200 days)
- Check if `lookback_days` is large enough
- Verify indicator periods are less than lookback days
- Check data quality for selected stocks

### Debug Mode

Enable verbose output for troubleshooting:
```bash
python screener.py --verbose --debug
```

This will:
- Print detailed execution logs
- Save raw data to files for inspection
- Show API response details
- Display calculation steps for indicators

### Log Files

Check log files in the `logs/` directory:
- `screener.log`: General application logs
- `alerts.log`: Stock alerts matching criteria
- `errors.log`: Error logs (if error handling enabled)
- `backtest.log`: Backtesting results

## Disclaimers

### Important Legal Disclaimer

**This tool is provided for educational and informational purposes only.**

1. **Not Financial Advice**: This screener does not constitute financial advice, investment recommendation, or an offer to buy or sell securities. Always consult with a qualified financial advisor before making investment decisions.

2. **Past Performance**: Historical data and backtesting results are not indicative of future performance. Past performance does not guarantee future results.

3. **Market Risk**: Stock trading, particularly swing trading, involves substantial risk of loss. You may lose some or all of your investment. Do not invest more than you can afford to lose.

4. **No Warranty**: This software is provided "AS IS" without warranty of any kind, express or implied. The developers assume no responsibility for errors, omissions, or consequences of using this tool.

5. **Data Accuracy**: While we strive for accuracy, we do not guarantee that all data is accurate, complete, or timely. Market data may have delays or errors.

6. **Technical Limitations**: 
   - Technical indicators are lagging by nature
   - Past indicator signals do not guarantee future signals
   - Market conditions change rapidly
   - External events can cause unexpected price movements

7. **Liquidity Risk**: Not all Indonesian stocks have sufficient liquidity. Ensure selected stocks have adequate trading volume before executing trades.

8. **System Risk**: Software bugs, API failures, or connectivity issues may occur. Always have backup plans and never rely solely on automated tools.

9. **Regulatory Compliance**: Ensure your trading activities comply with Indonesian financial regulations and your broker's terms of service.

10. **Responsible Trading**: 
    - Always use stop losses
    - Size your positions appropriately
    - Never use leverage without understanding risks
    - Keep detailed trading records
    - Review and adjust strategies regularly

### User Responsibility

By using this tool, you acknowledge that:
- You understand the risks involved in stock trading
- You are responsible for your own investment decisions
- You will not hold the developers liable for any losses
- You comply with all applicable laws and regulations

## Getting Help

### Support Resources

- **Issues**: Report bugs or request features on [GitHub Issues](https://github.com/Sulthanari79/stock-screener-swing-trading/issues)
- **Discussions**: Join discussions on [GitHub Discussions](https://github.com/Sulthanari79/stock-screener-swing-trading/discussions)
- **Documentation**: Check wiki for advanced topics
- **Email**: Contact for support

### Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Changelog

### Version 1.0.0 (2024)
- Initial release
- Core screening engine
- Multiple technical indicators
- Backtesting support
- CSV export functionality

---

**Last Updated**: 2025-12-09  
**Maintainer**: Sulthanari79  
**Python Version**: 3.8+
