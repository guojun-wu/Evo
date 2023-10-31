import pandas as pd
import argparse 
from bert import Bert_score

def set_scorer(metric, tgt_lang, test_mode=False):
    if metric == 'bert':
        scorer = Bert_score(tgt_lang, test_mode=test_mode)
    else:
        raise NotImplementedError
    return scorer

def get_score(scorer, src_lang, tgt_lang):
    base_path = 'evo_data'
    output_path = 'result'
    df = pd.read_csv(f'{base_path}/{src_lang}-{tgt_lang}.csv')
    target = df['target'].tolist()
    score_df = pd.DataFrame()

    for date in df.iloc[:, 2:]:
        sys_output = df[date].tolist()
        sentence_score = scorer.score(target, sys_output)
        score_df[date] = sentence_score
        
    score_df.to_csv(f'{output_path}/bert_{src_lang}-{tgt_lang}.csv', index=False)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--metric', type=str, default='bert', help='metric to use')
    parser.add_argument('--test', action='store_true', help='test mode')
    args = parser.parse_args()

    languages = ['en', 'de', 'es', 'it', 'zh']

    for tgt_lang in languages:
        scorer = set_scorer(args.metric, tgt_lang, args.test)

        for src_lang in languages:
            if tgt_lang == src_lang:
                continue
            print(f'{src_lang} to {tgt_lang}')
            get_score(scorer, src_lang, tgt_lang)
            

if __name__ == "__main__":
    main()



