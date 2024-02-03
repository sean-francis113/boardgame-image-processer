import skimage as ski
import os
from helper import rgb2rgba

from skimage.color import rgb2gray
from skimage import data

# The File Holding Settings for Cropping Current Image
profile_settings = None

# The Current Image to be Cropped
curr_image = None

# The Color Threshold When Analyzing and Operating on Pixel Colors
threshold = 50

# The Greyscale Threshold When Analyzing and Operating on Pixel Brightness
gs_threshold = 0.25
    
def find_boundries(img):
    """Analyzes the Provided Image and Uses Contrasting Pixels to Determine the Crop Boundries.
    Depending on Profile Settings, Could Return Multiple Crop Boundries.
    
    Parameters
    ----------
    img : ndarray, required
        The Image Loaded from Skimage
    
    Returns
    -------
    boundries : list
        The Boundries of the Cropping. 
        Will Always Return a List With a Length of One (1), the Contents Being a List of [Left, Upper, Right, Lower],
            However Can Return a Longer List of Boundries Depending on the Profile Settings.
    """
    
    # The Main Boundry to Be Returned
    final_boundry = [0, 0, 0, 0]

    # Bool for if image is greyscale
    is_grey = len(img.shape) == 2
    
    # The Furthest Horizontal Pixel
    max_rows = 0
    
    # The Furthest Vertical Pixel
    max_cols = 0
    
    # The Row to Start Analyzing
    # Will Be Pulled from Profile Settings
    start_row = 0
    
    # The Column to Start Analyzing
    # Will Be Pulled from Profile Settings
    start_col = 0
    
    # The Current Row Being Analyzed
    curr_row = start_row
    
    # The Current Column Being Analyzed
    curr_col = start_col
    
    # The Center Row of the Image
    center_row = (max_rows - start_row) / 2
    
    # The Center Column of the Image
    center_col = (max_cols - start_col) / 2
    
    # The Pixel Being Analyzed
    pixel = None
    
    # The Previous Pixel Analyzed
    prev_pixel = None
    if(is_grey): prev_pixel = 1.0
    else: prev_pixel = [255,255,255,255]
    
    # Start Finding Left Boundry
    while(curr_col < max_cols):
        # Grab Pixel Information
        pixel = img[center_row, curr_col]
        
        # The Difference in the Pixel Color/Brightness
        pixel_difference = 0
        
        if(is_grey):
            pixel_difference = pixel - prev_pixel
            
            # Make Sure the Difference is a Positive Number
            if(pixel_difference < 0): pixel_difference *= -1
            
            # If the Difference Has Reached the Threshold
            if(pixel_difference >= gs_threshold): 
                # Set the Left Boundry to the Current Column
                final_boundry[0] = curr_col
                break