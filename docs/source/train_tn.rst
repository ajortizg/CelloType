Cell Segmentation (Fluorescent Images)
--------------------------------------

See :doc:`downloads` for command-line and Python downloads, checksums, and
file-specific licenses. All commands below run from the cloned repository root:

.. code-block:: bash

    git clone https://github.com/maxpmx/CelloType.git
    cd CelloType

Download data and pretrained model weights
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Download the processed data
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**IMPORTANT**: Note that the raw data is from `TissueNet <https://datasets.deepcell.org/>`_, this processed data is for demo purpose ONLY!

Download and extract the processed data with these commands. The downloader
creates ``data/`` and verifies the archive's SHA-256 checksum. A
`direct ZIP download <https://zenodo.org/records/22736357/files/example_tissuenet.zip?download=1>`__
is also available; save it under ``data/`` before extracting.

.. code-block:: bash

    python download.py example_tissuenet.zip
    python -m zipfile -e data/example_tissuenet.zip data

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

Note: If you want to train the model using multi-channel images with a number of channels other than 3, you can modify the ``cfg.MODEL.IN_CHANS`` setting in the ``train_tissuenet.py`` script.

.. code-block:: bash

    python train_tissuenet.py --num-gpus 4

The parameters are optimized for 4\*A100 (40GB) environment, if your machine does not have enough GPU memory, you can reduce the batch size by changing the ``IMS_PER_BATCH`` in ``configs/Base-COCO-InstanceSegmentation.yaml``.

Test model and visualize results
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Download our trained CelloType weights and run the test:

.. code-block:: bash

    python download.py tissuenet_model_0019999.pth

The file is saved as ``models/tissuenet_model_0019999.pth``. A
`direct trained-weight download <https://zenodo.org/records/22736357/files/tissuenet_model_0019999.pth?download=1>`__
is also available. The testing script expects the processed dataset extracted
in the first section.

.. code-block:: bash

    python test_tissuenet.py --num-gpus 1

The example prediction saved in the ``output/tissuenet`` folder.

.. image:: ../../output/tissuenet/0_pred.png
    :width: 250px
    :alt: drawing
