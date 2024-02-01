metrics = ['mscomet22qe','comet22', 'unite', 'comet20', 'cometkiwi', 'bert', 'bleu', 'chrf']

corpus_score_path = 'result/corpus_'

lps = ['en-de',  'it-de', 'zh-de',
        'de-en', 'it-en', 'zh-en',
        'de-it', 'en-it', 'zh-it',
         'de-zh', 'en-zh', 'it-zh']
        # ['en-de', 'es-de', 'it-de', 'zh-de',
        # 'de-en', 'es-en', 'it-en', 'zh-en',
        # 'de-it', 'en-it', 'es-it', 'zh-it',
        # 'de-zh', 'en-zh', 'es-zh', 'it-zh']
    
metric_dict = {'mscomet22qe': "MS-COMET-22-QE",'comet22': 'COMET-22', 'unite': 'UniTE', 
                'comet20': 'COMET-20', 'cometkiwi': 'COMET-Kiwi', 
                'bert': 'BERTScore', 'bleu': 'BLEU', 'chrf': 'chrF'}
            
colors = {'mscomet22qe': '#226646', 'comet22': '#9F05C5', 'bert': '#660C16', 'unite': '#CC2732',
        'comet20': '#9570DD', 'cometkiwi': '#90C825', 'bleu': '#008EF1', 'chrf': '#E6B111', 'vote': '#000000'}

into_de = ['en-de', 'it-de', 'zh-de']
into_en = ['de-en',  'it-en', 'zh-en']
into_it = ['de-it',  'en-it',  'zh-it']
into_zh = ['de-zh',  'en-zh',  'it-zh']
from_de = ['de-en',  'de-it', 'de-zh']
from_en = ['en-de',  'en-it', 'en-zh']
from_es = ['es-de', 'es-en', 'es-it', 'es-zh']
from_it = ['it-de', 'it-en', 'it-zh']
from_zh = ['zh-de', 'zh-en', 'zh-it']
all_4 = ['en-de',  'it-de', 'zh-de',
        'de-en', 'it-en', 'zh-en',
        'de-it', 'en-it', 'zh-it',
        'de-zh', 'en-zh', 'it-zh']
subsets = {'all': all_4, 'into_en': into_en, 'from_en': from_en, 'into_de': into_de, 'from_de': from_de,'into_it': into_it, 
        'from_it': from_it, 'into_zh': into_zh, 'from_zh': from_zh}

subsets_dict = {'all': 'All', 'into_en': 'Into EN', 'from_en': 'From EN', 'into_de': 'Into DE', 'from_de': 'From DE',
        'into_it': 'Into IT', 'from_it': 'From IT', 'into_zh': 'Into ZH', 'from_zh': 'From ZH', 'from_es': 'From ES'}