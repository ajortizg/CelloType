
<div align="center">    

# CelloType   
  
</div>

# Description   
CelloType [(Nature Methods 2024)](https://www.nature.com/articles/s41592-024-02513-1) is an end-to-end Transformer-based method for automated cell/nucleus segmentation and cell-type classification.  
[[Documentation]](https://cellotype.readthedocs.io/)

![overview](figures/overview.png)

## Feature Highlights:
- Improved Precision: For both segmentation and classification
- Wide Applicability: Various types of images  (fluorescent, brighfield, natural)
- Multi-scale: Capable of classifying diverse cell types and microanatomical structures

![example](figures/codex_example.png)

Our codes are based on open-source projects [Detectron2](https://github.com/facebookresearch/detectron2), [Mask DINO](https://github.com/IDEA-Research/MaskDINO).

## Installation
First, install dependencies 
- Linux with Python = 3.8 
- Detectron2: follow [Detectron2](https://detectron2.readthedocs.io/en/latest/tutorials/install.html) installation instructions. 

```bash
# create conda environment
conda create --name cellotype python=3.8
conda activate cellotype
# install pytorch and detectron2
conda install pytorch==1.9.0 torchvision==0.10.0 cudatoolkit=11.1 -c pytorch -c nvidia
python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'
# (add --user if you don't have permission)

# Compile Deformable-DETR CUDA operators
git clone https://github.com/fundamentalvision/Deformable-DETR.git
cd Deformable-DETR
cd ./models/ops
sh ./make.sh

# clone and install the project   
pip install cellotype
```

## Model weights and example datasets

The pretrained weights and processed example datasets are archived on
[Zenodo (version 1.0.0)](https://doi.org/10.5281/zenodo.22736357).
Files have stable version-specific links and SHA-256 checksums. Downloads need
only Python 3.8 or later; no GPU, CelloType installation, Zenodo login, or API
token is required. Start in the cloned repository root:

```bash
git clone https://github.com/maxpmx/CelloType.git
cd CelloType
```

From the command line:

```bash
# List available files without downloading
python download.py --list

# Download the TissueNet checkpoint (default; about 2.68 GB)
python download.py

# Download a matching checkpoint and dataset
python download.py xenium_model_0001499.pth example_xenium.zip
python -m zipfile -e data/example_xenium.zip data

# Download all five checkpoints and all three dataset ZIPs (19.14 GB)
python download.py --all
```

The downloader uses Python's standard library, verifies SHA-256 checksums, and
places checkpoints in `models/` and dataset archives in `data/`. Rerun the same
command to resume an interrupted transfer. Use `--output-root /path/to/CelloType`
to choose another destination. ZIPs must be extracted separately.

From Python or a notebook started in the repository root, use the same verified
downloader and the returned path:

```python
from download import download_asset

model_path = download_asset("tissuenet_model_0019999.pth", output_root=".")
# Use str(model_path) as CelloTypePredictor's model_path.
```

| Example | Checkpoint | Processed dataset |
| --- | --- | --- |
| TissueNet segmentation | `tissuenet_model_0019999.pth` | `example_tissuenet.zip` |
| CRC CODEX segmentation and classification | `crc_model_0005999.pth` | `example_codex_crc.zip` |
| Xenium segmentation | `xenium_model_0001499.pth` | `example_xenium.zip` |

The archive also includes `cellpose_model_0001999.pth` and the upstream MaskDINO
initialization checkpoint used by the training tutorials. See the
[complete download guide](https://cellotype.readthedocs.io/en/latest/downloads.html)
for all eight filenames, sizes, direct links, standalone-script setup, `curl`/`wget`
commands, and Python dataset extraction. The small images in `data/example/`
are already included in GitHub; the inference notebooks do not require a dataset ZIP.

Read the [file-specific licenses and attribution](https://zenodo.org/records/22736357/files/LICENSES_AND_ATTRIBUTION.txt).
The TissueNet example data retain their noncommercial academic-use license;
CRC/Xenium example data use CC BY 4.0, and checkpoints use Apache 2.0.

# Quick started

Clone the repository:

```bash
git clone https://github.com/maxpmx/CelloType.git
cd CelloType
```

Download the TissueNet checkpoint for this example:

```bash
python download.py tissuenet_model_0019999.pth
```

The existing `sh models/download.sh` command also works and accepts the same
filenames and options. See [model weights and example datasets](#model-weights-and-example-datasets)
for other resources and Python usage.

```python
from skimage import io
from cellotype.predict import CelloTypePredictor

img = io.imread('data/example/example_tissuenet.png') # [H, W, 3]

model = CelloTypePredictor(model_path='./models/tissuenet_model_0019999.pth',
  confidence_thresh=0.3, 
  max_det=1000, 
  device='cuda', 
  config_path='./configs/maskdino_R50_bs16_50ep_4s_dowsample1_2048.yaml')

mask = model.predict(img) # [H, W]
```

# Documentation
The documentation is available at [CelloType](https://cellotype.readthedocs.io/)


### Citation   
```
@article{pang2024cellotype,
  title={CelloType: A Unified Model for Segmentation and Classification of Tissue Images},
  author={Pang, Minxing and Roy, Tarun Kanti and Wu, Xiaodong and Tan, Kai},
  journal={Nature Methods},
  year={2024}
}
```
### Acknowledgement
Many thanks to these projects
- [Detectron2](https://github.com/facebookresearch/detectron2)
- [Mask DINO](https://github.com/IDEA-Research/MaskDINO)
