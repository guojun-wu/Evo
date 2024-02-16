import pandas as pd
import argparse 
from metric.bertscore import BERTScore
from metric.uncomet import COMET
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', type=str, default='en', help='source language')
    parser.add_argument('-t', '--target', type=str, default='de', help='target language')

    args = parser.parse_args()

    src_lang = args.source
    tgt_lang = args.target
    df = pd.read_csv(f'evo_data/{src_lang}-{tgt_lang}.csv')
    source = df['source'].tolist()
    target = []
    deepl_path = f"deepl/{src_lang}_{tgt_lang}.txt"
    with open(deepl_path, 'r', encoding='utf-8') as f:
        target = f.readlines()

    metrics = ['bert', 'comet22', 'unite', 'comet20']

    for metric in metrics:
        if metric != 'bert':
            scorer = COMET(metric, test_mode=True)
        else:
            scorer = BERTScore(tgt_lang, test_mode=True)

        score_df = pd.DataFrame()
        for date in df.iloc[:, 2:]:
            sys_output = df[date].tolist()
            sentence_score = scorer.score(source, target, sys_output)
            score_df[date] = sentence_score
        if not os.path.exists(f'deepl/{metric}'):
            os.makedirs(f'deepl/{metric}')
        score_df.to_csv(f'deepl/{metric}/{src_lang}-{tgt_lang}.csv', index=False)

    
        