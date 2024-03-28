from sqlalchemy import create_engine
from read_properties import load_properties

class SeedDatabase:
    def __init__(self):
        self.conn_str = load_properties("conn_str")
        self.engine = create_engine(self.conn_str, connect_args={'timeout': 180})

    def persist_all(self, table_name, df):
        if df is not None:
            df.to_sql(table_name, self.engine, if_exists='append', index=False)
            print(f"Data added to {table_name} table.")
        else:
            print(f"No data for {table_name}.")
