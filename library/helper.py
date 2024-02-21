import library.settings as settings

import skimage as ski
import numpy as np
import classes.image as image
from copy import deepcopy

def load_image(img_path, grayscale = False):
    """Takes an Image's Filepath, Loads It (As Greyscale If Requested) with Skimage, Then Returns the Loaded Image.
    
    Parameters
    ----------
    img_path : str, required
        The Full Filepath of the Image 
    """

    settings.log_file.enter(f"Attempting to Load {img_path} With Grayscale={grayscale}")
    # Attempts to Load Image
    img = ski.io.imread(img_path, as_gray=grayscale)

    # Check if Image Was Not Loaded as Greyscale
    if(grayscale == False):

        # The Number of Color Channels in the Image (3 = RGB, 4 = RGBA)
        max_channels = img.shape[-1]
        settings.log_file.enter(f"Channels: {max_channels}", True)
        
        if(max_channels != 4):
            settings.log_file.enter(f"Converting Image to RGBA")
            img = rgb2rgba(img)
        
    return img

def rgb2rgba(img):
    """Converts the Provided Image from RGB to RGBA, Adding Alpha Values to Every Pixel.
    
    Parameters
    ----------
    img : ndarray, required
        The Loaded Image to Convert
    
    Returns
    -------
    The Converted Image, as an ndarray
    """
    
    return np.insert(img, 3, 255, axis=2)

def rgba2rgb(img:image, background=[255,255,255], save_transparency=True):
    """Converts Color Image to RGB by Changing Transparent Pixels to the Background Color, Then Removes Alpha Channel"""

    if(save_transparency): img.get_transparency()

    row_iter = 0
    col_iter = 0

    while row_iter < img.row_size:
        col_iter = 0
        while col_iter < img.col_size:
            if(img.color[row_iter, col_iter][3] == 0):
                img.color[row_iter, col_iter] = [background[0], background[1], background[2], 1]
            col_iter += 1
        row_iter += 1

    img.color = img.color[:,:,:3]

def rgb2yuv(img:image.image):
    """Uses Conversion Formulae Found at https://softpixel.com/~cwright/programming/colorspace/yuv/ to Convert Color Image from RGB to YUV"""

    if(img.image_extension.lower() == ".jpeg"):
        settings.log_file.enter(f"Image is in JPEG Format, Which Uses a YUV-Like Colorspace. Converting to RGB, then Back to YUV.")
        return # FOR NOW
    
    yuv_img = deepcopy(img.color)

    row_iter = 0
    col_iter = 0
    while row_iter < img.row_size:
        col_iter = 0
        while col_iter < img.col_size:
            pixel = img.color[row_iter, col_iter]
            r = pixel[0]
            g = pixel[1]
            b = pixel[2]
            yuv_img[row_iter, col_iter] = [
                (r * 0.299000) + (g * 0.587000) + (b * 0.11400), 
                (r * -0.168736) + (g * -0.331264) + (b * 0.500000) + 128,
                (r * 0.500000) + (g * -0.418688) + (b * -0.081312) + 128
                ]
            col_iter += 1
        row_iter += 1
            
    img.color = yuv_img


def display_image_data(img_path, grayscale = False):
    """Tester Function to Display the Dimensions and Channels of an Image.
    
    Parameters
    ----------
    img_path : str, required
        The Full Filepath of the Image
    """
    
    img = load_image(img_path, grayscale)
    print(img.shape)
    print(img[0,0])
    
def ensure_folder_path(path:str, slash="\\"):
    """Ensures There is a Forwardslash (\\) or Backslash (/) at the End of the Folder Path
    
    Parameters
    ----------
    path : str, required
        The Path to Ensure
    slash : str, optional
        Which Slash is Used in the OS for Filepaths.
    """
    
    if(path[-1] != slash):
        return f"{path}{slash}"
    else:
        return path
    
def seperate_file_info(filepath:str, parent_dir=""):
    """Seperates the Filepath Into Filename, True Filepath, File Extension, and Relative Filepath. 
    If parent_dir is Provided, Relative Filepath is the Filepath with parent_dir Removed. Otherwise, it is an Empty String.

    Args:
        filepath (str): The Filepath to Seperate Out.
        parent_dir (str, optional): The Directory to Remove from Relative Filepath. If Not Provided, Relative Filepath is Empty. Defaults to "".
    """
    
    # Which Slash is Used in the Filepath
    slash = "\\"

    str_list = filepath.split(slash)

    # Handle Both Slashes
    if(len(str_list) == 1 and "/" in str_list[0]):
        slash = "/"
        str_list = filepath.split("/")
    
    file_name_full = str_list[-1]
    file_name = file_name_full.split(".")[0]
    true_filepath = ensure_folder_path(slash.join(str_list[:-1]), slash)
    file_extension = f".{file_name_full.split('.')[1]}"
    relative_filepath = ""
    if(parent_dir != ""):
        relative_filepath = ensure_folder_path(true_filepath.replace(parent_dir, ""), slash)
        
    return file_name, true_filepath, file_extension, relative_filepath