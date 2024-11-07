from backend import ercot_data
from tovowpal import df_to_vw

def main():
    vw = df_to_vw(ercot_data['LMP'], 'LMP', tag_col='Oper Day')