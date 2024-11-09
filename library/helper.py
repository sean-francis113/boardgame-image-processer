import library.settings as settings

import skimage as ski
import numpy as np
import classes.image as image
from copy import deepcopy
import library.converter as convert

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
            img = convert.rgb2rgba(img)
        
    return img


'''def rgb2rgba(img):
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
    """Converts an image from RGB to YUV. Grabbed from https://gist.github.com/Quasimondo/c3590226c924a06b276d606f4f189639"""
    m = np.array([[0.2126, 0.7152,  0.0722],
                 [0.09991, -0.33609, 0.436],
                 [0.615, -0.55861, -0.05639]])
     
    yuv = np.dot(img.color,m)
    yuv[:,:,1:]+=128.0
    img.color = yuv

def yuv2rgb(img:image.image):
    """Converts an image from YUV to RGB. Grabbed from https://gist.github.com/Quasimondo/c3590226c924a06b276d606f4f189639"""
    m = np.array([[ 1.0, 1.0, 1.0],
                 [-0.000007154783816076815, -0.3441331386566162, 1.7720025777816772],
                 [ 1.4019975662231445, -0.7141380310058594 , 0.00001542569043522235] ])
    
    rgb = np.dot(img.color,m)
    rgb[:,:,0]-=179.45477266423404
    rgb[:,:,1]+=135.45870971679688
    rgb[:,:,2]-=226.8183044444304
    rgb = rgb.clip(0,255)
    img.color = rgb'''

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
    
def ensure_folder_path(path:str):
    """Ensures There is a Forwardslash (\\) or Backslash (/) at the End of the Folder Path
    
    Parameters
    ----------
    path : str, required
        The Path to Ensure
    slash : str, optional
        Which Slash is Used in the OS for Filepaths.
    """
    
    slash = ""

    if("\\" in path):
        slash = "\\"
    elif("/" in path):
        slash = "/"
    else:
        settings.log_file.enter(f"\"{path}\" is Not a Valid Folder Path. Assuming {path} is a File", True)
        slash = "\\"

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
    true_filepath = ensure_folder_path(slash.join(str_list[:-1]))
    file_extension = f".{file_name_full.split('.')[1]}"
    relative_filepath = ""
    if(parent_dir != ""):
        relative_filepath = ensure_folder_path(true_filepath.replace(parent_dir, ""))
        
    return file_name, true_filepath, file_extension, relative_filepath

def get_transparency(img):
    """Stores All Transparent Pixels for Future Restoration"""

    if(type(img) == image.image):
        img.get_transparency()
        return
    
    transparent_pixels = []

    row_iter = 0
    col_iter = 0

    while row_iter < img.shape[0]:
        col_iter = 0
        while col_iter < img.shape[1]:
            if(img[row_iter, col_iter][3] == 0):
                transparent_pixels.append([row_iter, col_iter])
            col_iter += 1
        row_iter += 1

    return transparent_pixels

def restore_transparency(img, transparent_pixels=[]):
    """Restores All Stored Transparent Pixels"""

    if(type(img) == image.image):
        img.restore_transparency()
        return

    if(len(transparent_pixels) == 0):
        settings.log_file.enter(f"No Transparent Pixels Provided!", True)
        return

    for pixel in transparent_pixels:
        img[pixel[0], pixel[1]][3] = 0

    settings.log_file.enter(f"Pixels Restored!", True)