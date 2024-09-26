import requests
import json
import apikey

api_key = apikey.get_api_key()

url = f'https://api.eia.gov/series/?api_key={api_key}&series_id=ELEC.GEN.ALL-US-99.A'

response = requests.get(url)

if response.status_code == 200:
    data = response.json() 
    print(json.dumps(data, indent=2))
else:
    print(f"Error: {response.status_code} - {response.text}")
