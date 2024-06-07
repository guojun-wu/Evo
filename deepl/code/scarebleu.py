import pandas as pd
import sacrebleu
import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', type=str, default='en', help='source language')
    parser.add_argument('-t', '--target', type=str, default='de', help='target language')
    parser.add_argument('-p','--data_path', type=str, default='evo_data', help='data path')

    args = parser.parse_args()

    src_lang = args.source
    tgt_lang = args.target
    data_path = args.data_path

    df = pd.read_csv(f'{data_path}/{src_lang}-{tgt_lang}.csv')
    target = []
    deepl_path = f"deepl/data/{src_lang}_{tgt_lang}.txt"
    with open(deepl_path, 'r', encoding='utf-8') as f:
        target = f.readlines()

    metrics = ['chrf', 'bleu']

    for metric in metrics:
        score_list = []

        for date in df.iloc[:, 2:]:
            sys_output = df[date].tolist()
            if metric == 'chrf':
                sys_score = sacrebleu.corpus_chrf(sys_output, [target])
            else:
                if tgt_lang == 'zh':
                    sys_score = sacrebleu.corpus_bleu(sys_output, [target], tokenize='zh')
                else:
                    sys_score = sacrebleu.corpus_bleu(sys_output, [target])
                    
            score_list.append(sys_score.score)

        score_df = pd.DataFrame()
        score_df['date'] = df.columns[2:]
        score_df['score'] = score_list
        # reformat date from February-16-2024 to 2024-02-16
        score_df['date'] = pd.to_datetime(score_df['date']).dt.strftime('%Y-%m-%d')
        score_df = score_df.sort_values(by='date')
        if not os.path.exists(f'deepl/result/{metric}'):
                os.makedirs(f'deepl/result/{metric}')
        score_df.to_csv(f'deepl/result/{metric}/sys_{src_lang}-{tgt_lang}.csv', index=False)

if __name__ == "__main__":
    main()
    