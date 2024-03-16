import requests
import json

class ApiController:
    def get_data(url, payload, headers):
        try:
            response = requests.get(url, headers=headers, data=payload)
            if response.status_code == 200:
                return json.loads(response.text)
            else:
                print("Something Went Wrong:", response.text)
        except Exception as e:
            print("Error:", e)
        return None