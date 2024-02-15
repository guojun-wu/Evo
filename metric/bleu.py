from sacrebleu.metrics import BLEU, CHRF

class Sacrebleu:
    def __init__(self, metric, tgt_lang, test_mode=False):
        self.metric = metric
        self.tgt_lang = tgt_lang
        self.test_mode = test_mode
        if self.metric == 'bleu':
            self.scorer = BLEU(trg_lang=self.tgt_lang, effective_order=True)
        elif self.metric == 'chrf':
            self.scorer = CHRF()
        else:
            raise NotImplementedError
        
    def score(self, src_lines, ref_lines, hyp_lines):
        if self.test_mode:
            ref_lines = ref_lines[:2]
            hyp_lines = hyp_lines[:2]

        sentence_score = []

        for ref, hyp in zip(ref_lines, hyp_lines):
            result = self.scorer.sentence_score(ref, [hyp])
            sentence_score.append(result.score)
        return sentence_score
    