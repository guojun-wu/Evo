from bert_score import BERTScorer
import torch

class BERTScore():
    def __init__(self, tgt_lang, test_mode=False):
        self.scorer = BERTScorer(lang=tgt_lang, rescale_with_baseline=True, device=torch.device('cuda'))
        self.test_mode = test_mode

    def score(self, src_lines, ref_lines, hyp_lines):
        if self.test_mode:
            ref_lines = ref_lines[:2]
            hyp_lines = hyp_lines[:2]
        P, R, F1 = self.scorer.score(hyp_lines, ref_lines)
        sentence_score = F1.tolist()
        return sentence_score