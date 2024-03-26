import pandas as pd
import numpy as np
from SETTINGS import *

def get_score(lp, metric):
    sys_df = pd.DataFrame()
    seg_path = f"result_v2/{metric}/{lp}.csv"
    seg_df = pd.read_csv(seg_path, sep=',')

    for col in seg_df.columns:
        new_row = pd.DataFrame({'date': [col], lp: [seg_df[col].mean()]})
        sys_df = pd.concat([sys_df, new_row])
   
    return sys_df

def get_bleu_chrf(lp, metric):
    sys_df = pd.DataFrame()
    seg_path = f"result_v2/{metric}/{lp}.csv"
    seg_df = pd.read_csv(seg_path, sep=',')

    for col in seg_df.columns:
        new_row = pd.DataFrame({'date': [col], lp: [seg_df[col].mean()]})
        sys_df = pd.concat([sys_df, new_row])
   
    return sys_df

def main():

    for metric in metrics:
        if metric in ['bleu', 'chrf']:
            continue
        sys_df = pd.DataFrame({'date': []})
        for lp in lps:
            tmp_df = get_score(lp, metric)
            sys_df = pd.merge(sys_df, tmp_df, on='date', how='outer')
        # change the format of date from February-16-2024 to 2024-02-16
        sys_df['date'] = pd.to_datetime(sys_df['date']).dt.strftime('%Y-%m-%d')
        # sort the date
        sys_df = sys_df.sort_values(by='date')
        sys_df.to_csv(f"result_v2/sys_{metric}.csv", index=False)

    for metric in ['bleu', 'chrf']:
        sys_df = pd.DataFrame({'date': []})
        for lp in lps:
            tmp_df = get_bleu_chrf(lp, metric)
            sys_df = pd.merge(sys_df, tmp_df, on='date', how='outer')
        # change the format of date from February-16-2024 to 2024-02-16
        sys_df['date'] = pd.to_datetime(sys_df['date']).dt.strftime('%Y-%m-%d')
        # sort the date
        sys_df = sys_df.sort_values(by='date')
        sys_df.to_csv(f"result_v2/sys_{metric}.csv", index=False)

        
            
            

if __name__ == "__main__":
    main()