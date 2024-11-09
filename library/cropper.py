import library.settings as settings

import skimage as ski
import os
import library.helper as h
import library.converter as convert
import numpy
from skimage.color import rgb2gray, rgba2rgb
from skimage import data
from classes import image

# The File Holding Settings for Cropping Current Image
profile_settings = None

# The Color Threshold When Analyzing and Operating on Pixel Colors
threshold = 100

# The Greyscale Threshold When Analyzing and Operating on Pixel Brightness
# Done This Way to Equalize Severity of Threshold Between Color and Grayscale
gs_threshold = threshold / 255

# The Pixel Value to Compare To
base_pixel_gs = 1.0 # Grayscale White

def find_boundries(img, final_boundry=[]):
    """Analyzes the Provided Image and Uses Contrasting Pixels to Determine the Crop Boundries.
    Depending on Profile Settings, Could Return Multiple Crop Boundries.
    
    Parameters
    ----------
    img : image, required
        The Image Loaded from Skimage
    final_boundry : list, optional
        The Final List of Boundries Found in the Image.
        Will Be Filled By the Function.
    
    Returns
    -------
    boundries : list
        The Boundries of the Cropping. 
        Will Always Return a List With a Length of One (1), the Contents Being a List of [Left, Upper, Right, Lower].
        If Multiple Objects Are Found, the List Will Contain the Boundries of All Objects
    """
    
    settings.log_file.enter(f"Starting to Find Boundries")
    
    # A Copy of the Image to Work On
    c_img = image.image(
                        n=img.name,
                        tfp=img.true_folder_path,
                        ie=img.image_extension
                        )
    c_img.copy_from(img)
    
    # The Current Boundry
    this_boundry = [0, 0, 0, 0]
    
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
    center_row = int((c_img.row_size - start_row) / 2)
    
    # The Center Column of the Image
    center_col = int((c_img.col_size - start_col) / 2)
    
    # The Pixel Being Analyzed
    pixel = None
    
    # The Previous Pixel Analyzed
    # NO LONGER USED
    #prev_pixel = None
    
    # The Difference in the Pixel Color/Brightness
    pixel_difference = 0
    
    # If Boundry Was Found
    bound_found = False
    
    # How Much Padding To Determine the Edge of an Object
    padding = 200
    
    # The Counter for Checking for Padding
    pad_count = 0
    
    # The Pixel That Started the Padding Count
    pad_start = []
    
    # Load a Greyscale Version of Image for Easier Processing if Needed
    if(type(c_img.grayscale) != numpy.ndarray):
        settings.log_file.enter(f"Couldn't Find Grayscale. Loading One")
        gs_img = rgba2rgb(c_img.color)
        gs_img = rgb2gray(gs_img)
        c_img.grayscale = gs_img
        c_img.grayscale_transparent = convert.gray2rgba(gs_img)
    
    # Start Finding Left Boundry
    settings.log_file.enter(f"Finding Left Boundry")
    while(curr_col < c_img.col_size):
        if(bound_found == False):
            curr_row = start_row
            # Search Each Pixel in Column for Threshold.
            while(curr_row < c_img.row_size):
                # Grab Pixel Information
                pixel = c_img.grayscale[curr_row, curr_col]
                #if(prev_pixel == None): 
                    #prev_pixel = pixel
                    #continue
                
                # Ensure Number is Positive
                pixel_difference = abs(pixel - base_pixel_gs)
                
                # If the Difference Has Reached the Threshold
                if(pixel_difference >= gs_threshold):
                    settings.log_file.enter(f"Pixel Difference Hit Threshold")
                    settings.log_file.enter(f"Base: {base_pixel_gs}; Current: {pixel}; Difference: {pixel_difference}", True) 
                    # Set the Left Boundry to the Current Column
                    this_boundry[0] = curr_col
                    settings.log_file.enter(f"Left Boundry: {curr_col}", True)
                    bound_found = True
                    settings.log_file.enter(f"Finding Right Boundry")
                    curr_col += 1 # To Set Up For Finding Right Boundry Next
                    break
                
                curr_row += 1
            
        # Use Left Boundry to Find Right Boundry
        elif(bound_found == True):
            # Grab The Next Paddings Worth of Pixels in Next Few Columns
            test_pixels = c_img.grayscale[curr_row:curr_row + padding + 1, curr_col:curr_col + 5]
            
            # Test if Any Pixels in test_pixels Hit Threshold.
            # If Not, We've Hit the Right Boundry and Can Break Completely Out of Loop
            if(len(test_pixels[numpy.nonzero(abs(test_pixels - base_pixel_gs) > gs_threshold)]) == 0):
                settings.log_file.enter(f"Found Right Boundry")
                settings.log_file.enter(f"Right Boundry: {curr_col}", True)
                this_boundry[2] = curr_col
                break
            
        curr_col += 1
        
    # Now to Find the Upper and Lower Boundries Using the Left and Right
    settings.log_file.enter(f"Finding Upper Boundry")
    
    # The Range of Columns to Search Through
    min_col, max_col = (this_boundry[0], this_boundry[2])
    curr_row = start_row
    bound_found = False
    
    while(curr_row < c_img.row_size):
        # Searching for Upper Boundry
        if(bound_found == False):
            test_pixels = c_img.grayscale[curr_row, min_col:max_col + 1]
            
            # If a Pixel Above Threshold is Found Assume It is the Upper Bound
            if(len(test_pixels[numpy.nonzero(abs(test_pixels - base_pixel_gs) > gs_threshold)]) > 0):
                settings.log_file.enter(f"Found Upper Boundry")
                settings.log_file.enter(f"Upper Boundry: {curr_row}", True)
                this_boundry[1] = curr_row
                bound_found = True
                curr_row += 1
                settings.log_file.enter(f"Finding Lower Boundry")
                
        # Searching for Lower Boundry
        elif(bound_found == True):                                
            test_pixels = c_img.grayscale[curr_row, min_col:max_col + 1]
            
            # Test if Any Pixels in test_pixels Hit Threshold.
            # If Not, We've Hit the Lower Boundry and Can Break Completely Out of Loop
            if(len(test_pixels[numpy.nonzero(abs(test_pixels - base_pixel_gs) > gs_threshold)]) == 0):
                settings.log_file.enter(f"Found Lower Boundry")
                settings.log_file.enter(f"Lower Boundry: {curr_row}", True)
                this_boundry[3] = curr_row
                break
            
        curr_row += 1
  
    settings.log_file.enter(f"Found Boundry {this_boundry}")    
    # If A Crop Boundry Was Found
    if(this_boundry != [0,0,0,0]):
        settings.log_file.enter(f"Adding Boundry to List")
        final_boundry.append(this_boundry)
        settings.log_file.enter(f"Whiting Out Boundry for Next Search")
        c_img.white_out([this_boundry[0] - 10, this_boundry[1] - 10, this_boundry[2] + 10, this_boundry[3] + 10])
        
        img_check = c_img.grayscale[numpy.nonzero(abs(c_img.grayscale - base_pixel_gs) > gs_threshold)]
        settings.log_file.enter(img_check)
        
        if(len(img_check) > padding):
            return find_boundries(c_img, final_boundry)
        else:
            return final_boundry
    else:
        if(final_boundry == []):
            settings.log_file.enter(f"No Boundries Found")
            return None
        settings.log_file.enter(f"Final Boundries: {final_boundry}")
        return final_boundry
    
def crop_image(img, boundries):
    """Crops Image and Returns it, Using the Boundries Provided.
    
    Parameters
    ----------
    img : image, required
        The Image Loaded from Skimage
    boundries : list, required
        The List of Boundries to Crop the Image to. 
        Can Be a List of Lists, Which Indicates Multiple Crops to Make.
        
    Returns
    -------
    c_img : image or list
        The Final Image after Cropping. 
        If List, it is All of the Cropped Images from Multiple Boundries.
    """
    
    settings.log_file.enter(f"Starting Crop Process")
    
    # Bool for if There are Multiple Crop Boundries
    is_multiple = len(boundries) > 1
    settings.log_file.enter(f"Multiple Crops: {is_multiple}")
    
    # Initialize Final Image Variable
    c_img = None
    if(is_multiple): c_img = [None]
    
    # Crop the Image
    if(is_multiple == False):
        # Go On and Return the Cropped Image
        return img.crop(boundries[0])
    else:
        settings.log_file.enter(f"Starting Multiple Crops")
        c_img = []
        num_iter = 1
        
        # Add Cropped Images to Final List
        for bound in boundries:
            temp_img = image.image()
            temp_img.copy_from(img)
            
            c_img.append(temp_img.crop(bound))
            num_iter += 1
            
        return c_img
        
        
def clean_image(img):
    """Cleans the Corners and Edges of the Image to Make its Background Transparent.
    
    Parameters
    ----------
    img : image, required
        The Loaded Image to Clean
        
    Returns
    -------
    t_img : image
        The Image Cleaned and Transparent
    """
    
    # The Starting Row
    start_row = 0
    
    # The Starting Column
    start_col = 0

    # The Current Row
    curr_row = start_row
    
    # The Current Column
    curr_col = start_col

    # A Copy of the Image to Analyze and Work On
    c_img = image.image(
        n = img.name,
        tfp = img.true_folder_path,
        ie = img.image_extension        
    )
    c_img.copy_from(img)

    # Pixels to Make Transparent
    pixel_ranges = []

    # Start from Upper Left Corner and Head Down to the Lower Left Corner
    while(curr_row < c_img.row_size):
        curr_col = start_col
        while(curr_col < c_img.col_size):
            pixel = c_img.grayscale[curr_row, curr_col]
            pixel_difference = abs(pixel - base_pixel_gs)
            
            
            # If Threshold is Met, or We Hit the Edge of the Image, We've Hit the Ending Column
            if(pixel_difference > gs_threshold or curr_col >= c_img.col_size - 1):
                pixel_ranges.append([[curr_row, start_col], [curr_row, curr_col]])
                curr_row += 1
                break
            
            curr_col += 1
    
    curr_row = start_row
    curr_col = c_img.col_size - 1
    # Start From the Upper Right Corner and Head Down to the Lower Right Corner
    while(curr_row < c_img.row_size):
        curr_col = c_img.col_size - 1
        while(curr_col >= start_col):
            pixel = c_img.grayscale[curr_row, curr_col]
            pixel_difference = abs(pixel - base_pixel_gs)
            
            # If Threshold is Met, or We Hit the Edge of the Image, We've Hit the Ending Column
            if(pixel_difference > gs_threshold or curr_col == start_col):
                pixel_ranges.append([[curr_row, curr_col], [curr_row, c_img.col_size - 1]])
                curr_row += 1
                break
            
            curr_col -= 1
            
    # Run Through Whole List of Ranges
    for range in pixel_ranges:
        row_iter = range[0][0] # Get Range's Starting Row
        col_iter = range[0][1] # Get Range's Starting Column
        while(row_iter <= range[1][0]): # While Iterator Has Not Passed Ending Row
            while(col_iter <= range[1][1]): # While Iterator Has Not Passed Ending Column
                c_img.color[row_iter, col_iter][3] = 0 # Set Transparency of Pixel to Transparent
                col_iter += 1
            
            row_iter += 1
            
    return c_img