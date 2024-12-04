from backend import get_ercot_df
from tovowpal import df_to_vw

def main():
    ercot_data = get_ercot_df()
    vw = df_to_vw(ercot_data['LMP'], 'LMP', tag_col='Oper Day')