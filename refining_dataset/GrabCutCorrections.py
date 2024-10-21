from skimage import io
from matplotlib import pyplot as plt
import numpy as np
import cv2 as cv
import os
import GrabCutCallable as gcc
from parameters import *

cursor_x=0
cursor_y=0

# Create output and mask folder if it doesn't exist
if not os.path.exists(corrected_outputs):
    os.makedirs(corrected_outputs)
if not os.path.exists(masks):
    # masks = os.path.join(os.path.dirname(__file__), masks)
    if not os.path.exists(masks):
        assert False, "masks folder does not exist, run GrabCutFolder.py first"
if not os.path.exists(corrected_masks):
    os.makedirs(corrected_masks)

# Check if the input folder exists
if not os.path.exists(input_folder):
    # input_folder = os.path.join(os.path.dirname(__file__), input_folder)
    if not os.path.exists(input_folder):
        assert False, "input folder does not exist, run GrabCutFolder.py first"

# List all image files in the input folder
image_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f)) and f != 'README.md']


adding_to_selection = False
# Brush radius for drawing
brush_radius = 30
# Mouse callback function
def draw_mask(event, x, y, flags, param):
    try:
        global drawing, mask_display, input_mask, output_mask, cursor_y, cursor_x
        cursor_x = x
        cursor_y = y

        if event == cv.EVENT_LBUTTONDOWN:
            drawing = True
            # cv.circle(mask_display, (x, y), brush_radius, (255), -1)
            for i in range(-brush_radius, brush_radius+1):
                for j in range(-brush_radius, brush_radius+1):
                    if i*i + j*j <= brush_radius*brush_radius:
                        if adding_to_selection:
                            input_mask[y+j, x+i] = 1
                            output_mask[y+j, x+i] = 1
                        else:
                            input_mask[y+j, x+i] = 0
                            output_mask[y+j, x+i] = 0

        elif event == cv.EVENT_LBUTTONUP:
            drawing = False

        elif event == cv.EVENT_MOUSEMOVE:
            if drawing:
                # cv.circle(mask_display, (x, y), brush_radius, (255), -1)
                for i in range(-brush_radius, brush_radius+1):
                    for j in range(-brush_radius, brush_radius+1):
                        if i*i + j*j <= brush_radius*brush_radius:
                            if adding_to_selection:
                                input_mask[y+j, x+i] = 1
                                output_mask[y+j, x+i] = 1
                            else:
                                input_mask[y+j, x+i] = 0
                                output_mask[y+j, x+i] = 0
    except:
        pass


# Function to display information window
def show_information_window():
    info_window = np.zeros((400, 800), np.uint8)
    cv.putText(info_window, "Features", (20, 30), cv.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
    cv.putText(info_window, "Press 'Spacebar' to apply GrabCut", (20, 80), cv.FONT_HERSHEY_SIMPLEX, 0.7, 255, 2)
    cv.putText(info_window, "Press 'Enter' to correct the next image", (20, 110), cv.FONT_HERSHEY_SIMPLEX, 0.7, 255, 2)
    cv.putText(info_window, "Press 'Esc' to cancel and exit", (20, 140), cv.FONT_HERSHEY_SIMPLEX, 0.7, 255, 2)
    cv.putText(info_window, "Press 'Backspace' or 'Ctrl'+'z' to reset Mask", (20, 170), cv.FONT_HERSHEY_SIMPLEX, 0.7, 255, 2)
    cv.putText(info_window, "Press '0'-'9' to update brush radius", (20, 200), cv.FONT_HERSHEY_SIMPLEX, 0.7, 255, 2)
    cv.putText(info_window, "Press 'tab' to switch between subtracting/adding to mask", (20, 230), cv.FONT_HERSHEY_SIMPLEX, 0.7, 255, 2)
    cv.imshow('Information', info_window)



# Process each image file
for file_name in image_files:
    # Read the input image
    input_path = os.path.join(input_folder, file_name)
    img = cv.imread(input_path)
    assert img is not None, "File could not be read, check with os.path.exists()"
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    original = img.copy()

    # if input_folder == 'spinach/no overlap/all pictures':
    img = cv.resize(img, (round(img.shape[1]/4), round(img.shape[0]/4))) #downsizing image for faster runtime
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    input_mask = np.load(os.path.join(masks, f"grabCut_input_mask_{file_name[:-4]}.npy"))
    output_mask = np.load(os.path.join(masks, f"grabCut_output_mask_{file_name[:-4]}.npy"))

    # Create a mask of the same size as the image
    mask_display = np.zeros((img.shape[0],img.shape[1]), np.uint8)
    

    # Define the desired window size
    desired_height=img.shape[1]
    desired_width=img.shape[0]

    screen_height = 800
    #downsize window until it fits on screen
    if(desired_height>screen_height):
        while(desired_height >= screen_height):
            desired_height = round(desired_height*0.9)
            desired_width = 2*round(desired_width*0.9)


    # Create a window and bind the mouse callback function
    cv.namedWindow('Image_'+file_name, cv.WINDOW_NORMAL)
    cv.setMouseCallback('Image_'+file_name, draw_mask)

    # Resize the window
    cv.resizeWindow('Image_'+file_name, desired_width, desired_height)
    cv.moveWindow('Image_'+file_name, 10, 10)

    # Flag to indicate drawing
    drawing = False

    while True:

        # Apply the darkening effect to the stacked image using the output_mask
        display_img = gcc.decrease_brightness(img, output_mask)
        # Show the image with the current mask
        display_img = cv.add(display_img, np.dstack((mask_display, mask_display, mask_display)))
        
        #drawing a circle where the cursor is with the brush radius
        cv.circle(display_img, (cursor_x, cursor_y), brush_radius, (255,255,255), -1)
        #writing text to indicate adding or removing from mask
        if adding_to_selection:
            cv.putText(display_img, "[+] i", (20, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        else:
            cv.putText(display_img, "[-] i", (20, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        
        output_mask_display = cv.convertScaleAbs(output_mask*255)
        combined_image = np.concatenate((display_img, np.dstack((output_mask_display,output_mask_display,output_mask_display))), axis=1)
        
        cv.imshow('Image_'+file_name, combined_image)

        # Wait for key events (0xFF for NumLock)
        key = cv.waitKey(1) & 0xFF

        # Press 'Enter' to finalize the mask
        if key == 32:  # 'Spacebar' key
                # Apply GrabCut using the mask
                output_mask = gcc.grabCutCallable(file_name, input_folder, corrected_outputs, masks, input_mask)
                # Resize the window
                cv.resizeWindow('Image_'+file_name, desired_width, desired_height)
                cv.moveWindow('Image_'+file_name, 10, 10)
                # reset mask_display
                mask_display = np.zeros((img.shape[0],img.shape[1]), np.uint8)
        
        if key == 13: # 'Enter' key
            output_mask = gcc.grabCutCallable(file_name, input_folder, corrected_outputs, masks, input_mask)
            img = gcc.decrease_brightness(img, output_mask)
            break

        # Press 'Esc' to cancel and exit
        if key == 27:  # Esc key
            cv.destroyAllWindows()
            exit()

        if 48<=key<=57: #number keys update brush radius
            #multiplicand defines step size
            brush_radius = 4*(key-48)
        
        if key == 8 or key == 127 or key == 26: #backspace, ctrl+z
            mask_display = np.zeros((img.shape[0],img.shape[1]), np.uint8)
            input_mask = np.load(os.path.join(masks, f"grabCut_input_mask_{file_name[:-4]}.npy"))
            output_mask = np.load(os.path.join(masks, f"grabCut_output_mask_{file_name[:-4]}.npy"))

        if key == ord('i'):  # Press 'i' to show information window
            show_information_window()
        
        if key == 9: #press 'tab' to toggle adding to selection
            adding_to_selection = not adding_to_selection
            mask_display = np.zeros((img.shape[0],img.shape[1]), np.uint8)
            



    # Save the corrected image
    output_path = os.path.join(corrected_outputs, file_name[:-4] + '.png')
    cv.imwrite(output_path, img)

    # Save the mask as a PNG
    mask_output_path = os.path.join(corrected_masks, file_name[:-4] + '.png')
    cv.imwrite(mask_output_path, output_mask * 255)

    # Close the OpenCV windows
    cv.destroyAllWindows()