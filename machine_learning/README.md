# Machine Learning Workflow for YOLOv8 Segmentation

This repository is the final step in our workflow to train a YOLOv8 segmentation model. We prepare the dataset and then train the model.



## Dataset

It is the responsibility of the user to separate the images and masks we created in the previous steps into training and validation sets. Please refer to the [README](./dataset/input/README.md) of the dataset folder for further details on the structure. Here is a brief summary:

- `train_images/`: Contains the training images used to train the YOLOv8 segmentation model.
- `train_masks/`: Contains the masks (labels) for the corresponding training images. Each class needs its own subfolder in this folder.
- `val_images/`: Contains the validation images used to evaluate the model's performance.
- `val_masks/`: Contains the masks (labels) for the corresponding validation images. Each class needs its own subfolder in this folder.

### Dataset Preparation

The [`dataset_construction.ipynb`](./dataset_construction.ipynb) notebook is responsible for preparing and organizing the dataset. This notebook will load images and masks, ensuring that they are correctly paired for both training and validation. It will create a new folder `dataset/yolo_dataset/` from where the training scripts will take the data.

To run the notebook, open it in Jupyter or any Python environment that supports notebooks, and follow the instructions to create your dataset.

## Model Training

Once the dataset is prepared, the [`yolo.ipynb`](./yolo.ipynb) notebook can be used to train the YOLOv8 segmentation model.

### YOLOv8 Training Steps

1. **Load the Dataset**: The model will load the images and masks from the [`dataset/input/`](./dataset/input/) directory.
2. **Configure the Model**: Adjust model parameters such as the size of the pretrained yolov8 model, learning rate, epochs, and batch size.
3. **Train the Model**: Run the training process. The model will save checkpoints and evaluation results to `dataset/yolo_dataset/results`.
4. **Evaluate the Model**: After training, the model can be evaluated on the validation dataset to check its performance.
5. **Inference**: The last cells in the notebook are for applying the segmentation model to images from outside the dataset.

To train the model, run the [`yolo.ipynb`](./yolo.ipynb) notebook after ensuring that the dataset is correctly set up.

## Requirements

- Python 3.x
- Jupyter Notebook or Jupyter Lab
- Required Python packages (install via `pip`):
  - `ultralytics`
  - `numpy`
  - `opencv-python`
  - `torch`
  - `matplotlib`

You can install all dependencies by running the following command:

```bash
pip install ultralytics numpy opencv-python torch matplotlib
```

If you run into version conflicts please refer to the [`requirements.txt`](../requirements.txt) in the parent folder.

## Usage

1. **Prepare the dataset** by running the [`dataset_construction.ipynb`](./dataset_construction.ipynb) notebook.
2. **Train the model** by running the [`yolo.ipynb`](./yolo.ipynb) notebook.
3. Monitor the training process and evaluate the model's performance.

## Acknowledgements

This workflow leverages the Ultralytics YOLOv8 model for segmentation tasks.

Much of the code, especially in the [`dataset_construction.ipynb`](./dataset_construction.ipynb) was taken from [DigitalSreeni](https://www.youtube.com/watch?v=ytlhMAF6ok0) and adapted to our purposes.