# Dataset
save the masks and images as .png in the following folder structure: copy them from the refining_dataset subfolders [`corrected_masks`](../../refining_dataset/corrected_masks/) and [`corrected_outputs`](../../refining_dataset/corrected_outputs/).

The process up until now was for a single class. If you want the model to detect multiple classes, repeat the masking and refining process up until now for as many classes as you want and save them in subfolders.

```
dataset/   #Primary data folder for the project
├── input/           #All input data is stored here. 
│   ├── train_images/
│   │   ├── image01.png
│   │   ├── image02.png
│   │   └── ...
│   ├── train_masks/        #All binary masks organized in respective sub-directories.
│   │   ├── class1/
│   │   │   ├── image01.png
│   │   │   ├── image02.png
│   │   │   └── ...
│   │   ├── class2/
│   │   │   ├── image01.png
│   │   │   ├── image02.png
│   │   │   └── ...
│   ├── val_images/         #Validation images
│   │   ├── image01.png
│   │   ├── image02.png
│   │   └── ...
│   ├── val_masks/          #Validation masks organized in respective sub-directories.
│   │   ├── class1/
│   │   │   ├── image01.png
│   │   │   ├── image02.png
│   │   │   └── ...
│   │   ├── class2/
│   │   │   ├── image01.png
│   │   │   ├── image02.png
│   │   │   └── ...
```