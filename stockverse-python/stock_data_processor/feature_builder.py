import pandas as pd
import numpy as np
from database_handler import DatabaseHandler
import StockEnum

def extract_technical_features(df):
    
    # 1. Moving Averages
    df['SMA_10'] = df['Close'].rolling(window=10).mean()
    df['EMA_10'] = df['Close'].ewm(span=10, adjust=False).mean()

    # 2. RSI (Relative Strength Index)
    # df['RSI_14'] = talib.RSI(df['Close'].values, timeperiod=14)

    # 3. MACD (Moving Average Convergence Divergence)
    # macd, macdsignal, macdhist = talib.MACD(df['Close'].values, fastperiod=12, slowperiod=26, signalperiod=9)
    # df['MACD'] = macd
    # df['MACD_Signal'] = macdsignal

    # 4. Bollinger Bands
    # upper_band, middle_band, lower_band = talib.BBANDS(df['Close'].values, timeperiod=20)
    # df['BB_Upper'] = upper_band
    # df['BB_Middle'] = middle_band
    # df['BB_Lower'] = lower_band

    # 5. Lagged Features (e.g., Previous day's closing price)
    # df['Prev_Close'] = df['Close'].shift(1)

    # 6. Example of sentiment feature (hypothetical)
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
