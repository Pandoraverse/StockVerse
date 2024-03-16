import requests
import json
import pandas as pd
from StockEnum import ApiParameter
import sys
from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table
from Read_Properties import load_properties

stock_data = []
from_date =  datetime.strptime(sys.argv[1], '%Y-%m-%d').date()
to_date = datetime.strptime(sys.argv[2], '%Y-%m-%d').date()

dfs = {}

#Fetches the data from the API and stores it in a df and returns the df.
def fetch_data_and_create_df(parameter, from_date, to_date):
	url = f"https://api.upstox.com/v2/historical-candle/NSE_EQ|{parameter}/day/{to_date}/{from_date}"
	payload={}
	headers = {
  	  'Accept': 'application/json'
  	}
	try:
		response = requests.request("GET", url, headers=headers, data=payload)
		if(response.status_code == 200):
			response = json.loads(response.text)
			stock_data = []
			#Loops through the response JSON and stores the OLHC value in a df.
			for data in response['data']['candles']:
				stock_data.append(data)
			
			# Create DataFrame after collecting all data
			columns = ["Date", "Open", "High", "Low","Close","Volume", "Open Interest"]
			df = pd.DataFrame(stock_data, columns=columns)
			df['Date'] = pd.to_datetime(df['Date']).dt.date
			return df
		else:
			print("Something Went Wrong", response.text)
			return None

	except Exception as e:
		print(e)
		return None



def add_data_to_db():
	#use this line to get the connection string from the properties file and modify/delete this method as per the need.
	conn_str = str(load_properties("conn_str"))



# This will loop through the ENUM and fetch and store the OLHC value as per the stock name in a dictionary.
for key in ApiParameter:
  df_name = f'{key.name}'  # Name of DataFrame
  #df = fetch_data_and_create_df(key.value, from_date, to_date)
  dfs[df_name] = df

# Print the df as per the stock name
print(dfs)

