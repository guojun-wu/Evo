import pandas as pd
import requests
import os

def translate_text(text, target_lang, src_lang, auth_key):
    url = 'https://api-free.deepl.com/v2/translate'
    headers = {
        'Authorization': f'DeepL-Auth-Key {auth_key}',
        'Content-Type': 'application/json',
    }
    data = {
        'text': [text],
        'target_lang': target_lang,
        'source_lang': src_lang,
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        translated_text = response.json()['translations'][0]['text']
        return translated_text
    else:
        return None

def translate_and_save(input_texts, output_file, target_lang, source_lang, auth_key):
    translations = []
    for idx, text in enumerate(input_texts):
        translation = translate_text(text, target_lang, source_lang, auth_key)
        if translation is not None:
            translations.append(translation)
        else:
            print(f"Error translating text at index {idx}. Please resume from here.")
            break
    if not os.path.exists(output_file):
        with open(output_file, 'w', encoding='utf-8'):
            pass

    with open(output_file, 'a', encoding='utf-8') as f:
        for translation in translations:
            f.write(translation + '\n')

data_path = 'evo_data'
src_lang = 'zh'
tgt_lang = 'en'
auth_key = '3acb081d-7e8c-4184-be27-1b4b9a075290:fx'

df = pd.read_csv(f'{data_path}/{src_lang}-{tgt_lang}.csv')
source = df['source'].tolist()

output_path = 'deepl'
output_file = f'{output_path}/{src_lang}_{tgt_lang}.txt'

translate_and_save(source, output_file, tgt_lang.upper(), src_lang.upper(), auth_key)

