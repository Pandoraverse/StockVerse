import pandas as pd
from datetime import datetime
from seed_database import SeedDatabase
from StockEnum import NSEScripts
from api_controller import ApiController

class StockDataFetcher:
    def __init__(self, from_date, to_date):
        self.from_date = from_date
        self.to_date = to_date
        self.stock_data = []
        
    def fetch_data_and_create_df(self, parameter):
        url = f"https://api.upstox.com/v2/historical-candle/NSE_EQ|{parameter}/day/{self.to_date}/{self.from_date}"
        payload = {}
        headers = {'Accept': 'application/json'}

        response = ApiController.get_data(url, payload, headers)
        if response:
            data = self.extract_data(response)
            if data:
                return pd.DataFrame(data)
        return None
    
    def extract_data(self, response):
        try:
            return response['data']['candles']
        except KeyError:
            print("Error: Invalid response format")
        return None

    def fetch_stock_data(self, api_parameter):
        df = self.fetch_data_and_create_df(api_parameter.value)
        return df


class StockDataProcessor:
    @staticmethod
    def process_stock_data(df):
        if df is not None:
            df.columns = ["Date", "Open", "High", "Low", "Close", "Volume", "Open Interest"]
            df['Date'] = pd.to_datetime(df['Date']).dt.date
        return df


def main():
    #Seed/update data from 2004 to today
    from_date = datetime(2004, 1, 1).date()
    to_date = datetime.today().date()

    stock_data_fetcher = StockDataFetcher(from_date, to_date)
    stock_data_processor = StockDataProcessor()
    seed_db = SeedDatabase()

    for key in NSEScripts:
        df = stock_data_fetcher.fetch_stock_data(key)
        df_processed = stock_data_processor.process_stock_data(df)
        table_name = f"{key.name}_Data"
        seed_db.persist_all(table_name, df_processed)

#To ensure that the main() function is only executed if the script is run directly as the main program, 
#And not when it is imported as a module into another script.
if __name__ == "__main__":
    main()
