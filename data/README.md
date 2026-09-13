# Example datasets

The processed example datasets are available in the
[CelloType Zenodo archive](https://doi.org/10.5281/zenodo.22736357).
Run the commands for your dataset from the repository root:

```bash
# TissueNet
python download.py example_tissuenet.zip
python -m zipfile -e data/example_tissuenet.zip data

# CRC CODEX
python download.py example_codex_crc.zip
python -m zipfile -e data/example_codex_crc.zip data

# Xenium
python download.py example_xenium.zip
python -m zipfile -e data/example_xenium.zip data
```

Downloads use only Python's standard library and verify SHA-256 checksums.
Rerun the same command to resume an interrupted transfer. Archives are saved in
`data/` and extract to `data/example_tissuenet/`, `data/example_codex_crc/`, or
`data/example_xenium/`. The small images in `data/example/` are included in GitHub
and are sufficient for the inference quickstart and notebooks.

From Python in the repository root:

```python
from download import download_asset
from zipfile import ZipFile

archive_path = download_asset("example_xenium.zip", output_root=".")
with ZipFile(archive_path) as archive:
    archive.extractall(archive_path.parent)
```

See the [download guide](https://cellotype.readthedocs.io/en/latest/downloads.html)
for matching model weights, file sizes, direct links, and `curl`/`wget` examples.
TissueNet example data retain the upstream license for non-commercial academic
use. CRC and Xenium example data use CC BY 4.0. Read the
[full licenses and attribution](https://zenodo.org/records/22736357/files/LICENSES_AND_ATTRIBUTION.txt).
For original raw datasets and preprocessing instructions, see [preprocess](../preprocess/README.md).
