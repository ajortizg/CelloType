Cell Segmentation (Xenium Spatial Transcriptomics)
--------------------------------------------------

See :doc:`downloads` for command-line and Python downloads, checksums, and
file-specific licenses. All commands below run from the cloned repository root:

.. code-block:: bash

    git clone https://github.com/maxpmx/CelloType.git
    cd CelloType

Download data and pretrained model weights
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Download the processed data
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**IMPORTANT**: Note that the raw data is from `Xenium Human Lung Dataset <https://www.10xgenomics.com/datasets/preview-data-ffpe-human-lung-cancer-with-xenium-multimodal-cell-segmentation-1-standard>`_. This processed data is for demo purpose ONLY!

Download and extract the processed data with these commands. The downloader
creates ``data/`` and verifies the archive's SHA-256 checksum. A
`direct ZIP download <https://zenodo.org/records/22736357/files/example_xenium.zip?download=1>`__
is also available; save it under ``data/`` before extracting.

.. code-block:: bash

    python download.py example_xenium.zip
    python -m zipfile -e data/example_xenium.zip data

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

.. code-block:: bash

    python train_xenium.py --num-gpus 4

The parameters are optimized for 4\*A100 (40GB) environment, if your machine does not have enough GPU memory, you can reduce the batch size by changing the ``IMS_PER_BATCH`` in ``configs/Base-COCO-InstanceSegmentation.yaml``. For reference, the training take ~10 hours on 4\*A100 (40GB) environment.

Test model and visualize results
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Download our trained CelloType weights and run the test:

.. code-block:: bash

    python download.py xenium_model_0001499.pth

The file is saved as ``models/xenium_model_0001499.pth``. A
`direct trained-weight download <https://zenodo.org/records/22736357/files/xenium_model_0001499.pth?download=1>`__
is also available. The testing script expects the processed dataset extracted
in the first section.

.. code-block:: bash

    python test_xenium.py --num-gpus 1

The example prediction saved in the ``output/xenium`` folder.

.. image:: ../../output/xenium/0_pred.png
    :width: 250px
    :alt: drawing
