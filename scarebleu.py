import pandas as pd
import sacrebleu
import os
import argparse 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str, default='data', help='data path')
    parser.add_argument('--output_path', type=str, default='result', help='output path')
    parser.add_argument('-m', '--metric', type=str, default='bleu', help='metric to use')
    args = parser.parse_args()
    languages = ['en', 'de', 'it', 'zh']

    metric = args.metric
    data_path = args.data_path
    output_path = args.output_path

    for src_lang in languages:
        for tgt_lang in languages:
            if tgt_lang == src_lang:
                continue
            print(f'{src_lang} to {tgt_lang}')
            df = pd.read_csv(f'{data_path}/{src_lang}-{tgt_lang}.csv')
            score_df = pd.DataFrame()

            for date in df.iloc[:, 2:]:
                sys_output = df[date].tolist()

                if metric == 'chrf':
                    sys_score = sacrebleu.corpus_chrf(sys_output, [df['target'].tolist()])
                else:
                    if tgt_lang == 'zh':
                        sys_score = sacrebleu.corpus_bleu(sys_output, [df['target'].tolist()], tokenize='zh')
                    else:
                        sys_score = sacrebleu.corpus_bleu(sys_output, [df['target'].tolist()])
            print(f"{metric} score for {date} is {sys_score.score}")
            score_df[date] = [sys_score.score]

            if not os.path.exists(f'{output_path}/{metric}'):
                os.makedirs(f'{output_path}/{metric}')
            score_df.to_csv(f'{output_path}/{metric}/{src_lang}-{tgt_lang}.csv', index=False)

if __name__ == "__main__":
    main()                    