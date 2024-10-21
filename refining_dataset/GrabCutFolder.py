from skimage import io
from matplotlib import pyplot as plt
import numpy as np
import cv2 as cv
import os
from parameters import *

#######################################


# Create output and mask folder if it doesn't exist
if not os.path.exists(output_folder_figures):
    os.makedirs(output_folder_figures)
if not os.path.exists(masks):
    os.makedirs(masks)
if not os.path.exists(output_folder_images):
    os.makedirs(output_folder_images)

# List all image files in the input folder
image_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f)) and f != 'README.md']

# Process each image file
#TODO: parallelize this
#TODO: remove scaling down of images
for file_name in image_files:
    print("Processing", file_name)
    # Read the input image
    input_path = os.path.join(input_folder, file_name)
    img = cv.imread(input_path)

    img = cv.resize(img, (round(img.shape[1]/4), round(img.shape[0]/4))) #downsizing image for faster runtime
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    original = img

    assert img is not None, "file could not be read, check with os.path.exists()"

    def is_color(rgb):
        # convert rgb to hsv
        hsv = cv.cvtColor(np.array([[rgb]], dtype=np.uint8), cv.COLOR_RGB2HSV)[0][0]
        
        # get the hue, saturation and value 
        hue = hsv[0]
        saturation = hsv[1]
        value = hsv[2]

        # check if hue is in the range of yellwo and value is not too dark or too light (brightness)
        return ((lower_value <= value <= upper_value) & (lower_hue <= hue <= upper_hue) & (saturation > lower_saturation))

    def decrease_brightness(img, mask):
        # Convert the image to HSV color space
        hsv_img = cv.cvtColor(img, cv.COLOR_RGB2HSV)
        # Define the brightness adjustment factor (you can change this value to control the brightness)
        darkening_factor = 0.25
        # Set the brightness channel (V) of the pixels with mask value 1 to a lower value
        hsv_img[:, :, 2] = np.where(mask == 0, hsv_img[:, :, 2] * darkening_factor, hsv_img[:, :, 2])
        # Convert the image back to RGB color space
        modified_img = cv.cvtColor(hsv_img, cv.COLOR_HSV2BGR)
        
        return modified_img

    #mask cv.GC_BGD, cv.GC_FGD, cv.GC_PR_BGD, cv.GC_PR_FGD, or simply pass 0,1,2,3 to image.
    mask = np.zeros((img.shape[0],img.shape[1]), np.uint8)
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            current_R = img[i,j][0] #temporary variables for pixel (runtime)
            current_G = img[i,j][1]
            current_B = img[i,j][2]
            if(is_color((current_R,current_G,current_B))):
                mask[i,j] = 1
            else:
                mask[i,j] = 2

    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, np.ones((5,5),np.uint8))
    np.save(masks + "/grabCut_input_mask_" + file_name[:-4] + ".npy", mask)



    # mask = np.zeros(img.shape[:2],np.uint8)
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)
    rect = (0,0,img.shape[0],img.shape[1])
    cv.grabCut(img,mask,rect,bgdModel,fgdModel,iterCount=5, mode=cv.GC_INIT_WITH_MASK)
    #making a mask which is 1 where the mask is 1 or 3 (foreground) and 0 where the mask is 0 or 2 (background)
    mask2 = np.where((mask==2)|(mask==0),0,1)
    
    np.save(masks + "/grabCut_output_mask_" + file_name[:-4] + ".npy", mask2)
    img = decrease_brightness(img, mask2)
    cv.imwrite(output_folder_images+"/" + file_name, img)


    #PLOTTING THE IMAGES
    fig = plt.figure(figsize=(10, 10))  
    # setting values to rows and column variables
    rows = 2
    columns = 2

    # Adds a subplot
    fig.add_subplot(rows, columns, 1)
    # showing image
    plt.imshow(original)
    plt.axis('off')
    plt.title("original")

    # Adds a subplot
    fig.add_subplot(rows, columns, 2)
    # showing image
    plt.imshow(mask)
    plt.colorbar()
    plt.axis('off')
    plt.title("mask")

    # Adds a subplot
    fig.add_subplot(rows, columns, 3)
    # showing image
    plt.imshow(mask2)
    plt.colorbar()
    plt.axis('off')
    plt.title("GrabCut result")

    # Adds a subplot
    fig.add_subplot(rows, columns, 4)
    # showing image
    plt.imshow(img)
    plt.axis('off')
    plt.title("result")

    # Save the figures to the output folder
    fig.savefig(output_folder_figures+"/figures_" + file_name[:-4]+".png")
    plt.close(fig)