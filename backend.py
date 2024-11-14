import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from tqdm import tqdm
from sklearn.ensemble import IsolationForest

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

def remove_outliers(data: pd.DataFrame, fraction: float = 0.005) -> pd.DataFrame:
    """
    Remove outlier days from the dataframe
    """
    rows = data.shape[0]                # Number of rows in the dataframe
    rng = np.random.RandomState(42)     # Make results reproducible

    temp_data = data.drop(columns=['Oper Day', 'Interval Ending'])
    classifier = IsolationForest(
        max_samples = rows,
        contamination = fraction,
        random_state = rng)
    classifier.fit(temp_data)                # Fit the random forrest classifier

    labels = 0.5 * classifier.predict(temp_data) + 0.5
    return data[labels == 1]              # Return the data without outliers


import os

if os.path.exists('ercot.csv'):
    ercot_df = pd.read_csv('ercot.csv')
else:
    ercot_df = build_data(2024, 5, 11)
    # ercot_df = build_data(2024, 11, 11)