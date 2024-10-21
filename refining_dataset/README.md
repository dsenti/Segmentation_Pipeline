# Refining the Dataset

This folder contains tools and scripts designed to help the user correct the rough masks which we obtained in the first step of our pipeline. 

## Contents

- **`input/`**: This subfolder holds the input images that will be processed. Make sure to place all your image files here. Contrary to the input of our rough_mask folder which had to only be a representation of the distribution of our data, here we want all of the data.
- **`GrabCutCallable.py`**: This file is used by the other code and the user doesn't have to run it explicitly.
- **`GrabCutCorrections.py`**: Script used to have the user draw into the generated masks and correct them.
- **`GrabCutFolder.py`**: Provides code to apply the parameters to the whole input folder before running `GrabCutCorrections.py` and correcting the images manually.
- **`parameters.py`**: This file should contain the parameters which we got from the [`rough_mask.ipynb`](../rough_mask/rough_mask.ipynb) and has to be manually overwritten.
  
The processed outputs will be saved in automatically generated subfolders for further inspection and refinement.

## Installation

To utilize these scripts, ensure you have the following dependencies installed:

```bash
pip install numpy matplotlib opencv-python scikit-image ipywidgets
```
Refer to the [`requirements.txt`](../requirements.txt) file in the parent folder for version details if conflicts arise.

## Usage

1. Place your input images in the [`input`](./input/) folder.
2. Replace the parameters in [`parameters.py`](./parameters.py) with the ones we got from the [`rough_mask.ipynb`](../rough_mask/rough_mask.ipynb). The folder paths should be left the same.
3. Run [`GrabCutFolder.py`](./GrabCutFolder.py) to apply the rough masks to all the input data. The output will be saved in the folders `masks/`, `output_figures/` and `output_images/` (automatically created upon running the script).
4. Now run [`GrabCutCorrections.py`](./GrabCutCorrections.py) which will open an interactive window where you can paint over mistakes in the segmentation to refine the dataset. These results will in return be saved in the folders `corrected_masks/` and `corrected_outputs/` (folders are again created automatically). The commands for this interactive window are described below. Press the `i` key on your keyboard to revisit the commands.

### Keyboard Commands for [`GrabCutCorrections.py`](./GrabCutCorrections.py)

In `GrabCutCorrections.py`, several key events are implemented to control the segmentation-refinement process interactively. Below is a summary of the available commands and their functions:

- **Spacebar**:  
  Applies the GrabCut algorithm. It might take a few seconds depending on the performance of your machine. You will see the result after it has completed to further undertake refinements.

- **Tab**:  
  Toggles between adding to or removing from the selection mask. You can also see the current mode in the upper-left corner.

- **Number Keys (0-9)**:  
  Adjusts the brush radius used for selecting parts of the image. The brush size is increased based on the number key pressed (e.g., pressing '1' results in a smaller brush, while '9' results in a larger one).

- **Backspace or Ctrl+Z or Delete**:  
  Resets the mask display to the initial state. This is useful for undoing changes.

- **Enter**:
  Applies the GrabCut algorithm with the current mask and saves the image and the mask. This is typically the last step for a given image, the next image will be loaded.

- **Information Window ('i')**:  
  Press 'i' to display an information window that provides details about the current segmentation or available commands.

- **Esc**:  
  Exits the application. All windows are closed, and the script terminates.
