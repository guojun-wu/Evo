import pandas as pd
import argparse 
from metric.bertscore import BERTScore
from metric.comet import COMET
import os

def set_scorer(metric, tgt_lang, test_mode=False):
    if metric == 'bert':
        scorer = BERTScore(tgt_lang, test_mode=test_mode)
    elif metric in ['comet22', 'unite', 'comet20', 'cometkiwi', 'mscomet22qe']:
        scorer = COMET(metric, test_mode=test_mode)
    else:
        raise NotImplementedError
    return scorer

def get_score(scorer, src_lang, tgt_lang, metric, data_path, output_path):
    df = pd.read_csv(f'{data_path}/{src_lang}-{tgt_lang}.csv')
    source = df['source'].tolist()
    target = df['target'].tolist()
    score_df = pd.DataFrame()

    for date in df.iloc[:, 2:]:
        sys_output = df[date].tolist()
        sentence_score = scorer.score(source, target, sys_output)
        score_df[date] = sentence_score
    
    if not os.path.exists(f'{output_path}/{metric}'):
        os.makedirs(f'{output_path}/{metric}')
    score_df.to_csv(f'{output_path}/{metric}/{src_lang}-{tgt_lang}.csv', index=False)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--metric', type=str, default='bert', help='metric to use')
    parser.add_argument('--data_path', type=str, default='data_v2', help='data path')
    parser.add_argument('--output_path', type=str, default='result_v2', help='output path')
    parser.add_argument('--test', action='store_true', help='test mode')
    args = parser.parse_args()

    languages = ['en', 'de', 'it', 'zh']

    if args.metric != 'bert':
        scorer = set_scorer(args.metric, None, args.test)

    for tgt_lang in languages:
        if args.metric == 'bert':
            scorer = set_scorer(args.metric, tgt_lang, args.test)

        for src_lang in languages:
            if tgt_lang == src_lang:
                continue
            print(f'{src_lang} to {tgt_lang}')
            get_score(scorer, src_lang, tgt_lang, args.metric, args.data_path, args.output_path)
            
if __name__ == "__main__":
    main()