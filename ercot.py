from pathlib import Path
import pandas as pd
from isodata.sessions import Session

ercot = Session('ercot_public')
ercot.authorize(username=creds['credentials']['ercot_public_api']['username'],
                password=creds['credentials']['ercot_public_api']['password'],
                primary_key=creds['credentials']['ercot_public_api']['primary_key'],
                auth_url=creds['credentials']['ercot_public_api']['auth_url'])

# Fetch 'SCED Shadow Prices and Binding Transmission Constraints'
emil = 'NP6-86-CD'

# Fetch the list of documents on the first page
report_list, count = ercot.fetch_listing(emil_id=emil, page=1)

# Fetch the first file and save it locally, the 2nd element
# in the tuple is the link to the report.
data_file = ercot.fetch_url(report_list[0][2], Path('path/to/save/report'))

# Do what you want with the data in the file from here.
# Beware of zips with multiple files, or data_files that 
# are just plain .csv files.  An example for NP6-86-CD data is:
df = pd.read_csv(data_file, compression='zip')
