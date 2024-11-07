import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from tqdm import tqdm

def generate_table(url):
    response = requests.get(url)
    response.raise_for_status()  

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    
    headers = [th.get_text(strip=True) for th in table.find_all('th')]
    data = [
        [cell.get_text(strip=True) for cell in row.find_all('td')]
        for row in table.find_all('tr')[1:] # skip header row
        if row.find_all('td')
    ]
    
    return pd.DataFrame(data, columns=headers)

ercot_data = {}

def build_data(start_yr, start_m, start_d):
    date = datetime(start_yr, start_m, start_d)
    days_left = (datetime.now() - date).days + 1
    
    ercot_df = pd.DataFrame()
    
    for _ in tqdm(range(days_left)):
        t_date = date.strftime("%Y%m%d")

        url = f"https://www.ercot.com/content/cdr/html/{t_date}_real_time_spp.html"
        df = generate_table(url)
        
        ercot_df = pd.concat([ercot_df, df], ignore_index=True)
        
        for column in df.columns:
            ercot_data.setdefault(column, {})
            
            for _, row in df.iterrows():
                key = (row['Oper Day'], row['Interval Ending'])
                ercot_data[column][key] = row[column]

        date += timedelta(days=1)
    return ercot_df

ercot_df = build_data(2024, 11, 1)