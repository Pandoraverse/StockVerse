from sqlalchemy import create_engine
from read_properties import load_properties
from get_stock_data import GetStockDetails
import pandas as pd

class DatabaseHandler:
    def __init__(self):
        self.conn_str = load_properties("conn_str")
        self.engine = create_engine(self.conn_str, connect_args={'timeout': 180})

    def compare_data(self, api_df, table_name):
        #Gets all the data present in the table, and removes the columns not required for comparision
        db_df = GetStockDetails.get_stock_details(self, table_name).drop(columns=['Id', 'Reserved_Field_1','Reserved_Field_2','Reserved_Field_3','Reserved_Field_4','Reserved_Field_5'], axis = 1, inplace = False)
        
        #Converts the date into a 'yyyy-MM-dd' format and also sets the Date as Index for comparision
        db_df['Date'] = pd.to_datetime(db_df['Date']).dt.date
        db_df.set_index('Date', inplace=True)
        api_df['Date'] = pd.to_datetime(api_df['Date']).dt.date
        api_df.set_index('Date', inplace=True)

        #Stores all the dates found in db and coming from api into a list.
        api_dates = api_df.index.to_list()
        db_dates = db_df.index.to_list()

        #Extracts the unique dates, sorts the columns date wise and resets the index
        extra_dates = list(set(api_dates) - set(db_dates))
        extra_rows_api_df = api_df.loc[extra_dates].sort_index(axis = 0, ascending=True).reset_index()
        return extra_rows_api_df
    
    def get_data(self, stock_name):
        db_df = GetStockDetails.get_stock_details(self, stock_name).drop(columns=['Id', 'Reserved_Field_1','Reserved_Field_2','Reserved_Field_3','Reserved_Field_4','Reserved_Field_5'], axis = 1, inplace = False)
        return db_df
        
    def persist_all(self, table_name, df):
        if df is not None:
            unique_df = DatabaseHandler.compare_data(self, df, table_name)
            if not unique_df.empty:
                unique_df.to_sql(table_name, self.engine, if_exists='append', index=False)
                print(f"Data added to {table_name} table.")
            else:
                print(f"No unique data found for the table : {table_name}")
        else:
            print(f"No data for {table_name}.")

