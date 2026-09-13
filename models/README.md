# Pretrained model weights

All five checkpoints are available in the [CelloType Zenodo archive](https://doi.org/10.5281/zenodo.22736357).
From the repository root, run any of these commands (Python 3.8+ only):

```bash
python download.py --list
python download.py tissuenet_model_0019999.pth
python download.py crc_model_0005999.pth
python download.py xenium_model_0001499.pth
python download.py cellpose_model_0001999.pth
python download.py maskdino_swinl_50ep_300q_hid2048_3sd1_instance_maskenhanced_mask52.3ap_box59.0ap.pth
```

Choose the checkpoint needed by your example; each command verifies SHA-256 and
saves the file in this `models/` directory. Rerun the same command to resume an
interrupted transfer. Inference uses a trained TissueNet, CRC, or Xenium checkpoint;
the supplied training scripts use the MaskDINO initialization checkpoint.

The existing command also works from this directory:

```bash
sh download.sh                         # default TissueNet checkpoint
sh download.sh crc_model_0005999.pth    # choose another file
```

From Python in the repository root:

```python
from download import download_asset
model_path = download_asset("tissuenet_model_0019999.pth", output_root=".")
```

Use `str(model_path)` as the predictor's model path. See the
[download guide](https://cellotype.readthedocs.io/en/latest/downloads.html)
for direct links, sizes, `curl`/`wget`, dataset downloads, and licenses.
