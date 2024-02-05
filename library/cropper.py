import skimage as ski
import os
from library.helper import rgb2rgba

from skimage.color import rgb2gray, rgba2rgb
from skimage import data

# The File Holding Settings for Cropping Current Image
profile_settings = None

# The Color Threshold When Analyzing and Operating on Pixel Colors
threshold = 100

# The Greyscale Threshold When Analyzing and Operating on Pixel Brightness
# Done This Way to Equalize Severity of Threshold
gs_threshold = threshold / 255
    
def find_boundries(img):
    """Analyzes the Provided Image and Uses Contrasting Pixels to Determine the Crop Boundries.
    Depending on Profile Settings, Could Return Multiple Crop Boundries.
    
    Parameters
    ----------
    img : image, required
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
    center_row = int((img.row_size - start_row) / 2)
    
    # The Center Column of the Image
    center_col = int((img.col_size - start_col) / 2)
    
    # The Pixel Being Analyzed
    pixel = None
    
    # The Previous Pixel Analyzed
    prev_pixel = None
    
    # Load a Greyscale Version of Image for Easier Processing if Needed
    if(type(img.grayscale) != list):
        gs_img = rgba2rgb(img.color)
        gs_img = rgb2gray(gs_img)
        img.grayscale = gs_img
    
    # Start Finding Left Boundry
    while(curr_col < img.col_size):
        # Grab Pixel Information
        pixel = img.grayscale[center_row, curr_col]
        if(prev_pixel == None): 
            prev_pixel = pixel
            continue
        
        # The Difference in the Pixel Color/Brightness
        pixel_difference = 0
        
        #if(is_grey):
        pixel_difference = pixel - prev_pixel
        
        # Make Sure the Difference is a Positive Number
        if(pixel_difference < 0): pixel_difference *= -1
        
        print(f"Pixel Difference = {pixel_difference}")
        
        # If the Difference Has Reached the Threshold
        if(pixel_difference >= gs_threshold):
            print(f"Pixel Difference Hit Threshold") 
            # Set the Left Boundry to the Current Column
            final_boundry[0] = curr_col
            # Reset Previous Pixel Value
            prev_pixel = None
            break
            
        # Run a Similar Process for Colored Image    
        #else:
            #pixel_difference = [pixel[0] - prev_pixel[0], pixel[1] - prev_pixel[1], pixel[2] - prev_pixel[2]]
            #print(f"Pixel Difference = {pixel_difference}")
            
            #if(pixel_difference[0] < 0): pixel_difference[0] *= -1
            #if(pixel_difference[1] < 0): pixel_difference[1] *= -1
            #if(pixel_difference[2] < 0): pixel_difference[2] *= -1
            
            # If Any Color Band Hits the Threshold
            #if(pixel_difference[0] > threshold or pixel_difference[1] > threshold or pixel_difference[2] > threshold):
                #print(f"Pixel Difference Hit Threshold")
                #final_boundry[0] = curr_col
                #prev_pixel = None
                #break
            
        curr_col += 1
            
    # Now Find Upper Boundry
    while(curr_row < img.row_size):
        # Grab Pixel Information
        pixel = img.grayscale[curr_row, center_col]
        if(prev_pixel == None): 
            prev_pixel = pixel
            continue
        
        # The Difference in the Pixel Color/Brightness
        pixel_difference = 0
        
        #if(is_grey):
        pixel_difference = pixel - prev_pixel
        
        # Make Sure the Difference is a Positive Number
        if(pixel_difference < 0): pixel_difference *= -1
        
        # If the Difference Has Reached the Threshold
        if(pixel_difference >= gs_threshold): 
            # Set the Upper Boundry to the Current Row
            final_boundry[1] = curr_row
            # Reset Previous Pixel Value
            prev_pixel = None
            break
            
        # Run a Similar Process for Colored Image    
        #else:
            #pixel_difference = [pixel[0] - prev_pixel[0], pixel[1] - prev_pixel[1], pixel[2] - prev_pixel[2]]
            
            #if(pixel_difference[0] < 0): pixel_difference[0] *= -1
            #if(pixel_difference[1] < 0): pixel_difference[1] *= -1
            #if(pixel_difference[2] < 0): pixel_difference[2] *= -1
            
            # If Any Color Band Hits the Threshold
            #if(pixel_difference[0] > threshold or pixel_difference[1] > threshold or pixel_difference[2] > threshold):
                #final_boundry[1] = curr_row
                #prev_pixel = None
                #break
            
        curr_row += 1
        
    # Prepare to Find the Right and Lower Boundries
    curr_row = img.row_size - 1
    curr_col = img.col_size - 1
    prev_pixel = None
    
    # Start Finding Right Boundry
    while(curr_col > final_boundry[0]):
        print(f"Current Column: {curr_col}")
        # Grab Pixel Information
        pixel = img.grayscale[center_row, curr_col]
        print(f"Pixel: {pixel}")
        if(prev_pixel == None): 
            prev_pixel = pixel
            continue
        
        # The Difference in the Pixel Color/Brightness
        pixel_difference = 0
        
        #if(is_grey):
        pixel_difference = pixel - prev_pixel
        
        # Make Sure the Difference is a Positive Number
        if(pixel_difference < 0): pixel_difference *= -1
        
        print(f"Pixel Difference: {pixel_difference}")
        
        # If the Difference Has Reached the Threshold
        if(pixel_difference >= gs_threshold): 
            print(f"Threshold Met! At {curr_col}")
            # Set the Right Boundry to the Current Column
            final_boundry[2] = curr_col
            # Reset Previous Pixel Value
            prev_pixel = None
            break
            
        # Run a Similar Process for Colored Image    
        #else:
            #pixel_difference = [pixel[0] - prev_pixel[0], pixel[1] - prev_pixel[1], pixel[2] - prev_pixel[2]]
            
            #if(pixel_difference[0] < 0): pixel_difference[0] *= -1
            #if(pixel_difference[1] < 0): pixel_difference[1] *= -1
            #if(pixel_difference[2] < 0): pixel_difference[2] *= -1
            
            # If Any Color Band Hits the Threshold
            #if(pixel_difference[0] > threshold or pixel_difference[1] > threshold or pixel_difference[2] > threshold):
                #final_boundry[2] = curr_col
                #prev_pixel = None
                #break
            
        curr_col -= 1
            
    # Now Find Lower Boundry
    while(curr_row > start_row):
        # Grab Pixel Information
        pixel = img.grayscale[curr_row, center_col]
        if(prev_pixel == None): 
            prev_pixel = pixel
            continue
        
        # The Difference in the Pixel Color/Brightness
        pixel_difference = 0
        
        #if(is_grey):
        pixel_difference = pixel - prev_pixel
        
        # Make Sure the Difference is a Positive Number
        if(pixel_difference < 0): pixel_difference *= -1
        
        # If the Difference Has Reached the Threshold
        if(pixel_difference >= gs_threshold): 
            # Set the Lower Boundry to the Current Row
            final_boundry[3] = curr_row
            # Reset Previous Pixel Value
            prev_pixel = None
            break
            
        # Run a Similar Process for Colored Image    
        #else:
            #pixel_difference = [pixel[0] - prev_pixel[0], pixel[1] - prev_pixel[1], pixel[2] - prev_pixel[2]]
            
            #if(pixel_difference[0] < 0): pixel_difference[0] *= -1
            #if(pixel_difference[1] < 0): pixel_difference[1] *= -1
            #if(pixel_difference[2] < 0): pixel_difference[2] *= -1
            
            # If Any Color Band Hits the Threshold
            #if(pixel_difference[0] > threshold or pixel_difference[1] > threshold or pixel_difference[2] > threshold):
                #final_boundry[3] = curr_row
                #prev_pixel = None
                #break
            
        curr_row -= 1
        
    # Find and Process Crop Boundries From Profiles Here
    
    print(f"Final Boundries = {final_boundry}")
    # Return Single Final Boundry
    return final_boundry

    # If Multiple Boundries, Return Them Here
    
def crop_image(img, boundries):
    """Crops Image and Returns it, Using the Boundries Provided.
    
    Parameters
    ----------
    img : image, required
        The Image Loaded from Skimage
    boundries : list, required
        The List of Boundries to Crop the Image to. 
        Can Be a List of Lists, Which Indicates Multiple Crops to Make, Usually From the First.
        
    Returns
    -------
    c_img : image or list
        The Final Image after Cropping. 
        If List, it is All of the Cropped Images from Multiple Boundries.
    """
    
    # Bool for if There are Multiple Crop Boundries
    is_multiple = type(boundries[0]) == list
    
    # Initialize Final Image Variable
    c_img = None
    if(is_multiple): c_img = [None]
    
    # Crop the First Image
    if(is_multiple == False):
        img = img.crop(boundries)
        # Go On and Return the Cropped Image
        return img
    #else:
        #c_img[0] = img[boundries[0][0]:boundries[0][2]+1, boundries[0][1]:boundries[0][3]+1]
        
def clean_image(img):
    """Cleans the Corners and Edges of the Image to Make its Background Transparent.
    
    Parameters
    ----------
    img : ndarray, required
        The Loaded Image to Clean
        
    Returns
    -------
    t_img : ndarray
        The Image Cleaned and Transparent
    """
    
    # The Starting Row
    start_row = 0
    
    # The Starting Column
    start_col = 0
    
    # The Furthest Row
    row_size = img.shape[0]
    
    # The Furthest Column
    col_size = img.shape[1]
    
    