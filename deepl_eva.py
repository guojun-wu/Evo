import pandas as pd
import sacrebleu

def main():
    src_lang = 'zh'
    tgt_lang = 'en'
    data_path = 'evo_data'

    df = pd.read_csv(f'{data_path}/{src_lang}-{tgt_lang}.csv')
    target = []
    deepl_path = f"deepl/{src_lang}_{tgt_lang}.txt"
    with open(deepl_path, 'r', encoding='utf-8') as f:
        target = f.readlines()

    score_list = []

    for date in df.iloc[:, 2:]:
        sys_output = df[date].tolist()
        sys_score = sacrebleu.corpus_chrf(sys_output, [target])
        print(f"chrf score for {date} is {sys_score.score}")
        score_list.append(sys_score.score)

    score_df = pd.DataFrame()
    score_df['date'] = df.columns[2:]
    score_df['score'] = score_list
    score_df.to_csv(f'deepl/chrf_{src_lang}-{tgt_lang}.csv', index=False)

if __name__ == "__main__":
    main()
    