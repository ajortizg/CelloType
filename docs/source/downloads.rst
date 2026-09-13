Model weights and example datasets
==================================

The pretrained checkpoints and processed example datasets are archived on
`Zenodo, version 1.0.0 <https://doi.org/10.5281/zenodo.22736357>`_.
The archive contains five checkpoints and three dataset ZIPs (19.14 GB).
Public downloads require neither a Zenodo account nor an API token.

Download with Python
--------------------

Run these commands from the CelloType repository root:

.. code-block:: bash

    # List filenames and sizes without downloading
    python download.py --list

    # Download the default TissueNet checkpoint (2.68 GB)
    python download.py

    # Select individual resources
    python download.py xenium_model_0001499.pth example_xenium.zip

    # Download all eight assets (19.14 GB)
    python download.py --all

The downloader uses Python's standard library, verifies each SHA-256 checksum,
and reuses verified files. If a transfer is interrupted, rerun the same command
to resume its ``.part`` file when the server supports HTTP range requests.
Use ``--output-root PATH`` to choose a different destination.

Checkpoints are saved under ``models/`` and archives under ``data/``. Extract
the relevant ZIP as shown in the training tutorial. The existing
``sh models/download.sh`` command invokes the same downloader and accepts the
same arguments.

Available resources
-------------------

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
   * - Cellpose benchmark
     - ``cellpose_model_0001999.pth``
     - Not included

The archive also contains the upstream MaskDINO Swin-L initialization file:
``maskdino_swinl_50ep_300q_hid2048_3sd1_instance_maskenhanced_mask52.3ap_box59.0ap.pth``.

Direct downloads and checksums
------------------------------

Individual file links are listed on the
`record page <https://zenodo.org/records/22736357>`_. For reproducible scripts,
use this version-specific record rather than a link that follows future versions.
The `SHA256SUMS.txt file <https://zenodo.org/records/22736357/files/SHA256SUMS.txt>`_
contains hashes for all eight original resources.

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
