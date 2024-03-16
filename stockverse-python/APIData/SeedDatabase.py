from sqlalchemy import create_engine, MetaData, Table
from Read_Properties import load_properties

def add_data_to_db(dfs):
	conn_str = str(load_properties("conn_str"))
	engine = create_engine(conn_str, connect_args={'timeout': 180})

	for key, df in dfs.items():
		if df is not None:
			table_name = f"{key}_Data" 
			df.to_sql(table_name, engine, if_exists='replace', index=False)
			print(f"Data added to {table_name} table.")
		else:
			print(f"No data for {key}.")