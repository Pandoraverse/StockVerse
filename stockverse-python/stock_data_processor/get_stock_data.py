from sqlalchemy import create_engine
from read_properties import load_properties
import pandas as pd
import sys

class GetStockDetails:
    def __init__(self):
        self.conn_str = load_properties("conn_str")
        self.engine = create_engine(self.conn_str, connect_args={'timeout': 180})

    def get_stock_details(self, stock_name):
        if not '_Data' in stock_name:
            stock_name = f"{stock_name}_Data"
        df = pd.read_sql_table(stock_name, self.engine)
        df['Open_Interest'] = df['Open_Interest'].astype('int64')
        return df
    
def main():
    if(len(sys.argv) != 0 and len(sys.argv) == 2):
        stockName = sys.argv[1]
    else:
        print("Enter the Stock Name")
        raise Exception("Enter the stock name")

    stock_data = GetStockDetails().get_stock_details(stockName)
    #print(stock_data)
    return stock_data
if __name__ == "__main__":
    main()
