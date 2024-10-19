import pandas as pd
import numpy as np
from talipp.indicators import RSI, MACD, BB
from talipp.ohlcv import OHLCVFactory
from database_handler import DatabaseHandler
from model_trainer import train
import StockEnum

def stochastic_oscillator(df, periods = 14):
  high_roll = df['High'].rolling(periods).max()
  low_roll = df['Low'].rolling(periods).min()  
  # Fast stochastic indicator
  num = df['Close'] - low_roll
  denom = high_roll - low_roll
  K = (num / denom) * 100    
  return K

def calculate_stoch_rsi(df, period=14):
    # Calculate RSI
    delta = df['Close'].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    # Calculate Stochastic RSI
    stoch_rsi = ((rsi - rsi.rolling(window=period).min()) /
                 (rsi.rolling(window=period).max() - rsi.rolling(window=period).min()))
    
    return stoch_rsi * 100

def calculate_tsi(df, short_window=25, long_window=13):
    # Calculate the price changes
    delta = df['Close'].diff(1)
    
    # Calculate double smoothed EMA of positive changes
    abs_delta = abs(delta)
    double_smoothed_delta = df["EMA5"].ewm(span=5).mean()
    double_smoothed_abs_delta = abs_delta.ewm(span=5).mean()
    
    # Calculate TSI
    tsi = 100 * (double_smoothed_delta / double_smoothed_abs_delta)
    return tsi

def calculate_vwap(df):
    # Ensure the DataFrame has 'Close', 'Volume', 'High', and 'Low' columns
    typical_price = (df['Close'] + df['High'] + df['Low']) / 3
    return(typical_price * df['Volume']).cumsum() / df['Volume'].cumsum()

def extract_technical_features(df):
    df["STOCHOSC"] = stochastic_oscillator(df)
    # 1. Moving Averages
    df['SMA5'] = df['Close'].rolling(window=10).mean()
    df['EMA5'] = df['Close'].ewm(span=10, adjust=False).mean()
    df['SMA20'] = df['Close'].rolling(window=20).mean()
    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
    df['SMA34'] = df['Close'].rolling(window=34).mean()
    df['SMA50'] = df['Close'].rolling(window=50).mean()
    df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()
    df['SMA100'] = df['Close'].rolling(window=100).mean()
    df['EMA100'] = df['Close'].ewm(span=100, adjust=False).mean()
    df['SMA250'] = df['Close'].rolling(window=250).mean()
    df['EMA250'] = df['Close'].ewm(span=250, adjust=False).mean()

    # 2. RSI (Relative Strength Index)
    df['RSI14'] = RSI(period=14, input_values= df['Close'].values)

    # 3. MACD (Moving Average Convergence Divergence)
    macd_values = MACD(fast_period=12, slow_period=26, signal_period=9, input_values= df['Close'].values)
    df['MACD'] =  [obj.macd if obj is not None else np.nan for obj in macd_values]
    df['MACDSignal'] = [obj.signal if obj is not None else np.nan for obj in macd_values]

    # 4. Bollinger Bands
    bb= BB(period=20, std_dev_mult=5, input_values=df['Close'].values)
    df['BBUpper'] = [obj.lb if obj is not None else np.nan for obj in bb]
    df['BBMiddle'] = [obj.ub if obj is not None else np.nan for obj in bb]
    df['BBLower'] = [obj.cb if obj is not None else np.nan for obj in bb]

    # 5. Lagged Features (e.g., Previous day's closing price, tomorrow's price)
    df['PrevClose'] = df['Close'].shift(1)
    df['Tomorrow'] = df['Close'].shift(-1)
    df['Target'] = (df['Tomorrow'] > df['Close']).astype(int)

    # 6. Example of sentiment feature (hypothetical)  -- This can't be implemented right now but will be in future.
    # Assume sentiment_score is a hypothetical sentiment score from NLP analysis
    # df['Sentiment_Score'] = sentiment_score

    # Additional features can be added similarly

    #Adding AO, Stoch RSI, TSI and VWAP
    df['AO'] = df['SMA5'] - df['SMA34']
    df["STOCHRSI"] = calculate_stoch_rsi(df)
    df["TSI"] = calculate_tsi(df)
    df["VWAP"] = calculate_vwap(df)
    # Drop rows with NaN values that result from rolling window operations
    df.dropna(inplace=True)
    #df = df.drop(columns = 'Date')
    #print(df.corr())

    # Now df contains the original OHLC data with additional engineered features
    #print(df.head(10000))

    return df


def main():
    print('Feature builder module')    
    db_handler =  DatabaseHandler()
    df = db_handler.get_data(StockEnum.NSEScripts.Tata_Steel.name)
    stock_df_with_features = extract_technical_features(df)
    stock_df_with_features.plot.line(y="Close", x = "Date", use_index=True)
    # print(stock_df_with_features)
    train(stock_df_with_features)

if __name__ == "__main__":
    main()
