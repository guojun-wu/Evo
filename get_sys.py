import pandas as pd
import numpy as np
import argparse
from evaluation.SETTINGS import *
import os

def get_score(path, lp, metric):
    sys_df = pd.DataFrame()
    file_path = f"{path}/{metric}/{lp}.csv"
    df = pd.read_csv(file_path, sep=',')

    for col in df.columns:
        new_row = pd.DataFrame({'date': [col], lp: [df[col].mean()]})
        sys_df = pd.concat([sys_df, new_row])
    return sys_df

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default='result', help='path')

    args = parser.parse_args()
    path = args.path

    for metric in metrics:
        # check if the metric folder exists
        if not os.path.exists(f"{path}/{metric}"):
            continue
        
        sys_df = pd.DataFrame({'date': []})
        for lp in lps:
            tmp_df = get_score(path, lp, metric)
            sys_df = pd.merge(sys_df, tmp_df, on='date', how='outer')
            
        # change the format of date from February-16-2024 to 2024-02-16
        sys_df['date'] = pd.to_datetime(sys_df['date']).dt.strftime('%Y-%m-%d')
        # sort the date
        sys_df = sys_df.sort_values(by='date')
        sys_df.to_csv(f"{path}/sys_{metric}.csv", index=False)

if __name__ == "__main__":
    main()