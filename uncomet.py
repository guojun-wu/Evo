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
        }

        model_info = models_info[metric]
        local_files_only = os.path.exists(cache_dir + model_info['subdir'])
        model_path = download_model(model_info['model_name'], cache_dir, local_files_only=local_files_only)
        self.model = load_from_checkpoint(model_path)
        self.test_mode = test_mode
        print("Model cache directory:", model_path)

    def score(self, src_lines, ref_lines, hyp_lines):
        # transform the lines into the format expected by COMET
        data = []
        for src, ref, hyp in zip(src_lines, ref_lines, hyp_lines):
            data.append({
                "src": src,
                "mt": hyp,
                "ref": ref
            })
        if self.test_mode:
            data = data[:2]

        model_output = self.model.predict(data, batch_size=16, gpus=1)
        return model_output.scores