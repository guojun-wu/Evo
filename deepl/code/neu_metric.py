import pandas as pd
import argparse 
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))

if project_root not in sys.path:
    sys.path.append(project_root)
from metric.bertscore import BERTScore
from metric.uncomet import COMET
import os
def get_sys(df):
    sys_df = pd.DataFrame()

    for col in df.columns:
        new_row = pd.DataFrame({'date': [col], lp: [df[col].mean()]})
        sys_df = pd.concat([sys_df, new_row])
    
    sys_df['date'] = pd.to_datetime(sys_df['date']).dt.strftime('%Y-%m-%d')
    return sys_df
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', type=str, default='en', help='source language')
    parser.add_argument('-t', '--target', type=str, default='de', help='target language')
    parser.add_argument('-p','--data_path', type=str, default='evo_data', help='data path')
    parser.add_argument('--test', action='store_true', help='test mode')

    args = parser.parse_args()

    src_lang = args.source
    tgt_lang = args.target
    test_mode = args.test
    data_path = args.data_path

    df = pd.read_csv(f'{data_path}/{src_lang}-{tgt_lang}.csv')
    source = df['source'].tolist()
    target = []
    deepl_path = f"deepl/data/{src_lang}_{tgt_lang}.txt"
    with open(deepl_path, 'r', encoding='utf-8') as f:
        target = f.readlines()

    metrics = ['comet22', 'unite', 'comet20', 'cometkiwi', 'mscomet22qe', 'bert']

    for metric in metrics:
        if metric != 'bert':
            scorer = COMET(metric, test_mode=test_mode)
        else:
            scorer = BERTScore(tgt_lang, test_mode=test_mode)

        score_df = pd.DataFrame()
        for date in df.iloc[:, 2:]:
            sys_output = df[date].tolist()
            sentence_score = scorer.score(source, target, sys_output)
            score_df[date] = sentence_score
        if not os.path.exists(f'deepl/result/{metric}'):
            os.makedirs(f'deepl/result/{metric}')
        score_df.to_csv(f'deepl/result/{metric}/{src_lang}-{tgt_lang}_v2.csv', index=False)

        sys_df = get_sys(score_df)
        sys_df.to_csv(f'deepl/{metric}/sys_{src_lang}-{tgt_lang}_v2.csv', index=False)

if __name__ == "__main__":
    main()
    
        