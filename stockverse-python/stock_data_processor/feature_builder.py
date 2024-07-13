import pandas as pd
import numpy as np
from talipp.indicators import RSI, MACD, BB
from talipp.ohlcv import OHLCVFactory
from database_handler import DatabaseHandler
import StockEnum

def extract_technical_features(df):
    
    # 1. Moving Averages
    df['SMA_10'] = df['Close'].rolling(window=10).mean()
    df['EMA_10'] = df['Close'].ewm(span=10, adjust=False).mean()
    df['SMA_30'] = df['Close'].rolling(window=30).mean()
    df['EMA_30'] = df['Close'].ewm(span=30, adjust=False).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
    df['SMA_100'] = df['Close'].rolling(window=100).mean()
    df['EMA_100'] = df['Close'].ewm(span=100, adjust=False).mean()

    # 2. RSI (Relative Strength Index)
    df['RSI_14'] = RSI(period=14, input_values= df['Close'].values)

    # 3. MACD (Moving Average Convergence Divergence)
    macd_values = MACD(fast_period=12, slow_period=26, signal_period=9, input_values= df['Close'].values)
    df['MACD'] =  [obj.macd if obj is not None else np.nan for obj in macd_values]
    df['MACD_Signal'] = [obj.signal if obj is not None else np.nan for obj in macd_values]

    # 4. Bollinger Bands
    bb= BB(period=20, std_dev_mult=5, input_values=df['Close'].values)
    df['BB_Upper'] = [obj.lb if obj is not None else np.nan for obj in bb]
    df['BB_Middle'] = [obj.ub if obj is not None else np.nan for obj in bb]
    df['BB_Lower'] = [obj.cb if obj is not None else np.nan for obj in bb]

    # 5. Lagged Features (e.g., Previous day's closing price)
    df['Prev_Close'] = df['Close'].shift(1)

    # 6. Example of sentiment feature (hypothetical)  -- This can't be implemented right now but will be in future.
    # Assume sentiment_score is a hypothetical sentiment score from NLP analysis
    # df['Sentiment_Score'] = sentiment_score

    # Additional features can be added similarly

    # Drop rows with NaN values that result from rolling window operations
    df.dropna(inplace=True)

    # Now df contains the original OHLC data with additional engineered features
    print(df.head())


def main():
    print('Feature builder module')    
    db_handler =  DatabaseHandler()
    df = db_handler.get_data(StockEnum.NSEScripts.Tata_Power.name)
    extract_technical_features(df)

if __name__ == "__main__":
    main()
