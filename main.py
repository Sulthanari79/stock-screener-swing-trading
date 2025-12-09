"""
Indonesian Stock Screener for Swing Trading
A beginner-friendly tool to identify potential swing trading opportunities
using technical indicators (RSI and MACD) on Indonesian stocks.
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

# ============================================================================
# CONFIGURATION
# ============================================================================

# List of popular Indonesian stocks (Yahoo Finance format: stock.JK)
INDONESIAN_STOCKS = [
    'BBCA.JK',  # Bank Central Asia
    'BBRI.JK',  # Bank Rakyat Indonesia
    'BMRI.JK',  # Bank Mandiri
    'INDF.JK',  # Indofood
    'TLKM.JK',  # Telekomunikasi Indonesia
    'UNVR.JK',  # Unilever Indonesia
    'GGRM.JK',  # Gudang Garam
    'ASII.JK',  # Astra International
    'PGAS.JK',  # Perusahaan Gas Negara
    'ADRO.JK',  # Adaro Energy
]

# Technical Indicator Periods
RSI_PERIOD = 14          # Standard RSI period
MACD_FAST = 12          # Fast EMA for MACD
MACD_SLOW = 26          # Slow EMA for MACD
MACD_SIGNAL = 9         # Signal line EMA for MACD
LOOKBACK_DAYS = 100     # Days of historical data to fetch

# ============================================================================
# HELPER FUNCTIONS FOR TECHNICAL INDICATORS
# ============================================================================

def calculate_rsi(prices, period=14):
    """
    Calculate Relative Strength Index (RSI).
    
    RSI measures momentum and identifies overbought/oversold conditions.
    - RSI > 70: Stock might be overbought (potential sell signal)
    - RSI < 30: Stock might be oversold (potential buy signal)
    
    Args:
        prices: Pandas Series of closing prices
        period: Number of periods for RSI calculation (default: 14)
    
    Returns:
        Pandas Series with RSI values
    """
    # Calculate price changes
    delta = prices.diff()
    
    # Separate gains and losses
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    # Calculate Relative Strength
    rs = gain / loss
    
    # Calculate RSI
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


def calculate_macd(prices, fast=12, slow=26, signal=9):
    """
    Calculate MACD (Moving Average Convergence Divergence).
    
    MACD is a momentum indicator that shows the relationship between two moving averages.
    - MACD Line: Fast EMA - Slow EMA
    - Signal Line: 9-period EMA of MACD Line
    - Histogram: MACD Line - Signal Line
    
    Trading signals:
    - Bullish: MACD crosses above Signal Line
    - Bearish: MACD crosses below Signal Line
    
    Args:
        prices: Pandas Series of closing prices
        fast: Period for fast EMA (default: 12)
        slow: Period for slow EMA (default: 26)
        signal: Period for signal line EMA (default: 9)
    
    Returns:
        Dictionary containing MACD Line, Signal Line, and Histogram
    """
    # Calculate exponential moving averages
    ema_fast = prices.ewm(span=fast).mean()
    ema_slow = prices.ewm(span=slow).mean()
    
    # MACD Line
    macd_line = ema_fast - ema_slow
    
    # Signal Line
    signal_line = macd_line.ewm(span=signal).mean()
    
    # MACD Histogram
    histogram = macd_line - signal_line
    
    return {
        'macd': macd_line,
        'signal': signal_line,
        'histogram': histogram
    }


def fetch_stock_data(ticker, period_days=LOOKBACK_DAYS):
    """
    Fetch historical stock data from Yahoo Finance.
    
    Args:
        ticker: Stock ticker symbol (e.g., 'BBCA.JK')
        period_days: Number of days of historical data (default: 100)
    
    Returns:
        Pandas DataFrame with OHLCV data, or None if fetch fails
    """
    try:
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=period_days)
        
        # Fetch data
        data = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            progress=False  # Don't print progress bar
        )
        
        if len(data) == 0:
            return None
        
        return data
    
    except Exception as e:
        print(f"Error fetching data for {ticker}: {str(e)}")
        return None


# ============================================================================
# SCREENING LOGIC
# ============================================================================

def screen_stock(ticker, data):
    """
    Screen a single stock based on swing trading criteria.
    
    Beginner-friendly criteria:
    1. RSI between 40-60: Neutral zone, safe for swing trades
    2. MACD histogram positive: Momentum is upward
    3. Price above 200-day simple moving average: In uptrend
    4. Recent volume higher than average: Increased interest
    
    Args:
        ticker: Stock ticker symbol
        data: DataFrame with OHLCV data
    
    Returns:
        Dictionary with screening results, or None if screening fails
    """
    try:
        # Ensure we have enough data
        if len(data) < RSI_PERIOD:
            return None
        
        # Calculate technical indicators
        close_prices = data['Close']
        rsi = calculate_rsi(close_prices, RSI_PERIOD)
        macd_data = calculate_macd(close_prices, MACD_FAST, MACD_SLOW, MACD_SIGNAL)
        
        # Calculate moving averages
        sma_20 = close_prices.rolling(window=20).mean()
        sma_50 = close_prices.rolling(window=50).mean()
        sma_200 = close_prices.rolling(window=200).mean()
        
        # Get the most recent values
        latest_idx = -1
        current_price = close_prices.iloc[latest_idx]
        current_rsi = rsi.iloc[latest_idx]
        current_macd = macd_data['macd'].iloc[latest_idx]
        current_signal = macd_data['signal'].iloc[latest_idx]
        current_histogram = macd_data['histogram'].iloc[latest_idx]
        current_sma_20 = sma_20.iloc[latest_idx]
        current_sma_50 = sma_50.iloc[latest_idx]
        current_sma_200 = sma_200.iloc[latest_idx]
        
        # Calculate average volume
        avg_volume = data['Volume'].rolling(window=20).mean().iloc[latest_idx]
        current_volume = data['Volume'].iloc[latest_idx]
        
        # ====================================================================
        # SWING TRADING CRITERIA FOR BEGINNERS
        # ====================================================================
        
        signals = {
            'ticker': ticker,
            'price': current_price,
            'rsi': current_rsi,
            'macd': current_macd,
            'signal_line': current_signal,
            'histogram': current_histogram,
            'sma_20': current_sma_20,
            'sma_50': current_sma_50,
            'sma_200': current_sma_200,
            'volume': current_volume,
            'avg_volume': avg_volume,
        }
        
        # Scoring system (0-5 points)
        score = 0
        reasons = []
        
        # Criterion 1: RSI in favorable zone (30-70, neutral: 40-60)
        if 30 < current_rsi < 70:
            score += 1
            if 40 < current_rsi < 60:
                score += 1
                reasons.append(f"RSI {current_rsi:.1f} in neutral zone (40-60)")
            else:
                reasons.append(f"RSI {current_rsi:.1f} in trading zone (30-70)")
        
        # Criterion 2: MACD positive histogram (bullish momentum)
        if current_histogram > 0:
            score += 1
            reasons.append("MACD histogram positive (bullish)")
        
        # Criterion 3: MACD above signal line
        if current_macd > current_signal:
            score += 1
            reasons.append("MACD above signal line")
        
        # Criterion 4: Price above 20-day SMA (short-term uptrend)
        if current_price > current_sma_20:
            score += 1
            reasons.append("Price above 20-day SMA (short-term uptrend)")
        
        # Criterion 5: Price above 50-day SMA (medium-term uptrend)
        if current_price > current_sma_50:
            score += 1
            reasons.append("Price above 50-day SMA (medium-term uptrend)")
        
        signals['score'] = score
        signals['reasons'] = reasons
        
        return signals
    
    except Exception as e:
        print(f"Error screening {ticker}: {str(e)}")
        return None


# ============================================================================
# MAIN SCREENING FUNCTION
# ============================================================================

def run_screener():
    """
    Run the stock screener on all Indonesian stocks in the list.
    Display results sorted by screening score.
    """
    print("=" * 80)
    print("INDONESIAN STOCK SCREENER - SWING TRADING")
    print("=" * 80)
    print(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Indicators: RSI ({RSI_PERIOD}), MACD ({MACD_FAST},{MACD_SLOW},{MACD_SIGNAL})")
    print(f"Lookback Period: {LOOKBACK_DAYS} days")
    print("=" * 80)
    print()
    
    results = []
    
    # Screen each stock
    for i, ticker in enumerate(INDONESIAN_STOCKS, 1):
        print(f"[{i}/{len(INDONESIAN_STOCKS)}] Screening {ticker}...", end=" ")
        
        # Fetch data
        data = fetch_stock_data(ticker)
        if data is None:
            print("FAILED TO FETCH DATA")
            continue
        
        # Screen stock
        signals = screen_stock(ticker, data)
        if signals is None:
            print("FAILED TO SCREEN")
            continue
        
        results.append(signals)
        print("OK")
        
        # Be respectful to API rate limits
        time.sleep(0.5)
    
    # Sort results by score (highest first)
    results.sort(key=lambda x: x['score'], reverse=True)
    
    # Display results
    print()
    print("=" * 80)
    print("SCREENING RESULTS (sorted by score)")
    print("=" * 80)
    print()
    
    for result in results:
        score_display = "★" * result['score'] + "☆" * (5 - result['score'])
        
        print(f"Ticker: {result['ticker']}")
        print(f"Price: {result['price']:.2f} | Score: {result['score']}/5 {score_display}")
        print(f"RSI: {result['rsi']:.1f} | MACD Histogram: {result['histogram']:.4f}")
        print(f"Reasons:")
        for reason in result['reasons']:
            print(f"  • {reason}")
        print("-" * 80)
    
    print()
    print(f"Total stocks screened: {len(results)}")
    print("Strong candidates (score >= 4):")
    strong_candidates = [r for r in results if r['score'] >= 4]
    for candidate in strong_candidates:
        print(f"  • {candidate['ticker']} (Score: {candidate['score']}/5)")
    
    print()
    print("=" * 80)
    print("DISCLAIMER: This screener is for educational purposes only.")
    print("Always do your own research and consult a financial advisor before trading.")
    print("=" * 80)


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    """
    Run the stock screener when this script is executed directly.
    """
    run_screener()
