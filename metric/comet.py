from comet import download_model, load_from_checkpoint
import os

class COMET:
    def __init__(self, metric, test_mode=False):
        model_info = {
            'comet22': 'Unbabel/wmt22-comet-da',
            'unite': 'Unbabel/unite-mup',
            'comet20': 'Unbabel/wmt20-comet-da',
            'cometkiwi': 'Unbabel/wmt22-cometkiwi-da',
        }
        if metric in models_info:
            checkpoint_path = download_model(model_info[metric])
        # the checkpoint for mscomet22qe should be downloaded from 
        elif metric == 'mscomet22qe':
            checkpoint_path = "checkpoints path for mscomet22qe"

        self.metric = metric
        self.model = load_from_checkpoint(checkpoint_path)
        self.test_mode = test_mode

    def score(self, src_lines, ref_lines, hyp_lines):
        # Transform the lines into the format expected by COMET
        data = []
        for src, ref, hyp in zip(src_lines, ref_lines, hyp_lines):
            data.append({
                "src": src,
                "mt": hyp,
                "ref": ref
            })

        if self.metric in ['cometkiwi', 'mscomet22qe']:
            # Only requires src and mt
            data = [{"src": d["src"], "mt": d["mt"]} for d in data]
        if self.test_mode:
            data = data[:2]

        model_output = self.model.predict(data, batch_size=16, gpus=1)
        return model_output.scores