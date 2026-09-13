Quickstart
------------------------------

Clone the repository and download the checkpoint
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This example uses the TissueNet checkpoint from Zenodo. See :doc:`downloads`
for all resources, command-line alternatives, Python downloads, and licenses.

.. code-block:: bash

    git clone https://github.com/maxpmx/CelloType.git
    cd CelloType

.. code-block:: bash

    python download.py tissuenet_model_0019999.pth

This saves the verified checkpoint to ``models/``. The example image is already
included under ``data/example/``, so no dataset ZIP is needed. You can also
download the checkpoint from Python, running in the repository root:

.. code-block:: python

    from download import download_asset
    model_path = download_asset("tissuenet_model_0019999.pth", output_root=".")

The existing ``sh models/download.sh`` command also downloads this default checkpoint.

Prepare the input images
~~~~~~~~~~~~~~~~~~~~~~~~~

Convert the input images into an RGB format where the blue channel represents the nuclear channel, the green channel corresponds to the membrane channel.

.. image:: ../../data/example/example_tissuenet.png
    :width: 250px
    :alt: drawing

Inference the cell segmentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from skimage import io
    from cellotype.predict import CelloTypePredictor

    img = io.imread('data/example/example_tissuenet.png') # [H, W, 3]

    model = CelloTypePredictor(model_path='./models/tissuenet_model_0019999.pth',
      confidence_thresh=0.3, 
      max_det=1000, 
      device='cuda', 
      config_path='./configs/maskdino_R50_bs16_50ep_4s_dowsample1_2048.yaml')

    mask = model.predict(img) # [H, W]
