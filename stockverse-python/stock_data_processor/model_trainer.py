from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, accuracy_score
import matplotlib.pyplot as plt
import pandas as pd

def train(stock_df):
    stock_df= stock_df.rename(str,axis="columns") 
    stock_df.columns = stock_df.columns.astype(str)
    model = RandomForestClassifier(n_estimators=100, min_samples_split=100, random_state=1)
    train = stock_df.iloc[:-200]
    test = stock_df.iloc[-200:]
    predictors = ["Open", "Volume", "Close", "SMA50", "EMA50", "SMA100", "EMA100", "RSI14", "MACD", "STOCHOSC", "AO", "STOCHRSI" ,"TSI"]#, 'BBMiddle', 'BBLower']
    model.fit(train[predictors], train["Target"])

    preds = model.predict(test[predictors])
    preds = pd.Series(preds, index=test.index)
    print(preds.value_counts() / preds.shape[0])

    #Calcualtes how precisely model calculates the prices going up or down.
    precision = precision_score(test["Target"], preds)
    print('Precision Score: {0}'.format(precision))

    combined = pd.concat([test["Target"], preds], axis=1)
    #print(preds.tail(100))
    combined.plot()
    #Calculates the accuracy of the model.
    accuracy = accuracy_score(test["Target"], preds)
    print('Accuracy: {0}'.format(accuracy))

    # plt.show()