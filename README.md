# Segmentation pipeline
This repository contains the workflow for developing and training machine learning models which solve segmentation tasks. The project is organized into three main sub-folders, each serving a distinct purpose in the pipeline.

## Workflow

### 1. [`rough_mask/`](./rough_mask/)
This sub-folder contains the code and instructions required to create a first very rudimentary segmentation. The goal here is not to have a nice result but to create an initialization which can be manually refined in the next step.

### 2. [`refining_dataset/`](./refining_dataset/)
Here we first apply the parameters defined in the previous step to all our data and then manually correct errors in our dataset. As we use a pretrained model and only fine-tune it to our needs, we have seen good performance with datasets of less thann 100 images, making this approach feasible. Of course, the better our rough masks are, the less corrections have to be applied.


### 3. [machine_learning/](./machine_learning/)

This folder holds the Python notebook used for training the YOLOv8 segmentation model. The training process is based on the dataset prepared in the previous step and includes:
- Changing our dataset from our `.png` files into the YOLOv8 format expected by the ultralytics model.
- Configuration of YOLOv8 parameters such as learning rate, batch size, and epochs.
- Running the training loop and evaluating the performance of the model on the validation set.


Please refer to the `README.md` files in the subfolders for detailed instructions, sticking to the order applied above.