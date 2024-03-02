import requests
import json
import pandas as pd
from StockEnum import ApiParameter
import sys
from datetime import datetime

stock_data = []
from_date =  datetime.strptime(sys.argv[1], '%Y-%m-%d').date()
to_date = datetime.strptime(sys.argv[2], '%Y-%m-%d').date()

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

			for data in response['data']['candles']:
				stock_data.append(data)
				columns = ["Date", "Open", "High", "Low","Close","Volume", "Open Interest"]
				df = pd.DataFrame(stock_data, columns=columns)
				df['Date'] = pd.to_datetime(df['Date']).dt.date
		else:
			print("Something Went Wrong", response.text)
		return df
	except Exception as e:
		print(e)

dfs = {}
for key  in ApiParameter:
  df_name = f'{key.name}'  # Name of DataFrame
  df = fetch_data_and_create_df(key.value, from_date, to_date)
  dfs[df_name] = df

# Now you have multiple DataFrames stored in the dictionary `dfs`
# You can access them using keys like dfs['df_string1'], dfs['df_string2'], etc.

# Example usage:
print(dfs['Bajaj_Finance'])  # Print DataFrame for 'string1'
# file_path = 'C:\Project\StockVerse\Finance.csv'
# dfs['Bajaj_Finance'].to_csv(file_path, sep='|', index=False)
