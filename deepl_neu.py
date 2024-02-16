import pandas as pd
import argparse 
from metric.bertscore import BERTScore
from metric.uncomet import COMET
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', type=str, default='en', help='source language')
    parser.add_argument('-t', '--target', type=str, default='de', help='target language')
    parser.add_argument('--test', action='store_true', help='test mode')

    args = parser.parse_args()

    src_lang = args.source
    tgt_lang = args.target
    test_mode = args.test
    df = pd.read_csv(f'evo_data/{src_lang}-{tgt_lang}.csv')
    source = df['source'].tolist()
    target = []
    deepl_path = f"deepl/{src_lang}_{tgt_lang}.txt"
    with open(deepl_path, 'r', encoding='utf-8') as f:
        target = f.readlines()

    # metrics = ['comet22', 'unite', 'comet20']
    metrics = ['bert'] 

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
        if not os.path.exists(f'deepl/{metric}'):
            os.makedirs(f'deepl/{metric}')
        score_df.to_csv(f'deepl/{metric}/{src_lang}-{tgt_lang}.csv', index=False)

if __name__ == "__main__":
    main()
    
        