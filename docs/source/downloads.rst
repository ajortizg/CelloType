Model weights and example datasets
==================================

The pretrained checkpoints and processed example datasets are archived on
`Zenodo, version 1.0.0 <https://doi.org/10.5281/zenodo.22736357>`_.
The archive contains five checkpoints and three dataset ZIPs (19.14 GB).
Public downloads require neither a Zenodo account nor an API token.

Download from the command line
------------------------------

Only Python 3.8 or later is needed to download files; the downloader does not
import CelloType or require its machine-learning dependencies. Clone the
repository and enter its root directory first:

.. code-block:: bash

    git clone https://github.com/maxpmx/CelloType.git
    cd CelloType

Then choose the files you need:

.. code-block:: bash

    # List filenames and sizes without downloading
    python download.py --list

    # Download the default TissueNet checkpoint (2.68 GB)
    python download.py

    # Select individual resources
    python download.py xenium_model_0001499.pth example_xenium.zip

    # Download all eight assets (19.14 GB)
    python download.py --all

    # Save to a different repository or storage directory
    python download.py example_xenium.zip --output-root /path/to/CelloType

The downloader uses Python's standard library, verifies each SHA-256 checksum,
and reuses verified files. If a transfer is interrupted, rerun the same command
to resume its ``.part`` file when the server supports HTTP range requests.
Use ``--output-root PATH`` to choose a different destination.

Checkpoints are saved under ``models/`` and archives under ``data/``. Extract
the relevant ZIP from the repository root (replace the filename for other datasets):

.. code-block:: bash

    python -m zipfile -e data/example_xenium.zip data

This creates ``data/example_xenium/``. The other archives similarly create
``data/example_tissuenet/`` and ``data/example_codex_crc/``. Allow additional disk
space for the extracted data. The small images under ``data/example/`` are already
included in GitHub; the inference quickstart and notebooks only need a checkpoint.
The existing
``sh models/download.sh`` command invokes the same downloader and accepts the
same arguments.

Download only the script
~~~~~~~~~~~~~~~~~~~~~~~~~~

For a machine that only needs the resources, save the
`standalone download.py <https://raw.githubusercontent.com/maxpmx/CelloType/main/download.py>`_
in your chosen directory, or run:

.. code-block:: bash

    curl --fail --location --retry 5 --output download.py \
      "https://raw.githubusercontent.com/maxpmx/CelloType/main/download.py"
    python download.py --list
    python download.py example_xenium.zip

By default, files are placed in ``models/`` and ``data/`` beside ``download.py``.
An existing clone should be updated with ``git pull`` to obtain the downloader.
``pip install cellotype`` alone does not provide this repository-level script.

Download from Python or a notebook
------------------------------------

Start Python in the directory containing ``download.py``. Both checkpoint and
dataset downloads use the same function, including checksum verification,
retries, and reuse of complete files:

.. code-block:: python

    from download import download_asset

    model_path = download_asset("xenium_model_0001499.pth", output_root=".")
    archive_path = download_asset("example_xenium.zip", output_root=".")
    print(model_path)  # models/xenium_model_0001499.pth

    # Extract the downloaded example dataset when needed.
    from zipfile import ZipFile
    with ZipFile(archive_path) as archive:
        archive.extractall(archive_path.parent)

``download_asset`` returns a ``pathlib.Path``. Use ``str(model_path)`` when passing
it to a predictor. Set ``output_root`` to an absolute path when the files should
be saved elsewhere. In a notebook located inside the clone, see the setup cell
in either inference notebook for locating the repository root.

Choose resources for your task
------------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 45 30

   * - Task
     - Checkpoint
     - Example data
   * - TissueNet
     - ``tissuenet_model_0019999.pth``
     - ``example_tissuenet.zip``
   * - CRC CODEX
     - ``crc_model_0005999.pth``
     - ``example_codex_crc.zip``
   * - Xenium
     - ``xenium_model_0001499.pth``
     - ``example_xenium.zip``
   * - Additional
     - ``cellpose_model_0001999.pth``
     - Not included

The archive also contains the upstream MaskDINO Swin-L initialization file:
``maskdino_swinl_50ep_300q_hid2048_3sd1_instance_maskenhanced_mask52.3ap_box59.0ap.pth``.
The training scripts use this initialization file by default. Download it when
training with the supplied configuration; it is not needed for inference using
one of the trained CelloType checkpoints.

Direct downloads and checksums
------------------------------

Each link below downloads one file directly. Sizes use decimal GB/MB. The
full MaskDINO filename is shown above and in ``python download.py --list``.

.. list-table::
   :header-rows: 1
   :widths: 60 15 25

   * - File
     - Size
     - Save under
   * - `tissuenet_model_0019999.pth <https://zenodo.org/records/22736357/files/tissuenet_model_0019999.pth?download=1>`_
     - 2.68 GB
     - ``models/``
   * - `crc_model_0005999.pth <https://zenodo.org/records/22736357/files/crc_model_0005999.pth?download=1>`_
     - 2.68 GB
     - ``models/``
   * - `xenium_model_0001499.pth <https://zenodo.org/records/22736357/files/xenium_model_0001499.pth?download=1>`_
     - 2.68 GB
     - ``models/``
   * - `cellpose_model_0001999.pth <https://zenodo.org/records/22736357/files/cellpose_model_0001999.pth?download=1>`_
     - 2.68 GB
     - ``models/``
   * - `MaskDINO Swin-L initialization (.pth) <https://zenodo.org/records/22736357/files/maskdino_swinl_50ep_300q_hid2048_3sd1_instance_maskenhanced_mask52.3ap_box59.0ap.pth?download=1>`_
     - 895.42 MB
     - ``models/``
   * - `example_tissuenet.zip <https://zenodo.org/records/22736357/files/example_tissuenet.zip?download=1>`_
     - 1.45 GB
     - ``data/``
   * - `example_codex_crc.zip <https://zenodo.org/records/22736357/files/example_codex_crc.zip?download=1>`_
     - 5.71 GB
     - ``data/``
   * - `example_xenium.zip <https://zenodo.org/records/22736357/files/example_xenium.zip?download=1>`_
     - 359.15 MB
     - ``data/``

To download directly from a terminal without the Python script, choose either
``curl`` or ``wget``. Run from the repository root:

.. code-block:: bash

    mkdir -p models
    curl --fail --location --retry 5 --continue-at - \
      --output models/tissuenet_model_0019999.pth \
      "https://zenodo.org/records/22736357/files/tissuenet_model_0019999.pth?download=1"

.. code-block:: bash

    mkdir -p models
    wget --continue --tries=5 --output-document=models/tissuenet_model_0019999.pth \
      "https://zenodo.org/records/22736357/files/tissuenet_model_0019999.pth?download=1"

Use the dataset URL and a ``data/`` destination to download a ZIP directly.
Direct ``curl``/``wget`` transfers do not automatically verify checksums.
Running ``python download.py tissuenet_model_0019999.pth`` afterward verifies
the downloaded file and reuses it if correct; it downloads a replacement if
verification fails.

These links target the published
`record version <https://zenodo.org/records/22736357>`_ for reproducibility.
The `SHA256SUMS.txt file <https://zenodo.org/records/22736357/files/SHA256SUMS.txt>`_
contains hashes for all eight original resources.

If Zenodo returns a temporary 502, 503, or 504 error, the Python downloader retries
automatically. If it eventually exits, keep the ``.part`` file and rerun the same
command when service recovers. For an unknown filename, copy its exact spelling
from ``python download.py --list``. For ``No module named download`` or a missing
``download.py``, change to the cloned repository root or download the standalone
script as above.

Licenses and citation
---------------------

Read `LICENSES_AND_ATTRIBUTION.txt <https://zenodo.org/records/22736357/files/LICENSES_AND_ATTRIBUTION.txt>`_
alongside the files you download. The CelloType and MaskDINO checkpoints use
Apache 2.0. The CRC and Xenium example data use CC BY 4.0. The TissueNet example
data retain the upstream Modified Apache License for non-commercial academic
use. These licenses apply to specific files and are not interchangeable
licenses for the whole archive.

Cite the archive DOI, the
`CelloType paper <https://doi.org/10.1038/s41592-024-02513-1>`_, and the original
datasets/checkpoints used in your work. The attribution file includes original
sources, modification notices, full upstream license texts, and citations.
