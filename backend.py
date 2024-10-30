import requests
import json
import apikey
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

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


