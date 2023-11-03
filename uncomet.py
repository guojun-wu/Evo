from comet import download_model, load_from_checkpoint
import torch

class COMET:
    def __init__(self, test_mode=False):
        model_path = download_model("Unbabel/wmt22-comet-da", "/home/ec255/ec255/guojun/.cache/huggingface/hub/")
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

        #4984772