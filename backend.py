import requests
import json
import apikey
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
from apikey import *
import os
from isodata.src.isodata.sessions import Session

def generate_table(url):
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors
    #https://www.ercot.com/content/cdr/html/20241010_dam_spp.html
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    headers = [th.get_text(strip=True) for th in table.find_all('th')]
    data = []
    for row in table.find_all('tr')[1:]:  # Skip the header row
        cells = [td.get_text(strip=True) for td in row.find_all('td')]
        if cells:  # Avoid empty rows
            data.append(cells)

    df = pd.DataFrame(data, columns=headers)
    return df


ercot_data = {}


def build_data(start_yr, start_m, start_d):
    start_date = datetime(start_yr, start_m, start_d)
    yesterday = (datetime.now() - timedelta(days=1)).date()
    current_date = start_date.date()
    while current_date <= yesterday:
        t_date = current_date.strftime("%Y%m%d")
        print(t_date)
        url = f"https://www.ercot.com/content/cdr/html/{t_date}_real_time_spp.html"
        df = generate_table(url)
        for column in df.columns:
            if column not in ercot_data:
                ercot_data[column] = {}

            for index, row in df.iterrows():
                date = row['Oper Day']
                interval = row['Interval Ending']
                value = row[column]
                ercot_data[column][(date, interval)] = value

        current_date += timedelta(days=1)


build_data(2024, 5, 11)
primary_key = get_ercot_primary_key()
creds = {
  "user": "arnav",
  "credentials":
  {
    "ercot_public_api":
      {
        "username": "arnavarora15@gmail.com",
        "password": "BQFG_QUANT123",
        "primary_key": f"{primary_key}",
        "auth_url": "https://ercotb2c.b2clogin.com/ercotb2c.onmicrosoft.com/B2C_1_PUBAPI-ROPC-FLOW/oauth2/v2.0/token?username={username}&password={password}&grant_type=password&scope=openid+fec253ea-0d06-4272-a5e6-b478baeecd70+offline_access&client_id=fec253ea-0d06-4272-a5e6-b478baeecd70&response_type=id_token"
      }
  }
}


ercot = Session('ercot_public')
ercot.authorize(username=os.getenv('ERCOT_PUBLIC_USERNAME'),
                password=os.getenv('ERCOT_PUBLIC_PASSWORD'),
                primary_key=os.getenv('ERCOT_PUBLIC_PRIMARYKEY'),
                auth_url=os.getenv('ERCOT_PUBLIC_AUTHURL'))

# Retrieve the public report: SCED Shadow Prices and Binding Transmission Constraints
emil = 'NP6-86-CD'
page = 1
report_list, meta = ercot.fetch_listing(emil_id=emil, page=page)
print(f'{emil} Page {page} Returned {len(report_list)} documents\n')
print(json.dumps(meta, indent=4))

# Retrieve the first (most recent) file in the document list.
# Will raise a FileNotFound error if it cannot retrieve from ERCOT
data_file = ercot.fetch_url(report_list[0][2], f'/documents/ercot/{emil}')
