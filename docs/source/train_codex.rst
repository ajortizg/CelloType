Cell Annotation (Fluorescent Images)
------------------------------------

See :doc:`downloads` for command-line and Python downloads, checksums, and
file-specific licenses. All commands below run from the cloned repository root:

.. code-block:: bash

    git clone https://github.com/maxpmx/CelloType.git
    cd CelloType

Download data and pretrained model weights
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Download the processed data
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**IMPORTANT**: Note that the raw data is from `Garry P. Nolan Lab <https://doi.org/10.7937/tcia.2020.fqn0-0326>`_, this processed data is for demo purpose ONLY!

Download and extract the processed data with these commands. The downloader
creates ``data/`` and verifies the archive's SHA-256 checksum. A
`direct ZIP download <https://zenodo.org/records/22736357/files/example_codex_crc.zip?download=1>`__
is also available; save it under ``data/`` before extracting.

.. code-block:: bash

    python download.py example_codex_crc.zip
    python -m zipfile -e data/example_codex_crc.zip data

Download initialization weights for training
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The training script uses the COCO-pretrained MaskDINO checkpoint by default.
Download it to ``models/`` before training. Skip this step if you only want to
run the trained CelloType checkpoint in the testing section below.

.. code-block:: bash

    python download.py maskdino_swinl_50ep_300q_hid2048_3sd1_instance_maskenhanced_mask52.3ap_box59.0ap.pth

Alternatively, use the
`direct initialization-weight download <https://zenodo.org/records/22736357/files/maskdino_swinl_50ep_300q_hid2048_3sd1_instance_maskenhanced_mask52.3ap_box59.0ap.pth?download=1>`__.

Train model
~~~~~~~~~~~

Note: If you want to train the model using multi-channel images with a number of channels other than 3, you can modify the ``cfg.MODEL.IN_CHANS`` setting in the ``train_crc.py`` script.

.. code-block:: bash

    python train_crc.py --num-gpus 4

The parameters are optimized for 4\*A100 (40GB) environment, if your machine does not have enough GPU memory, you can reduce the batch size by changing the ``IMS_PER_BATCH`` in ``configs/Base-COCO-InstanceSegmentation.yaml``. For reference, the training takes ~12 hours on 4\*A100 (40GB) environment.

Test model and visualize results
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Download our trained CelloType weights and run the test:

.. code-block:: bash

    python download.py crc_model_0005999.pth

The file is saved as ``models/crc_model_0005999.pth``. A
`direct trained-weight download <https://zenodo.org/records/22736357/files/crc_model_0005999.pth?download=1>`__
is also available. The testing script expects the processed dataset extracted
in the first section.

.. code-block:: bash

    python test_crc.py --num-gpus 1

The example prediction saved in the ``output/codex`` folder.

.. image:: ../../output/codex/0_pred.png
    :width: 250px
    :alt: drawing
