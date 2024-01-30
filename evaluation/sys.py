from SETTINGS import *
import pandas as pd
import numpy as np

def get_score(lp, metric):
    sys_df = pd.DataFrame()
    seg_path = f"result/{metric}/{lp}.csv"
    seg_df = pd.read_csv(seg_path, sep=',')

    for col in seg_df.columns:
        new_row = pd.DataFrame({'date': [col], lp: [seg_df[col].mean()]})
        sys_df = pd.concat([sys_df, new_row])
   
    return sys_df

def main():
    df = pd.DataFrame()
    
    # merge all the scores into one dataframe on date
    metric = 'comet22'
    df = get_score('en-es', 'mscomet22qe')
    for lp in lps:
        sys_df = get_score(lp, metric)
        df = pd.merge(df, sys_df, on='date', how='outer')
    df.to_csv(f"result/test_{metric}.csv", index=False)

if __name__ == "__main__":
    main()
        



        
    