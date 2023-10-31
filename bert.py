from bert_score import BERTScorer

class Bert_score():
    def __init__(self, tgt_lang, test_mode=False):
        self.scorer = BERTScorer(lang=tgt_lang, rescale_with_baseline=True)
        self.test_mode = test_mode

    def score(self, ref_lines, hyp_lines):
        if self.test_mode:
            ref_lines = ref_lines[:2]
            hyp_lines = hyp_lines[:2]
        P, R, F1 = self.scorer.score(hyp_lines, ref_lines)
        sentence_score = F1.tolist()
        return sentence_score