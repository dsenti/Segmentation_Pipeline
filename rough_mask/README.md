# Rough Mask Creation

Welcome to the first step for creating a segmentation dataset on which we will fine tune our pretrained ML model. This folder contains code which helps the user select parameters for a first segmentation. The idea is not for this code to output perfectly segmented results but to use the output as a starting point which can then be further refined. 

The code detects specific colors (given by the user as different hues and intensities), and applies a rough segmentation using OpenCV's `grabCut` method. The output includes modified images where the background is darker in order to visualize the segmentation, the generated masks, and visual plots.


## Installation

To use this notebook, ensure you have the following Python packages installed:

```bash
pip install numpy matplotlib opencv-python scikit-image ipywidgets
```
If you run into issues, please refer to the version numbers in requirements.txt located in the parent folder.

## Usage

1. Place your input images in the [`representative_sample_input`](representative_sample_input/) folder. 
2. Run the notebook to process the images. You can adjust color and brightness parameters using sliders in the notebook interface.
3. The processed images and their corresponding masks will be saved in the `output_images` and `masks` folders, respectively. These folders are created automatically by the notebook if they don't yet exist. 
   
    Additionally the notebook will create a folder `output_figures` and save `.png` files with convenient figures (original image, input mask for the `grabcut` algorithm, output) for analyzing the results.
4. Repeat the process of using the interactive widgets and creating results to fine-tune the color and brightness settings.


### Parameters and Widgets

The following parameters can be adjusted for image processing using the provided interactive widgets:

- **Color Range (Hue)**: The range of hues for detecting specific colors (e.g., green and yellow). Adjustable via the **Color Range Slider**. The hue used here is part of the HSV color scheme and we provide an image of the different hues with their values for your convenience.
- **Brightness Range**: Defines the brightness levels to focus on specific regions of the image. Adjustable via the **Brightness Slider**.
- **Saturation**: Minimum saturation for pixels to be considered part of the foreground. Adjustable via the **Saturation Slider**.
- **File Selection**: Use the **File Selection Dropdown** to choose a file from the input folder for processing. (IMPORTANT: you have to select a file, otherwise applying the parameters does nothing)

You can adjust these parameters and apply them to the selected images using the **Apply Parameters** button. Do this with different images until you are content with your preselection. This selection will be used as input to the `grabcut` algorithm (a simple segmentation algo widely used for example in former photoshop versions etc).
