import requests
import json
import apikey

api_key = apikey.get_api_key()

url = 'https://api.eia.gov/v2/total-energy/data/?frequency=monthly&data[0]=value&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000'
url_with_key = f'{url}&api_key={api_key}'
response = requests.get(url_with_key)

if response.status_code == 200:
    data = response.json() 
    print(json.dumps(data, indent=2))
else:
    print(f"Error: {response.status_code} - {response.text}")
