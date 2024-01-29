from comet import download_model, load_from_checkpoint
import os

class COMET:
    def __init__(self, metric, test_mode=False):
        cache_dir = "/work/ec255/ec255/guojun/.cache/huggingface/hub/"
        models_info = {
            'comet22': {
                'model_name': 'Unbabel/wmt22-comet-da',
                'subdir': 'models--Unbabel--wmt22-comet-da',
            },
            'unite': {
                'model_name': 'Unbabel/unite-mup',
                'subdir': 'models--Unbabel--unite-mup',
            },
            'comet20': {
                'model_name': 'Unbabel/wmt20-comet-da',
                'subdir': 'models--Unbabel--wmt20-comet-da',
            },
            'cometkiwi': {
                'model_name': 'Unbabel/wmt22-cometkiwi-da',
                'subdir': 'models--Unbabel--wmt22-cometkiwi-da',
            },
        }
        if metric in models_info:
            model_info = models_info[metric]
            local_files_only = os.path.exists(cache_dir + model_info['subdir'])
            checkpoint_path = download_model(model_info['model_name'], cache_dir, local_files_only=local_files_only)
        elif metric == 'mscomet22qe':
            checkpoint_path = "checkpoints/MS-COMET-QE-22/model/MS-COMET-QE-22.ckpt"

        self.metric = metric
        self.model = load_from_checkpoint(checkpoint_path)
        self.test_mode = test_mode
        print("Model cache directory:", checkpoint_path)

    def score(self, src_lines, ref_lines, hyp_lines):
        # transform the lines into the format expected by COMET
        data = []
        for src, ref, hyp in zip(src_lines, ref_lines, hyp_lines):
            data.append({
                "src": src,
                "mt": hyp,
                "ref": ref
            })

        if self.metric in ['cometkiwi', 'mscomet22qe']:
            # COMET-Kiwi requires only src and mt
            data = [{"src": d["src"], "mt": d["mt"]} for d in data]
        if self.test_mode:
            data = data[:2]

        model_output = self.model.predict(data, batch_size=16, gpus=1)
        return model_output.scores