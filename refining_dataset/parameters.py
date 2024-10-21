import os

# Parameters
cutoff_percentage = 0.95
# define the range of yellow hues
lower_hue = 20
upper_hue = 60

# define the range of acceptable brightness values
lower_value = 225
upper_value = 250 #really good results with 251 and 252

#define minimum saturation
lower_saturation = 150


# Input and Output Folders
input_folder = os.path.join('segmentation-pipeline', 'refining_dataset', 'input')
output_folder_figures = os.path.join('segmentation-pipeline', 'refining_dataset', 'output_figures')
output_folder_images = os.path.join('segmentation-pipeline', 'refining_dataset', 'output_images')
masks = os.path.join('segmentation-pipeline', 'refining_dataset', 'masks')
corrected_outputs = os.path.join('segmentation-pipeline', 'refining_dataset', 'corrected_outputs')
corrected_masks = os.path.join('segmentation-pipeline', 'refining_dataset', 'corrected_masks')